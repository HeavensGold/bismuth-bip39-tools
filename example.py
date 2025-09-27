import json
import os
import warnings
from bismuth_bip39_tools.mnemonic import generate_mnemonic
from bismuth_bip39_tools.derivation import derive_addresses, check_mnemonic


def load_or_create_mnemonic():
    """
    Load mnemonic from wallet_hd.json file if it exists,
    otherwise generate a new one and save it to the file.
    """
    wallet_file = 'wallet_hd.json'
    
    if os.path.exists(wallet_file):
        print(f"Loading mnemonic from {wallet_file}...")
        try:
            with open(wallet_file, 'r') as f:
                data = json.load(f)
                if 'mnemonic' in data:
                    # Normalize and validate the mnemonic
                    try:
                        normalized_mnemonic = check_mnemonic(data['mnemonic'])
                        return normalized_mnemonic
                    except ValueError as e:
                        print(f"Error: Invalid mnemonic in {wallet_file}: {e}")
                        print("The mnemonic failed validation. Please fix the mnemonic in the file or delete it to generate a new one.")
                        exit(1)  # Exit the program with an error code
                else:
                    print(f"Warning: {wallet_file} does not contain a 'mnemonic' field. Generating a new one.")
        except json.JSONDecodeError:
            print(f"Error: {wallet_file} is not a valid JSON file. Generating a new mnemonic.")
        except Exception as e:
            print(f"Error reading {wallet_file}: {e}. Generating a new mnemonic.")
    
    # Generate a new 24-word mnemonic
    print("Generating a new 24-word mnemonic...")
    new_mnemonic = generate_mnemonic(256)
    
    # Save the new mnemonic to wallet_hd.json
    with open(wallet_file, 'w') as f:
        json.dump({'mnemonic': new_mnemonic}, f, indent=2)
    
    print(f"New mnemonic saved to {wallet_file}")
    return new_mnemonic


def main():
    """
    This example demonstrates how to generate a BIP39 mnemonic and derive
    Bismuth addresses from it. It first checks for wallet_hd.json and uses
    the mnemonic stored there if available, otherwise generates a new one.
    """
    
    # Load or create mnemonic
    mnemonic = load_or_create_mnemonic()
    # Ensure mnemonic is normalized (though it should already be from load_or_create_mnemonic)
    mnemonic = check_mnemonic(mnemonic)
    print(f"Mnemonic loaded: {mnemonic}\n")

    # Derive the first 5 addresses from the mnemonic
    print("Deriving the first 5 addresses from the mnemonic...")
    addresses = derive_addresses(mnemonic, count=5)

    # Print the derived addresses and keys
    for i, address_data in enumerate(addresses):
        print(f"--- Address #{i+1} ---")
        print(f"  Address:     {address_data['address']}")
        print(f"  Private Key: {address_data['private_key']}")
        print(f"  Public Key:  {address_data['public_key']}")
        print(f"  Derivation Path: {address_data['derivation_path']}")
    print("")


if __name__ == "__main__":
    main()
