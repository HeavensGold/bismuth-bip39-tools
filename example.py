from bismuth_bip39_tools.mnemonic import generate_mnemonic
from bismuth_bip39_tools.derivation import derive_addresses

def main():
    """
    This example demonstrates how to generate a BIP39 mnemonic and derive
    Bismuth addresses from it.
    """

    # 1. Generate a new 24-word mnemonic
    print("Generating a new 24-word mnemonic...")
    mnemonic = generate_mnemonic(256)
    print(f"  Mnemonic: {mnemonic}\n")

    # 2. Derive the first 5 addresses from the mnemonic
    print("Deriving the first 5 addresses from the mnemonic...")
    addresses = derive_addresses(mnemonic, count=5)

    # 3. Print the derived addresses and keys
    for i, address_data in enumerate(addresses):
        print(f"--- Address #{i+1} ---")
        print(f"  Address:     {address_data['address']}")
        print(f"  Private Key: {address_data['private_key']}")
        print(f"  Public Key:  {address_data['public_key']}")
        print(f"  Derivation Path: {address_data['derivation_path']}")
    print("")

if __name__ == "__main__":
    main()
