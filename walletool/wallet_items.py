# -- encoding: UTF-8 --
import socket
from binascii import hexlify

from walletool.bc_data_stream import BCDataStream
from walletool.utils import privkey_to_secret, secret_to_asecret, public_key_to_bc_address


def parse_TxIn(vds):
    d = {}
    d['prevout_hash'] = vds.read_bytes(32)
    d['prevout_n'] = vds.read_uint32()
    d['scriptSig'] = vds.read_bytes(vds.read_compact_size())
    d['sequence'] = vds.read_uint32()
    return d


def parse_TxOut(vds):
    d = {}
    d['value'] = vds.read_int64() / 1e8
    d['scriptPubKey'] = vds.read_bytes(vds.read_compact_size())
    return d


def inversetxid(txid):
    txid = hexlify(txid).decode()
    if len(txid) != 64:
        raise ValueError('txid %r length != 64' % txid)
    new_txid = ""
    for i in range(32):
        new_txid += txid[62 - 2 * i]
        new_txid += txid[62 - 2 * i + 1]
    return new_txid


def parse_CAddress(vds):
    d = {'ip': '0.0.0.0', 'port': 0, 'nTime': 0}
    try:
        d['nVersion'] = vds.read_int32()
        d['nTime'] = vds.read_uint32()
        d['nServices'] = vds.read_uint64()
        d['pchReserved'] = vds.read_bytes(12)
        d['ip'] = socket.inet_ntoa(vds.read_bytes(4))
        d['port'] = vds.read_uint16()
    except:
        pass
    return d


def parse_BlockLocator(vds):
    d = {'hashes': []}
    nHashes = vds.read_compact_size()
    for i in range(nHashes):
        d['hashes'].append(vds.read_bytes(32))
    return d


def parse_setting(setting, vds):
    if setting[0] == "f":  # flag (boolean) settings
        return str(vds.read_boolean())
    elif setting[0:4] == "addr":  # CAddress
        return parse_CAddress(vds)
    elif setting == "nTransactionFee":
        return vds.read_int64()
    elif setting == "nLimitProcessors":
        return vds.read_int32()
    return {'unknown': vds}


class WalletItem:
    item_type = None

    def __init__(self, key, value, type, data):
        self.key = key
        self.value = value
        self.type = type
        self.data = data

    def __repr__(self):
        return '<%s item: %s>' % (self.type, self.data)

    @classmethod
    def parse(cls, key, value):
        kds = BCDataStream(key)
        vds = BCDataStream(value)
        type = kds.read_string().decode()
        data = {}

        # From Pywallet:

        if type == 'tx':
            data['tx_id'] = inversetxid(kds.read_bytes(32))
            start = vds.read_cursor
            data['version'] = vds.read_int32()
            n_vin = vds.read_compact_size()
            data['txIn'] = []
            for i in range(n_vin):
                data['txIn'].append(parse_TxIn(vds))
            n_vout = vds.read_compact_size()
            data['txOut'] = []
            for i in range(n_vout):
                data['txOut'].append(parse_TxOut(vds))
            data['lockTime'] = vds.read_uint32()
            data['tx'] = vds.input[start:vds.read_cursor]
            data['txv'] = value
            data['txk'] = key
        elif type == 'name':
            data['hash'] = kds.read_string()
            data['name'] = vds.read_string()
        elif type == 'version':
            data['version'] = vds.read_uint32()
        elif type == 'minversion':
            data['minversion'] = vds.read_uint32()
        elif type == 'setting':
            data['setting'] = kds.read_string()
            data['value'] = parse_setting(data['setting'].decode(), vds)
        elif type == 'key':
            data['public_key'] = kds.read_bytes(kds.read_compact_size())
            data['private_key'] = vds.read_bytes(vds.read_compact_size())
        elif type == 'wkey':
            data['public_key'] = kds.read_bytes(kds.read_compact_size())
            data['private_key'] = vds.read_bytes(vds.read_compact_size())
            data['created'] = vds.read_int64()
            data['expires'] = vds.read_int64()
            data['comment'] = vds.read_string()
        elif type == 'defaultkey':
            data['key'] = vds.read_bytes(vds.read_compact_size())
        elif type == 'pool':
            data['n'] = kds.read_int64()
            data['nVersion'] = vds.read_int32()
            data['nTime'] = vds.read_int64()
            data['public_key'] = vds.read_bytes(vds.read_compact_size())
        elif type == 'acc':
            data['account'] = kds.read_string()
            data['nVersion'] = vds.read_int32()
            data['public_key'] = vds.read_bytes(vds.read_compact_size())
        elif type == 'acentry':
            data['account'] = kds.read_string()
            data['n'] = kds.read_uint64()
            data['nVersion'] = vds.read_int32()
            data['nCreditDebit'] = vds.read_int64()
            data['nTime'] = vds.read_int64()
            data['otherAccount'] = vds.read_string()
            data['comment'] = vds.read_string()
        elif type == 'bestblock':
            data['nVersion'] = vds.read_int32()
            data.update(parse_BlockLocator(vds))
        elif type == 'ckey':
            data['public_key'] = kds.read_bytes(kds.read_compact_size())
            data['encrypted_private_key'] = vds.read_bytes(vds.read_compact_size())
        elif type == 'mkey':
            data['nID'] = kds.read_uint32()
            data['encrypted_key'] = vds.read_string()
            data['salt'] = vds.read_string()
            data['nDerivationMethod'] = vds.read_uint32()
            data['nDerivationIterations'] = vds.read_uint32()
            data['otherParams'] = vds.read_string()

        for item_cls in cls.__subclasses__():
            if item_cls.item_type == type:
                break
        else:
            item_cls = cls

        return item_cls(key, value, type, data)


class KeyWalletItem(WalletItem):
    item_type = 'key'

    def get_address(self, version):
        return public_key_to_bc_address(self.data['public_key'], version=version)

    def get_private_key(self, version):
        secret = privkey_to_secret(self.data['private_key'])
        asecret = secret_to_asecret(secret, version=version)
        return asecret


def parse_wallet_dict(wallet_dict):
    for key, value in wallet_dict.items():
        yield WalletItem.parse(key, value)
