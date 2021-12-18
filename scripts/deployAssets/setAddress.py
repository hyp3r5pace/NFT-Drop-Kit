import subprocess
import os
import json

def main():
    """
    Set the currently used wallet address to the asset JSON data
    """
    warning = '\033[91m'

    # get the list of json file in assets directory
    fileList = os.listdir('assets')
    jsonList = []
    for file in fileList:
        if file.endswith('.json'):
            jsonList.append(file)
    
    # get the currently used address
    try:
        with open('.wallet', 'r') as f:
            walletData = f.read()
    except:
        print(f'{warning}ERROR: Reading from file .wallet')
        exit(1)
    
    walletAddress = walletData.split('\n')[1][8:]

    # set the wallet address to the asset json files
    for file in jsonList:
        try:
            with open('assets/'+file, 'r') as f:
                assetData = json.load(f)
        except:
            print(f'{warning}ERROR: Reading data from assets/{file}')
            exit(1)
        
        assetData['properties']['creators'][0]['address'] = walletAddress
        data = json.dumps(assetData, indent=4)
        try:
            with open('assets/'+file, 'w') as f:
                f.write(data)
        except:
            print(f'{warning}ERROR: Writing to {file}')
            exit(1)
    
        
