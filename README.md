# GPG Experiments

PGP/GPG Experiments with RSA

Highly experimental, use at your own risks and only if you understand what you're doing.

## Pre-requisites

- openpgp compatible token, like a nitrokey or yubikey or a gnuk token  
  See Tokens.md
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
- Select `4` "Set the reset code", set pin code. Then `3` "Admin PIN", then `1` "Change PIN"

Ref: http://www.fsij.org/doc-gnuk/gnuk-passphrase-setting.html#set-up-pw1-pw3-and-reset-code

## Create a signature key

- `gpg2 --full-gen-key --expert`
- Choice 4 RSA, sig only
- 4096 bits
- 0 (do not expire)
- set a passphrase
- wait for entropy and key generation
- This process may take a long time depending on how active your system is and the keysize you selected.  
 To generate additional entropy more easily, you can use haveged: https://www.digitalocean.com/community/tutorials/how-to-setup-additional-entropy-for-cloud-servers-using-haveged

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

> **Warning**: This will *move* the key to the card, therefore delete it from the local keyring.  
You need to do the backup first.

- `gpg2 --edit-key YOUR_KEY_ID`
- `keytocard`
- Select `1`: Signature key
- `save`

## Export the pubkey

Unarmored:  
`gpg2 --export YOUR_KEY_ID > your_key_id.public.bin`

Armored:  
`gpg2 --armor --export YOUR_KEY_ID > your_key_id.public.asc`

## Convert the privkey to .pem

In order to convert the key to pem format, we need a key exported without a passphrase.  
gpg2 does not allow that. So we use gpg as a temporary step.  
Pay attention to gpg/gpg2 in the commands!

- export gpg2 and import into gpg with hpassphrase 
  `gpg2 --export-secret-keys YOUR_KEY_ID| gpg --import`
- remove passphrase  
  `gpg --edit-key YOUR_KEY_ID`  
  `passwd` Enter temporary passphrase to unlock, then give new, empty passphrase, confirm empty passphrase.  
  `save`
- export unencrypted  
   `gpg --armor --export-secret-keys YOUR_KEY_ID > your_key_id.secret.clear.asc`
- now we can finally convert  
  `cat your_key_id.secret.clear.asc|openpgp2pem YOUR_KEY_ID > your_key_id.secret.pem`

## Convert to pycrypto format

You can now read from pycryptodome:

```
from Cryptodome.PublicKey import RSA

with open('your_key_id.secret.pem', 'rb') as f:
    key_secret = RSA.importKey(f.read())
```

Python script to regenerate pubkey and address, see pem_recover.py

## Sign a message with the card

- `gpg2 --detach-sign  test.txt` creates a test.sig (bin)
- `gpg2 --armor --detach-sign  test.txt` creates a test.asc

## TODO

Convert PGP signature to Pycrypto signature and compare outputs.

## Possible useful related info

* https://github.com/SecurityInnovation/PGPy  
* pgpdump `gpg2 --export YOUR_KEY_ID | pgpdump -i`(needs apt install pgpdump)  
* To understand the output of pgpdump (and the structure of OpenPGP messages), see https://tools.ietf.org/html/rfc4880
* https://stackoverflow.com/questions/19305030/how-to-make-an-gnupg-key-compatible-with-pycrypto  
  (see saving PEM with passphrase)
* More conversions http://www.sysmic.org/dotclear/index.php?post/2010/03/24/Convert-keys-betweens-GnuPG%2C-OpenSsh-and-OpenSSL
