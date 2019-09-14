import serial
import binascii
import numpy as np
import paho.mqtt.client as mqtt  # import the client1
import json

if __name__ == "__main__":

    port = '/dev/ttyUSB0'

    ser = serial.Serial(
        port=port,
        baudrate=115200,
        timeout=0.2
    )

    broker_address = "127.0.0.1"
    client = mqtt.Client("P1")  # create new instance
    client.connect(broker_address)  # connect to broker

    counter = 0
    parked = False
    uid_car = None
    uid_park_space = "80808080806504"

    while True:
        packet = bytearray()
        packet.append(0x04)
        packet.append(0x00)
        packet.append(0x02)
        packet.append(0x79)
        packet.append(0x40)
        ser.write(packet)

        output = ser.read(6)
        hex_string = binascii.hexlify(output).decode('utf-8')
        bytes_arr = [hex_string[i:i + 2] for i in range(0, len(hex_string), 2)]

        if bytes_arr[2] == '00':
            packet = bytearray()
            packet.append(0x06)
            packet.append(0x3D)
            packet.append(0x00)
            packet.append(0x01)
            packet.append(0x02)
            packet.append(0xF6)
            packet.append(0xA7)
            ser.write(packet)

            output = ser.read(30)
            hex_string = binascii.hexlify(output).decode('utf-8')
            bytes_arr = np.array([hex_string[i:i + 2] for i in range(0, len(hex_string), 2)])

            if bytes_arr[0] == '1d':
                uid = bytes_arr[7:14]
                if len(uid) > 0:
                    counter += 1
                    if counter > 10 and not parked:
                        counter = 0
                        parked = True
                        uid_car = "".join(uid)

                        data = {"parkSpaceId": str(uid_park_space), "carId": str(uid_car)}
                        data = json.dumps(data)
                        client.publish("parkin", data)
                        print("Parking in | Parkspace: %s, Car: %s" % (uid_park_space, uid_car))
                else:
                    counter += 1
                    if counter > 10 and parked and uid_car is not None:
                        data = {"parkSpaceId": uid_park_space, "carId": uid_car}
                        data = json.dumps(data)
                        client.publish("parkout", data)
                        print("Parking out | Parkspace: %s, Car: %s" % (uid_park_space, uid_car))

                        counter = 0
                        parked = False
                        uid_car = None
            elif bytes_arr[0] == '04':
                counter += 1
                if counter > 10 and parked and uid_car is not None:
                    data = {"parkSpaceId": uid_park_space, "carId": uid_car}
                    data = json.dumps(data)
                    client.publish("parkout", data)
                    print("Parking out | Parkspace: %s, Car: %s" % (uid_park_space, uid_car))

                    counter = 0
                    parked = False
                    uid_car = None

        ser.flush()

    ser.close()
