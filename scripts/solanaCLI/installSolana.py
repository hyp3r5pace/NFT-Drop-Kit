import subprocess
import requests
import os

def main():
    # install solana CLI
    try:
        # read the solana CLI bin path from .path file
        with open('.path', 'r') as f:
            path = f.read()
        data = subprocess.Popen([path+'/solana', '--version'], stdout=subprocess.PIPE)
        output = data.communicate()[0].decode('utf-8')
        if output.startswith('solana-cli'):
            print('✔️', 'Solana CLI installed --- Version {}'.format(output.split(' ')[1]))
    except:
        print('❌', 'Solana CLI not installed')
        print('Installing Solana CLI...')
        # url to the install bash sript
        url = "https://release.solana.com/stable/install"
        # downloading the install bash script
        res = requests.get(url, allow_redirects=True)
        with open('solana.sh', 'w') as f:
            f.write(res.content.decode('utf-8'))
        # creating a executable bash script
        with open('solana.sh', 'r') as f, open('solana', 'w') as r:
            r.write('#!/bin/sh' + '\n')
            for line in f:
                r.write(line)
        
        os.chmod('solana', 0b111101101)
        output = subprocess.Popen(['./solana'], stdout=subprocess.PIPE)
        path_command = output.communicate()[0].decode('utf-8').split('\n')[3].strip()
        path = path_command.split('=')[1].split(':')[0][1:]
        # for the first time installation, writing the path to solana CLI bin .path file
        with open('.path', 'w') as f:
            f.write(path)
        
        # delete the solana CLI installation files
        os.remove('solana')
        os.remove('solana.sh') 

        output = subprocess.Popen([path+'/solana', '--version'], stdout=subprocess.PIPE)
        version = output.communicate()[0].decode('utf-8').strip().split(' ')[1]
        print('✔️', 'Solana CLI --- version {} installation complete'.format(version)) 


if __name__ == "__main__":
    main()