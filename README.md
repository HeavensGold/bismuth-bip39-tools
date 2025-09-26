# Bismuth BIP39 Tools

A Python library for generating BIP39 mnemonics and deriving Bismuth addresses.

## Installation

### For users
```bash
pip install git+https://github.com/HeavensGold/bismuth-bip39-tools.git
```

### For development
```bash
# Clone the repository
git clone <repository-url>
cd bismuth-bip39-tools

# Install in development mode
pip install -e .
```

## Usage

### Generate a mnemonic

```python
from bismuth_bip39_tools.mnemonic import generate_mnemonic

# Generate a 12-word mnemonic
mnemonic = generate_mnemonic(128)
print(mnemonic)

# Generate a 24-word mnemonic
mnemonic = generate_mnemonic(256)
print(mnemonic)
```

### Derive addresses

```python
from bismuth_bip39_tools.derivation import derive_addresses

mnemonic = """YOUR MNEMONIC HERE"""
addresses = derive_addresses(mnemonic, count=5)

for address in addresses:
    print(f"Address: {address['address']}")
    print(f"Private Key: {address['private_key']}")
    print(f"Public Key: {address['public_key']}")
    print("---")
```
