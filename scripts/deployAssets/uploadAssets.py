import subprocess
import os

def main():
    """Upload the assets in assets folder to arweave,
       a decentralized storage network
    """

    home = os.path.expanduser("~")

    metaplexCLI = "/metaplex-foundation/metaplex/js/packages/cli/src/candy-machine-cli.ts"
    uploadAssets = subprocess.run(['ts-node', home+metaplexCLI, 'upload', './assets', '--env', 'devnet', '--keypair',
                                  home+'/.config/solana/devnet.json'])
    
    print("Verifying upload...\n")
    verifyUpload = subprocess.run(['ts-node', home+metaplexCLI, 'verify', '--keypair', home+'/.config/solana/devnet.json'])
   
    print('✔️', 'Assets upload complete')
    