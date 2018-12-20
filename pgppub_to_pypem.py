"""
EggdraSyl - Bismuth Foundation

Read a PGP public key and converts to X.509 format (Bismuth .der, b64 encoded)
Also shows the matching BIS Address
"""

from Cryptodome.PublicKey import RSA
from pgpy import PGPKey, PGPKeyring
from hashlib import sha224

# Use either armored or binary key
# key, _ = PGPKey.from_file('DA3B9CAB.pub.asc')
key, _ = PGPKey.from_file('DA3B9CAB.pub.bin')

# print(key.key_size, key.key_algorithm, key.pubkey, key._key.__dict__, key._key.keymaterial.__dict__)

key_pub = RSA.construct((key._key.keymaterial.n, key._key.keymaterial.e), consistency_check=True)
key_public_export = key_pub.exportKey('PEM')

address = sha224(key_public_export).hexdigest()
print("Address", address)

with open('public.pem', 'wb') as f:
    f.write(key_public_export)
print("Saved to public.pem")

