import os
from lit_core.lit_node_client import LitNodeClient
from lit_core.constants import AuthSigVersion

client = LitNodeClient()

async def init_lit():
    await client.connect()

def get_lit_auth_signature():
    # In a real-world scenario, this would be generated on the client-side
    # For demonstration purposes, we'll use a mock auth signature
    return {
        "sig": "0x2bdede6164f56a601fc17a8a78327d28b54e87cf3fa20373fca1d73b804566736d76efe2dd79a4627870a50e66e1a9050ca333b6f98d9415d8bca424980611ca1c",
        "derivedVia": "web3.eth.personal.sign",
        "signedMessage": "I am creating an account to use Lit Protocol at 2024-10-19T23:14:00.000Z",
        "address": "0x7C0f86E78dA2E1E568C6B89C7e2F3364eB11Dbc0",
    }

async def encrypt_content(content, access_control_conditions):
    auth_sig = get_lit_auth_signature()
    
    encrypted = await client.encrypt(
        {
            'dataToEncrypt': content,
            'chain': 'ethereum',
            'accessControlConditions': access_control_conditions,
            'authSig': auth_sig,
        }
    )
    
    return {
        'encrypted_content': encrypted['encryptedString'],
        'encrypted_symmetric_key': encrypted['encryptedSymmetricKey'],
    }

async def decrypt_content(encrypted_content, encrypted_symmetric_key, access_control_conditions):
    auth_sig = get_lit_auth_signature()
    
    decrypted = await client.decrypt(
        {
            'encryptedString': encrypted_content,
            'encryptedSymmetricKey': encrypted_symmetric_key,
            'chain': 'ethereum',
            'accessControlConditions': access_control_conditions,
            'authSig': auth_sig,
        }
    )
    
    return decrypted['decryptedString']

# Example access control condition
example_access_control_conditions = [
    {
        "contractAddress": "",
        "standardContractType": "",
        "chain": "ethereum",
        "method": "eth_getBalance",
        "parameters": [
            ":userAddress",
            "latest"
        ],
        "returnValueTest": {
            "comparator": ">=",
            "value": "1000000000000000000"  # 1 ETH
        }
    }
]
