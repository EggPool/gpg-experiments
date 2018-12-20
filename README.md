# GPG Experiments

PGP/GPG Experiments with RSA

Highly experimental, use at your own risks and only if you understand what you're doing.

## Pre-requisites

- openpgp compatible token, like a nitrokey or yubikey or a gnuk token  
  See https://github.com/EggPool/gpg-experiments/blob/master/Tokens.md
- Done on Ubuntu, same on other linuxes
- GPG v1
- GPG v2
- Monkeysphere `sudo apt install monkeysphere`
- Python3
- air gap secure machine, like a tail distro if you want to use the keys IRL

`sudo apt install gnupg2 pcscd scdaemon pcsc-tools`

### OpenSc
Ubuntu 16 comes with opensc 0.15, needs 0.16 mini.  
Use ubuntu 18 or compile from source, see https://github.com/OpenSC/OpenSC/wiki/Compiling-and-Installing-on-Unix-flavors

Check version with `opensc-tool -i`, needs 0.16.0 min, current git is 0.19.0

Check opensc works with `opensc-tool -a`, should list at least one card reader and one card, give no error.

If needed, see
https://www.nitrokey.com/documentation/frequently-asked-questions-faq#which-gnupg,-opensc-and-libccid-versions-are-required
https://www.nitrokey.com/documentation/frequently-asked-questions-faq#latest-device-driver-missing-on-older-linux-distribution


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

- export gpg2 and import into gpg with passphrase 
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

> TODO: regenerated pubkey does not seem the same (under b64 form) than the one converted above.
Double check and see what gives export/import from python.

## Sign a message with the card

### GPG Signatures

- `gpg2 --detach-sign  test.txt` creates a test.sig (bin)
- `gpg2 --armor --detach-sign  test.txt` creates a test.asc
- `gpg2 --armor --clearsign test.txt` creates a test.asc with raw text as input, does not compress first

Those are of no use for Bismuth, since the GPG protocol append more bytes, including timestamp, to the buffer to be hashed and signed.

> https://tools.ietf.org/html/rfc4880#section-5.2.1  
"The concatenation of the data to be signed, the signature type, and creation time from the Signature packet  
(5 additional octets) is hashed.  
The resulting hash value is used in the signature algorithm."


### Raw PKCS1_15 Signatures

Prepare hash to be signed

- `openssl sha1 -binary ./test > test.sha1`  # Binary hash (same as Pytyhon SHA)
- `pkcs15-crypt --key 01 --sign --pkcs1 --sha-1 --input test.sha1 --output test.pk.sig`  
  01 is the first key of the device, the signature one.  
  --pkcs1 padds the input buffer
  
  test.pk.sig contains the (bin) signature, matches the python one.

## Useful related info

* https://htmlpreview.github.io/?https://github.com/OpenSC/OpenSC/blob/master/doc/tools/tools.html#pkcs15-crypt
* js packet decoder to get binary sig https://cirw.in/gpg-decoder
* https://github.com/SecurityInnovation/PGPy  
* pgpdump `gpg2 --export YOUR_KEY_ID | pgpdump -i`(needs apt install pgpdump)  
* To understand the output of pgpdump (and the structure of OpenPGP messages), see https://tools.ietf.org/html/rfc4880
* https://stackoverflow.com/questions/19305030/how-to-make-an-gnupg-key-compatible-with-pycrypto  
  (see saving PEM with passphrase)
* More conversions http://www.sysmic.org/dotclear/index.php?post/2010/03/24/Convert-keys-betweens-GnuPG%2C-OpenSsh-and-OpenSSL
