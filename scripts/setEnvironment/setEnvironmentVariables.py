import subprocess
import os
import json

def main():
    """Set the enivronment variables with candy machine pubic key, 
       wallet address and other info
    """
    warning = "\033[91m"
    # get environment variable data from .cache directory
    with open('.cache/devnet-temp', 'r') as f:
        data = json.load(f)
    
    candyMachineConfig = data["program"]["config"]
    candyMachineId = data['candyMachineAddress']
    TreasuryAddress = data["authority"]
    solanaNetwork = "devnet"
    solanaRPCHost = "https://explorer-api.devnet.solana.com"

    envVariables = f"REACT_APP_CANDY_MACHINE_CONFIG={candyMachineConfig}\n" + f"REACT_APP_CANDY_MACHINE_ID={candyMachineId}\n"
    envVariables += f"REACT_APP_TREASURY_ADDRESS={TreasuryAddress}\n" + f"REACT_APP_SOLANA_NETWORK={solanaNetwork}\n"
    envVariables += f"REACT_APP_SOLANA_RPC_HOST={solanaRPCHost}\n"

    try:
        with open('app/.env', 'w') as f:
            f.write(envVariables)
    except:
        print(f"{warning}ERROR: Writing to app/.env file")
        exit(0)
    
    print('✔️', 'App enviroment variables set')

if __name__ == "__main__":
    main()    
