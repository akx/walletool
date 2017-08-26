# -- encoding: UTF-8 --
import hashlib

b58_chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
b58_base = len(b58_chars)


def b58encode(v):
    """ encode v, which is a string of bytes, to base58.
    """

    long_value = 0
    for (i, c) in enumerate(v[::-1]):
        long_value += (256 ** i) * int(c)

    result = ''
    while long_value >= b58_base:
        div, mod = divmod(long_value, b58_base)
        result = b58_chars[mod] + result
        long_value = div
    result = b58_chars[long_value] + result

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in v:
        if c == 0:
            nPad += 1
        else:
            break

    return (b58_chars[0] * nPad) + result


def b58decode(v, length):
    """ decode v into a string of len bytes
    """
    long_value = 0
    for (i, c) in enumerate(v[::-1]):
        long_value += b58_chars.find(c) * (b58_base ** i)

    result = ''
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result = chr(mod) + result
        long_value = div
    result = chr(long_value) + result

    nPad = 0
    for c in v:
        if c == b58_chars[0]:
            nPad += 1
        else:
            break

    result = chr(0) * nPad + result
    if length is not None and len(result) != length:
        return None

    return result


def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def encode_base58_check(secret):
    hash = double_sha256(secret)
    return b58encode(secret + hash[0:4])


def privkey_to_secret(privkey):
    if len(privkey) == 279:
        return privkey[9:9 + 32]
    else:
        return privkey[8:8 + 32]


def secret_to_asecret(secret, version):
    prefix = (version + 128) & 255
    vchIn = bytes([prefix]) + secret
    return encode_base58_check(vchIn)


def hash_160(public_key):
    md = hashlib.new('ripemd160')
    md.update(hashlib.sha256(public_key).digest())
    return md.digest()


def public_key_to_bc_address(public_key, version):
    h160 = hash_160(public_key)
    return hash_160_to_bc_address(h160, version)


def hash_160_to_bc_address(h160, version):
    vh160 = bytes([int(version)]) + h160
    h = double_sha256(vh160)
    addr = vh160 + h[0:4]
    return b58encode(addr)


def bc_address_to_hash_160(addr):
    bytes = b58decode(addr, 25)
    return bytes[1:21]
