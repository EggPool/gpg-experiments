# OpenPGP Tokens

Main thing to check is that the token supports 4096 bits RSA keys.

## Yubikey

* Yubikey 5 NFC , 5c, Nano are ok  
https://www.yubico.com/products/yubikey-hardware/compare-yubikeys/  
  They also embed other functions such as OTP and several OAUTH as well as FIDO2 U2F.

## Nitrokey

* Nitrokey Start - GnuK (slow, 8 sec per signature)
  https://shop.nitrokey.com/shop/product/nitrokey-start-6
* Nitrokey Pro 2 - embeds a real openpgp card  
  https://shop.nitrokey.com/shop/product/nitrokey-pro-2-3

Installation reference:
https://www.nitrokey.com/documentation/installation

## GnuK

gnuK is a software only emulation of openpgp hardware.  
Used on chheap tokens, not the same level of security, since the private key could possibely be extracted from the microcontroller.
