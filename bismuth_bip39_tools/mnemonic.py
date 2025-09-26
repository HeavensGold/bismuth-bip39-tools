from mnemonic import Mnemonic

def generate_mnemonic(strength: int = 256) -> str:
    """Generates a BIP39 mnemonic.

    Args:
        strength: The strength of the mnemonic in bits. Can be 128 for 12 words or 256 for 24 words.

    Returns:
        A string containing the mnemonic.
    """
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=strength)
