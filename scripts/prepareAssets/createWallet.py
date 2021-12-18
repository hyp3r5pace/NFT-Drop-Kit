from re import sub
import subprocess
import os
import json
import stat

def main():
    """ Create the wallet which will be used to deploying candy machine
        key-pair values of this wallet will be stored in a hidden file for later use
    """
    warning = '\033[91m'
    # fetch the path to solana cli bin folder
    with open('.path', 'r') as f:
        path = f.read()
    
    # absolute path to home directory
    home = os.path.expanduser("~")
    
    # check for file storing information regarding existing wallet
    if os.path.isfile('.wallet'):
        try:
            with open('.wallet', 'r') as f:
                wallet = f.read()
        except:
            print(f'{warning}ERROR: Reading from file .wallet')
            exit(1)
        if wallet == "":
            warning = '\033[91m'
            print(f'{warning}ERROR: .wallet file is empty')
            exit(1)
        wallet = wallet.split('\n')
        try:
            address = wallet[1][8:]
        except:
            print(f'{warning}ERROR: ADDRESS filed is empty in .wallet')
            exit(1)
        print(f'Found a wallet with address: {address}')
        print(f'Do you want to deploy nft with this address?')
        print(f'No will lead to generation of new address')
        res = input('Press Y (for yes) or N (for no): ')

        if res.lower() == 'n':
            try:
                walletGenerate = subprocess.run([path+'/solana-keygen', 'new', '--outfile', home+'/.config/solana/devnet.json', '--force'], 
                                                input=b'')
            except:
                print('❌','Solana wallet generation failed')
                exit(1)

            # set it new keypair as default key pair
            try:
                setKeyPair = subprocess.run([path+'/solana', 'config', 'set', '--keypair', home+'/.config/solana/devnet.json'])
            except:
                print(f'{warning}ERROR: Failed setting new keypair as default')

            # reading the private key of the new wallet created
            try:
                with open(home+'/.config/solana/devnet.json', 'r') as f:
                    privKey = json.load(f)
            except:
                print(f'{warning}ERROR: Reading data from file {home}/.config/solana/devnet.json')
                exit(1)

            # read new wallet address and write it to .wallet file
            try:
                walletAddress = subprocess.run([path+'/solana', 'address'], capture_output=True, text=True)
                address = walletAddress.stdout[:-1]
            except:
                print(f'{warning}ERROR: executing solana address command')
                exit(1)
            
            # write private key and wallet address to .wallet
            try:
                with open('.wallet', 'w') as f:
                    f.write('PRIVKEY='+','.join(list(map(str, privKey)))+'\n'+'ADDRESS='+address)
            except:
                print(f'{warning}ERROR: writing to .wallet file')
                exit(1)
            
            print('✔️', f'New wallet generated with address: {address}')
        
        elif res.lower() == 'y':
            privKey = wallet[0].strip()[8:]
            privKey = privKey.split(',')

            try:
                with open(home+'/.config/solana/devnet.json', 'w') as f:
                    json.dump(list(map(int, privKey)), f)    
            except:
                print(f'{warning}ERROR: writing data to file {home}/.config/solana/devnet.json')
                exit(1)
            
            # set it new keypair as default key pair
            try:
                setKeyPair = subprocess.run([path+'/solana', 'config', 'set', '--keypair', home+'/.config/solana/devnet.json'])
            except:
                print(f'{warning}ERROR: Failed setting new keypair as default')
        else:
            print(f'{warning}INVALID INPUT!!')
            exit(1)
    
    else:
        # if .wallet file is missing --> create a new wallet
        # if user deleted the wallet by accident, just recreate the .wallet and fill the info 
        try:
            walletGenerate = subprocess.run([path+'/solana-keygen', 'new', '--outfile', home+'/.config/solana/devnet.json', '--force'], 
                                            input=b'')
        except:
            print('❌','Solana wallet generation failed')
            exit(1)
        
        # set it new keypair as default key pair
        try:
            setKeyPair = subprocess.run([path+'/solana', 'config', 'set', '--keypair', home+'/.config/solana/devnet.json'])
        except:
            print(f'{warning}ERROR: Failed setting new keypair as default')
        
        # set it new keypair as default key pair
        try:
            setKeyPair = subprocess.run([path+'/solana', 'config', 'set', '--keypair', home+'/.config/solana/devnet.json'])
        except:
            print(f'{warning}ERROR: Failed setting new keypair as default')

        # reading the private key of the new wallet created
        try:
            with open(home+'/.config/solana/devnet.json', 'r') as f:
                privKey = json.load(f)
        except:
            print(f'{warning}ERROR: Reading data from file {home}/.config/solana/devnet.json')
            exit(1)

        # read new wallet address and write it to .wallet file
        try:
            walletAddress = subprocess.run([path+'/solana', 'address'], capture_output=True, text=True)
            address = walletAddress.stdout[:-1]
        except:
            print(f'{warning}ERROR: executing solana address command')
            exit(1)
            
        # write private key and wallet address to .wallet
        try:
            with open('.wallet', 'w') as f:
                f.write('PRIVKEY='+','.join(list(map(str, privKey)))+'\n'+'ADDRESS='+address)
        except:
            print(f'{warning}ERROR: writing to .wallet file')
            exit(1)
            
        print('✔️', f'New wallet generated with address: {address}')

        


            
    
    