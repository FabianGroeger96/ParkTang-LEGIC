"""
Copyright (C) 2019 LEGIC (R) Identsystems AG, CH-8623 Wetzikon
Restricted use for HSLU Hackathon 2019. All rights reserved!

PROJECT:    Blockchain Hackathon
MODULE:     Interface to sign messages using LEGIC SM6300 as secure key store (Secure Element)

$File: LEGIC_SM6300_Signature.py$
$Revision: 8$
"""
import os

from lib.LEGIC_SM6300 import LEGIC_SM6300
from lib.DigitalSignature import DigitalSignature


# -------------------------------------------------------------------------------------------------------------------|
class LEGIC_SM6300_Signature:

    def __init__(self, port='/dev/ttyUSB0'):
        """
        establish connection to SM6300 and forward the only required function: 'create' signature

        :param port: serial connection identifier
                     e.g. for windows: 'COM1'
                          for linux:   '/dev/ttyUSB0'
        """
        sm6300 = LEGIC_SM6300(port)
        sm6300.connect()
        self.digitalSignature = DigitalSignature(sm6300)

    # ---------------------------------------------------------------------------------------------------------------|
    def create(self, message):
        """
        create signature from the given message using SHA256 and Elliptic Curve (EC) NIST256p

        :param message: string or bytes
        :return: signature as bytes ASN.1 DER encoded (compatible to OpenSSL)
        """
        return self.digitalSignature.create(message)


# -------------------------------------------------------------------------------------------------------------------|
if __name__ == "__main__":

    port = '/dev/ttyUSB0'
    # port = 'COM14'

    # ---------------------------------------------------------------------------------------------------------------|
    """
    1. example to create signatures using LEGIC-SM6300 with pre-loaded private key

        replace test_message with any data/payload you would like to create a signature
        e.g.: text/string:  test_message = 'your text message'
              bytes:        test_message = b'\x79\x6F\x75\x72\x20\x74\x65\x78\x74\x20\x6D\x65\x73\x73\x61\x67\x65'
    """
    test_message = 'your text message'
    signature = LEGIC_SM6300_Signature(port).create(test_message)

    # convert strings to bytes
    if isinstance(test_message, str):
        test_message = test_message.encode()

    print('test_message: "%s" = 0x%s' % (test_message, test_message.hex().upper()))
    print('signature: 0x%s' % signature.hex().upper())

    # ---------------------------------------------------------------------------------------------------------------|
    """
    2. example to verify a signature with public key file

        replace chipID bellow with the chip-ID used to create the signature to use the correct
        public key file for verification

        note: the verification is done using the python ecdsa package from https://pypi.org/project/ecdsa/
              the verification therefore does NOT require any connection to the LEGIC SM6300

    """
    # chipID = 'LEGIC-SM6300-1D37BCF9A62CBF08'
    # chipID = 'LEGIC-SM6300-1D78A6A5F308C231'
    chipID = 'LEGIC-SM6300-3B5005E4EFA84CD5'
    # chipID = 'LEGIC-SM6300-39DD28D483F38763'
    # chipID = 'LEGIC-SM6300-06187322BF40BE60'
    # chipID = 'LEGIC-SM6300-B8B76B5C3534B709'
    # chipID = 'LEGIC-SM6300-C1B1D181E07097F8'
    # chipID = 'LEGIC-SM6300-FA5C7431DC80F112'

    pub_key_file = os.path.join('keys', chipID + '_public.pem')
    valid = DigitalSignature.verify(test_message, signature, pub_pem_path=pub_key_file)
    assert valid is True, 'message signature verification failed. ' \
                          '-> check if you use the correct public-key-file for verification'
