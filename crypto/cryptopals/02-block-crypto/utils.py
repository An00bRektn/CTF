def pkcs7_pad(plaintext: bytes, block_size=16):
    space = block_size - (len(plaintext) % block_size)
    return plaintext + (space * bytes([space]))

def unpad(plaintext: bytes, block_size=16):
    if len(plaintext) % block_size != 0:
        raise ValueError("No padding found")
    if not _is_valid_padding(plaintext):
        raise ValueError("Invalid padding")

    return plaintext[:-plaintext[-1]]

def _is_valid_padding(plaintext: bytes):
    pad_byte = plaintext[-1]

    return plaintext[-pad_byte:] == bytes([pad_byte]) * pad_byte