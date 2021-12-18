import subprocess
import os

def main():
    """Deploy candy machine to devnet
    """
    warning = "\033[91m"
    home = os.path.expanduser("~")
    metaplexCLI = "/metaplex-foundation/metaplex/js/packages/cli/src/candy-machine-cli.ts"

    amount = float(input("Set the price of your NFTs (SOL): "))
    if amount < 0:
        print(f"{warning}ERROR: Invalid price")
        exit(1)
    
    # deploying candy machine using metaplex CLI command
    try:
        deployCandyMachine = subprocess.run(['ts-node', home+metaplexCLI, 'create_candy_machine', '--env', 'devnet', '--keypair',
                                        home+'/.config/solana/devnet.json', '-p', str(amount)], text=True, capture_output=True)
    except:
        print('❌', 'Deployment of candy machine failed')
        exit(1)
    
    # store the candy machine pubkey in file
    candyMachinePK = deployCandyMachine.stdout.split(":")[2].strip()
    try:
        with open('.candyMachine', 'w') as f:
            f.write(candyMachinePK)
    except:
        print(f'{warning}ERROR: writing to file .candyMachine')
        exit(1)
    
    print('✔️', 'Candy machine deployment successful')  
    
    

