#!/usr/bin/env python3
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

"""
Generate cryptographic key pairs for GraphQL API transaction signing.

This script generates Ed25519 key pairs that are used to SIGN transactions
in the GraphQL API. These are NOT for API authentication - they're for
cryptographically signing transactions.

How it works:
1. Run this script to generate a matching public/private key pair
2. Use the keys in your GraphQL mutation payload
3. The server validates the transaction signature (not the key itself)
4. No server-side key registration needed - any valid key pair works!

The keys are used like this:
- signerPublicKey: Identifies who is creating/signing the transaction
- signerPrivateKey: Used to cryptographically sign the transaction
- recipientPublicKey: Identifies who will receive the asset/tokens
"""

from collections import namedtuple
from cryptoconditions import crypto
import json

def generate_keypair(seed=None):
    """Generate a cryptographic key pair (same implementation as resdb_driver.crypto)."""
    CryptoKeypair = namedtuple("CryptoKeypair", ("private_key", "public_key"))
    return CryptoKeypair(*(k.decode() for k in crypto.ed25519_generate_key_pair(seed)))

def main():
    print("=" * 60)
    print("Generate Keys for GraphQL API")
    print("=" * 60)
    print()
    
    # Generate a key pair
    keypair = generate_keypair()
    
    print("✅ Key pair generated successfully!")
    print()
    print("Public Key (signerPublicKey / recipientPublicKey):")
    print(f"  {keypair.public_key}")
    print()
    print("Private Key (signerPrivateKey):")
    print(f"  {keypair.private_key}")
    print()
    print("=" * 60)
    print("Usage in GraphQL mutation:")
    print("=" * 60)
    print()
    print("Use these keys in your postTransaction mutation:")
    print()
    print(json.dumps({
        "operation": "CREATE",
        "signerPublicKey": keypair.public_key,
        "signerPrivateKey": keypair.private_key,
        "recipientPublicKey": keypair.public_key,  # Can be different
        "amount": 1,
        "asset": {
            "data": {
                "example": "test"
            }
        }
    }, indent=2))
    print()
    print("=" * 60)
    print("⚠️  IMPORTANT: Keep the private key secure!")
    print("=" * 60)

if __name__ == "__main__":
    main()
