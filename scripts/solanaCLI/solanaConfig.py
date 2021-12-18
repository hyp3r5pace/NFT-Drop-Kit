import os
import subprocess

def main():
    with open('.path', 'r') as f:
        path = f.read()
    

    # executing the solana CLI config commands
    # set the solana CLI chain to devnet chain
    print('\nSetting up the solana CLI config...\n')
    output = subprocess.Popen([path+'/solana', 'config', 'set', '--url', 'https://api.devnet.solana.com'], stdout=subprocess.PIPE)
    output.communicate()
    output = subprocess.Popen([path+'/solana', 'config', 'get'], stdout=subprocess.PIPE)
    print(output.communicate()[0].decode('utf-8'))

if __name__ == "__main__":
    main()
