# Walletool - Read wallet.dat files

## Access [Bitcoin-Core](https://bitcoin.org/en/bitcoin-core/) and [Litecoin-Core](https://litecoin.org/) wallets __addresses__ and __private keys__

-----------------------------------------------------------

## Requirements

* Install python 3.6+
* Install `requirements.py` by running:
  * `$pip install -r requirements.txt`
* Your wallet must be __UNENCRYPTED__!

## Installation

### _Linux - Install BerkeleyDB_

#### [Berkeley source installation](https://www.linuxfromscratch.org/blfs/view/svn/server/db.html)

1. [Download Berkely to compile](https://anduin.linuxfromscratch.org/BLFS/bdb/db-5.3.28.tar.gz)

2. First apply a fix so that this will compile with current versions of g++:

    `$ sed -i 's/\(__atomic_compare_exchange\)/\1_db/' src/dbinc/atomic.h`

3. Install Berkeley DB by running the following commands:

    `cd build_unix                        &&
    ../dist/configure --prefix=/usr      \
                      --enable-compat185 \
                      --enable-dbm       \
                      --disable-static   \
                      --enable-cxx       &&
    make`

4. Now, as the __root__ user:

    `make docdir=/usr/share/doc/db-5.3.28 install &&
        chown -v -R root:root                        \
              /usr/bin/db_*                          \
              /usr/include/db{,_185,_cxx}.h          \
              /usr/lib/libdb*.{so,la}                \
              /usr/share/doc/db-5.3.28`

## Wallet location

### _Linux_

* `~/.bitcoin/wallets/[WALLET_NAME]/wallet.dat`

-----------------------------------------------------------

### Types / CoinType

* For Bitcoin, run `python3 main.py -d WALLET_NAME.dat -v 0`
* For Litecoin, run `python3 main.py -d WALLET_NAME.dat -v 48`

-----------------------------------------------------------

### _Output_

Print / Log - Wallet addresses and private keys

<!-- Install berkely DB
https://www.linuxfromscratch.org/blfs/view/svn/server/db.html

Alt: 
  `$ sudo apt install libdb-dev && pip install bsddb3` -->