# import threading
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional
# from  etherscan import Etherscan
import requests
import json
from termcolor import colored, cprint
import logging, coloredlogs
from multiprocessing import Process
# import time
# import os

ETHAPI = 'https://etherscan.io/register Sign up and get API Key and Paste here'
BSCAPI = 'https://bscscan.com/register Sign up and get API Key and Paste here'


# Fixed Logs.
logging.basicConfig(handlers=[logging.FileHandler(filename="ErrorDump.log", 
                                                  encoding='utf-8', mode='a+')],
                                                  format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                                                  datefmt="%F %A %T", 
                                                  level=logging.WARNING)


def subforce1():

    while True:    
        MNEMONIC: str = generate_mnemonic(language="english", strength=128)
        PASSPHRASE: Optional[str] = None  # "meherett"
        bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        bip44_hdwallet.from_mnemonic(
            mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
        )
        bip44_hdwallet.clean_derivation()
        bip44_derivation: BIP44Derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet, account=0, change=False, address=0)
        bip44_hdwallet.from_path(path=bip44_derivation)

        me = bip44_hdwallet.mnemonic()
        addr = bip44_hdwallet.address()

        # #ETH
        try:
            eth =requests.get(f'https://api.etherscan.io/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={ETHAPI}', timeout=5000.0)
        except requests.exceptions.RequestException as err:
            print(colored("Request Error" , color="red"))
            logging.warning(err)
        
        
        ethJson =eth.json()
        dumpETHJson = json.dumps(ethJson)

        loadETHJson = json.loads(dumpETHJson)
        ethTransaction = loadETHJson["status"]
        print(colored("ETH" , color="blue"))
        print(ethTransaction)
        if int(ethTransaction) >0:
            print(colored(f"Has transaction history {me} {addr}", color="green"))
            with open("valid.txt", "a") as ethWallets:
                    ethWallets.write("\nWallet: " + me + " ETH CHAIN " + addr)
        else:
            print(colored(f"{ethTransaction} {me} {addr}", color="yellow"))
            with open("empty.txt", "a") as ethWallets:
                    ethWallets.write("\nWallet: " + me + " ETH CHAIN " + addr)

        #BSC
        try:
            bsc =requests.get(f'https://api.bscscan.com/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={BSCAPI}', timeout=5000.0)
        except requests.exceptions.RequestException as err:
            print(colored("Requests Error" , color="red"))
            logging.warning(err)    
        
        bscJson =bsc.json()
        dumpBSCJson = json.dumps(bscJson)

        loadBSCJson = json.loads(dumpBSCJson)
        bscTransaction = loadBSCJson["status"]
        print(colored("BSC" , color="blue"))
        print(bscTransaction)
        if int(bscTransaction) >0:
            print(colored(f"Has transaction history {me} {addr}", color="green"))
            with open("valid.txt", "a") as bscWallets:
                    bscWallets.write("\nWallet: " + me + " BSC CHAIN " + addr)
        else:
            print(colored(f"{bscTransaction} {me} {addr}", color="yellow"))
            with open("empty.txt", "a") as ethWallets:
                    ethWallets.write("\nWallet: " + me + " BSC CHAIN " + addr)



        bip44_hdwallet.clean_derivation()

def mainforce():
    print("Starting multiprocessing")
    p1 = Process(target=subforce1)
    p2 = Process(target=subforce1)
    p3 = Process(target=subforce1)
    p4 = Process(target=subforce1)


    p1.start()
    p2.start()
    p3.start()
    p4.start()

    
    print("Multiprocess started")
    
if __name__ == '__main__' :
    mainforce() 
