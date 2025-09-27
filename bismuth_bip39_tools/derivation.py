import hashlib
import warnings
from mnemonic import Mnemonic
from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.seeds import BIP39Seed
from hdwallet.derivations import BIP44Derivation
import base58
import ecdsa

BISMUTH_COIN_TYPE = 209

def check_mnemonic(mnemonic: str) -> str:
    """Checks and normalizes a mnemonic by removing extra spaces and ensuring proper format.
    
    Args:
        mnemonic: The BIP39 mnemonic to check and normalize.
        
    Returns:
        A normalized mnemonic string with single spaces between words and no leading/trailing whitespace.
        
    Raises:
        ValueError: If the mnemonic has an invalid word count or contains invalid BIP39 words.
    """
    # Check if normalization will be needed
    original_mnemonic = mnemonic
    normalized_mnemonic = " ".join(mnemonic.strip().split())
    
    # Issue a warning if normalization is needed (whitespace differences)
    if original_mnemonic != normalized_mnemonic:
        warnings.warn(f"Mnemonic contained extra whitespace and was normalized: '{original_mnemonic[:50]}...' -> '{normalized_mnemonic[:50]}...'", 
                      UserWarning, stacklevel=2)
    
    # Split the normalized mnemonic into words
    words = normalized_mnemonic.split()
    
    # Check if the word count is valid (12, 18, or 24 words)
    valid_counts = [12, 18, 24]
    if len(words) not in valid_counts:
        raise ValueError(f"Invalid mnemonic word count: {len(words)}. Valid counts are: {valid_counts}")
    
    # Create a Mnemonic instance to validate words
    mnemo = Mnemonic("english")
    
    # Check if all words are in the BIP39 word list
    english_word_list = set(mnemo.wordlist)
    invalid_words = [word for word in words if word not in english_word_list]
    
    if invalid_words:
        raise ValueError(f"Invalid BIP39 words found in mnemonic: {invalid_words}")
    
    return normalized_mnemonic

def mnemonic_to_seed(mnemonic: str, password: str = "") -> bytes:
    """Converts a BIP39 mnemonic to a seed.

    Args:
        mnemonic: The BIP39 mnemonic.
        password: The optional password.

    Returns:
        A byte string containing the seed.
    """
    # Normalize the mnemonic to handle potential whitespace issues
    normalized_mnemonic = check_mnemonic(mnemonic)
    mnemo = Mnemonic("english")
    return mnemo.to_seed(normalized_mnemonic, password)

def generate_bis1_address(private_key_hex: str, compressed=True):
    """
    Generate Bis1 address from private key

    Args:
        private_key_hex (str): 64-character hex private key
        compressed (bool): Use compressed public key format (True=standard)

    Returns:
        str: Bis1 address
    """
    # 1. Create ECDSA private key from hex
    private_key_bytes = bytes.fromhex(private_key_hex)
    private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)

    # 2. Get public key
    public_key = private_key.get_verifying_key()

    # 3. Format public key (compressed or uncompressed)
    if compressed:
        # Compressed: 33 bytes (0x02/0x03 + x coordinate)
        public_key_bytes = public_key.to_string("compressed")
    else:
        # Uncompressed: 65 bytes (0x04 + x + y coordinates)
        public_key_bytes = b'\x04' + public_key.to_string()

    # 4. SHA-256 hash of public key
    sha256_hash = hashlib.sha256(public_key_bytes).digest()

    # 5. RIPEMD-160 hash of SHA-256 result
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

    # 6. Add Bismuth network prefix bytes
    network_prefix = b'\x4f\x54\x5b'  # Bismuth mainnet prefix
    prefixed_hash = network_prefix + ripemd160_hash

    # 7. Base58Check encode (includes checksum)
    bis_address = base58.b58encode_check(prefixed_hash).decode('utf-8')

    return bis_address

def derive_addresses(mnemonic: str, password: str = "", start: int = 0, count: int = 1) -> list[dict]:
    """Derives Bismuth addresses from a BIP39 mnemonic.

    Args:
        mnemonic: The BIP39 mnemonic.
        password: The optional password.
        count: The number of addresses to derive.

    Returns:
        A list of dictionaries, where each dictionary contains the address, private key, and public key.
    """
    # Normalize the mnemonic to handle potential whitespace issues
    normalized_mnemonic = check_mnemonic(mnemonic)
    seed_bytes = mnemonic_to_seed(normalized_mnemonic, password)

    # Initialize the HD wallet with seed
    hdwallet = HDWallet(cryptocurrency=Bitcoin)  # Use Bitcoin as a generic cryptocurrency for BIP39 derivation
    hdwallet.from_seed(seed=BIP39Seed(seed_bytes))

    addresses = []
    for i in range(count):
        num_path = start + i
        path = f"m/44'/{BISMUTH_COIN_TYPE}'/0'/0/{num_path}"
        # Parse the derivation path components for BIP44
        # Format: m/44'/coin_type'/account'/change/address_index
        # For our case: m/44'/209'/0'/0/i
        derivation = BIP44Derivation(
            coin_type=BISMUTH_COIN_TYPE,
            account=0,
            change=0,
            address=num_path
        )
        # Update HD wallet with the derivation
        hdwallet.from_derivation(derivation=derivation)
        
        private_key_hex = hdwallet.private_key()
        address = generate_bis1_address(private_key_hex, compressed=True)
        
        # Get the public key by deriving it from the private key using ECDSA
        private_key_bytes = bytes.fromhex(private_key_hex)
        private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()
        public_key_bytes = public_key.to_string("compressed")
        public_key_hex = public_key_bytes.hex()
        
        addresses.append({
            "address": address,
            "private_key": private_key_hex,
            "public_key": public_key_hex,
            "derivation_path": path
        })

    return addresses
