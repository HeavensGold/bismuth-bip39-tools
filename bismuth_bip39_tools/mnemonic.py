from mnemonic import Mnemonic

def generate_mnemonic(strength: int = 128) -> str:
    """Generates a BIP39 mnemonic.

    Args:
        strength: The strength of the mnemonic in bits. Can be 128 or 256.

    Returns:
        A string containing the mnemonic.
    """
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=strength)
