# GPG Experiments

PGP/GPG Experiments with RSA

Highly experimental, use at your own risks and only if you understand what you're doing.

## Pre-requisites

- openpgp compatible token, like a nitrokey or yubikey or a gnuk token  
  TODO: list compatible cards and shops
- Done on Ubuntu, same on other linuxes
- GPG v1
- GPG v2
- Monkeysphere `sudo apt install monkeysphere`
- Drivers (TODO: see nitrokey install)
- Python3
- air gap secure machine, like a tail distro if you want to use the keys IRL

## Token initialisation

- Set the reset, admin and user pin (in that order)
- `gpg2 --card-edit`
- `admin`
- `passwd`
- Select 4 "Set the reset code", set pin code. Then 3 "Admin PIN", then 1 "Change PIN"

Ref: http://www.fsij.org/doc-gnuk/gnuk-passphrase-setting.html#set-up-pw1-pw3-and-reset-code

## Create a signature key

- `gpg2 --full-gen-key --expert`
- Choice 4 RSA, sig only
- 4096 bits
- 0 (do not expire)
- set a passphrase
- wait for entropy and key generation

This will give you the ID of the newly created key, like  
"pub rsa4096/C6963FA6" : C6963FA6 is your key id.

You can get the list via `gpg2 --list-keys`

## Backup the key

"Armor" format is ascii format, unarmored is binary.

Armor:  
`gpg2 --armor --export-secret-keys YOUR_KEY_ID > your_key_id.secret.asc`

Unarmored:  
`gpg2 --export-secret-keys YOUR_KEY_ID > your_key_id.secret.bin`

> Note: To wrap a file in PGP ASCII armor, use `gpg2 --enarmor < filename.bin > filename.txt`  
To unwrap a file already in PGP ASCII armor, use `gpg2 --dearmor < filename.txt > filename.bin`

## Move the key to the pgp card

## Export the pubkey

## Export the privkey

## Convert the keys to .pem

In order to convert the key to pem format, we need a key exported without a passphrase.  
gpg2 does not allow that. So we use gpg as a temporary step.

- export gpg2 | import gpg
- remove passphrase
- export unencrypted

## Convert to pycrypto format

- python, + regenerate pubkey and address

## Sign a message with the card

- 
