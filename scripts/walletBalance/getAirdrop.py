import subprocess
import os

def main():
    """Check balance, and ask if user want airdrop
       if yes, get airdrop
    """
    warning = "\033[91m"
    with open('.path', 'r') as f:
        path = f.read()
    
    while True:
        # check for wallet balance on devnet
        try:
            checkBalance = subprocess.run([path+'/solana', 'balance'], text=True, capture_output=True)
            print(f'Wallet Balance: {checkBalance.stdout}')
        except:
            print(f'{warning}ERROR: Fetching balance of wallet')
            exit(1)

        res = input('Do you want airdrop? (Y/N): ')

        if res.lower() == 'y':
            amount = float(input("Enter the amount of SOL: "))
            if amount <= 2 and amount > 0:
                airdrop = subprocess.run([path+'/solana', 'airdrop', str(amount)], text=True, capture_output=True)
                print('✔️',f'Airdrop of {amount} successful')
            elif amount > 2:
                quotient = amount//2
                remainder = amount - (quotient*2)
                for i in range(int(quotient)):
                    airdrop = subprocess.run([path+'/solana', 'airdrop', '2'], text=True, capture_output=True)
                if remainder > 0:
                    airdrop = subprocess.run([path+'/solana', 'airdrop', str(remainder)], text=True, capture_output=True)
                print(f'Airdrop of {amount} successful')
            else:
                print(f'{warning}INVALID AMOUNT')
                exit(1)       
        elif res.lower() == 'n':
            break
        else:
            continue
