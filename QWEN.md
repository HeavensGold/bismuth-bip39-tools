# Bismuth BIP39 Tools - Project Context

## Project Overview

This is a Python library for generating BIP39 mnemonics and deriving Bismuth addresses. The project provides tools to work with BIP39 (mnemonic code for generating deterministic keys) specifically tailored for the Bismuth cryptocurrency ecosystem.

**Main Purpose**: Generate BIP39 compliant mnemonics and derive Bismuth addresses (Bis1 format) from them using proper derivation paths.

**Architecture**: The project consists of a simple Python package with two main modules:
- `mnemonic.py`: Handles generation of BIP39 mnemonics
- `derivation.py`: Handles derivation of Bismuth addresses from mnemonics
- `example.py`: Demonstrates usage of the library

**Key Technologies**: 
- Python 3.6+
- `mnemonic` library for BIP39 mnemonic operations
- `hdwallet` for hierarchical deterministic wallet operations
- `ecdsa` for elliptic curve cryptography operations
- `base58` for Base58Check encoding

## Key Features

1. **Mnemonic Generation**: Generate 12-word (128-bit) or 24-word (256-bit) BIP39 mnemonics
2. **Bismuth Address Derivation**: Derive Bismuth addresses using BIP44 derivation path `m/44'/209'/0'/0/n`
3. **Key Information Extraction**: Retrieve private keys, public keys, and derivation paths for each address
4. **Bis1 Address Format**: Generate proper Bismuth addresses using RIPEMD-160 hashing and Base58Check encoding

## File Structure

```
bismuth_bip39_tools/
├── __init__.py          # Package initializer
├── mnemonic.py          # Mnemonic generation functionality
├── derivation.py        # Address derivation and key generation
└── __pycache__/         # Python cache files
```

## Key Functions

### mnemonic.py
- `generate_mnemonic(strength: int = 128) -> str`: Generates a BIP39 mnemonic with specified entropy (128 or 256 bits)

### derivation.py
- `mnemonic_to_seed(mnemonic: str, password: str = "") -> bytes`: Converts mnemonic to BIP39 seed
- `generate_bis1_address(private_key_hex: str) -> str`: Generates Bis1 address from private key
- `derive_addresses(mnemonic: str, password: str = "", count: int = 1) -> list[dict]`: Derives multiple Bismuth addresses from mnemonic

## Building and Running

### Installation
```bash
pip install bismuth-bip39-tools
```

### For development
```bash
# Clone the repository
git clone <repository-url>
cd bismuth-bip39-tools

# Install in development mode
pip install -e .
```

### Dependencies
- `mnemonic` - BIP39 mnemonic handling
- `hdwallet` - Hierarchical deterministic wallet operations  
- `base58check` - Base58Check encoding
- `ecdsa` - Elliptic curve digital signature algorithm

### Usage Examples

**Generate a mnemonic:**
```python
from bip39_tools.mnemonic import generate_mnemonic

# Generate a 12-word mnemonic
mnemonic = generate_mnemonic(128)
print(mnemonic)

# Generate a 24-word mnemonic
mnemonic = generate_mnemonic(256)
print(mnemonic)
```

**Derive addresses:**
```python
from bip39_tools.derivation import derive_addresses

mnemonic = "YOUR MNEMONIC HERE"
addresses = derive_addresses(mnemonic, count=5)

for address in addresses:
    print(f"Address: {address['address']}")
    print(f"Private Key: {address['private_key']}")
    print(f"Public Key: {address['public_key']}")
    print("---")
```

### Running the Example
Execute the example to see full functionality:
```bash
python example.py
```

## Development Conventions

- **BIP44 Path**: Uses `m/44'/209'/0'/0/n` where 209 is Bismuth's coin type
- **Address Format**: Generates Bis1 addresses using proper RIPEMD-160 + Base58Check encoding with Bismuth network prefix `\\x4f\\x54\\x5b`
- **Key Format**: Returns private keys as 64-character hex strings, public keys as compressed hex format
- **Return Structure**: Addresses are returned as dictionaries containing address, private key, public key, and derivation path

## Important Constants

- **BISMUTH_COIN_TYPE = 209**: The BIP44 coin type for Bismuth cryptocurrency
- **Network Prefix**: `\\x4f\\x54\\x5b` - Bismuth mainnet address prefix
- **Compression**: Uses compressed public keys (`0x02`/`0x03` format) by default

## Security Considerations

- Private keys are generated using proper cryptographic methods
- Mnemonic generation uses secure entropy sources
- All cryptographic operations follow BIP standards for deterministic key generation

## Testing

To run tests, use:
```bash
# TODO: Add specific test commands once test files are identified
```

## Project Context for AI Interactions

When working with this codebase:
- The library is specifically designed for Bismuth cryptocurrency addresses
- Follow BIP39, BIP44 standards for mnemonic and address generation
- Maintain consistency with Bis1 address format and network prefixes
- Preserve the existing API for generate_mnemonic and derive_addresses functions
- Keep the Bismuth coin type (209) constant for proper derivation paths
- Maintain backward compatibility with the dictionary return format from derive_addresses