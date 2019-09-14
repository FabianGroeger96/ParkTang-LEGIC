-----------------------------------------------------------------------------
Copyright (C) 2019 LEGIC (R) Identsystems AG, CH-8623 Wetzikon
Restricted use for HSLU Hackathon 2019. All rights reserved!
-----------------------------------------------------------------------------

The modules LEGIC_SM6300_Signature and DigitalSignature should contain all functions you need to know for the
Hackathon.

Dependencies:
- python >= v3.5: uses builtin bytes and hex

Site-Packages:
- pyserial (latest): for serial communication with LEGIC SM6300
- ecdsa (latest): for signature verification


Use LEGIC_SM6300_Signature (LEGIC_SM6300_Signature.py) to create signatures using LEGIC SM6300 chip.
The SM6300 will create signatures with the pre-loaded private key.
Create digital-signatures:

    signature = LEGIC_SM6300_Signature('/dev/ttyUSB0').create(b'your data')


Use DigitalSignature (DigitalSignature.py) to verify signatures created with LEGIC SM6300.
Verify digital-signature:

    valid = DigitalSignature.verify(b'your data', signature, pub_pem_path='public_key.pem')
    assert valid is True


Make sure you use the correct public-key for the verification. The LEGIC USB-Stick (EVS) should be already labeled with its unique chip ID.
The class LEGIC_SM6300 will print the chip ID to the console on every successful connect(). The corresponding key files are located under './keys/<chip-ID>_public.pem'
e.g. the public key for Chip-ID: "LEGIC-SM6300-1D37BCF9A62CBF08" is './keys/LEGIC-SM6300-1D37BCF9A62CBF08_public.pem'


Checkout __main__ section in LEGIC_SM6300_Signature for example calls.
