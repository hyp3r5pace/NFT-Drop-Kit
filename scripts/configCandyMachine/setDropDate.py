from posixpath import expanduser
import subprocess
import os

def main():
    """Set the drop date on the deployed candy machine
    """
    warning = '\033[91m'
    home = os.path.expanduser("~")
    metaplexCLI = "/metaplex-foundation/metaplex/js/packages/cli/src/candy-machine-cli.ts"

    print("Enter the drop date: ")
    try:
        day = int(input("Enter day: "))
    except:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    """
    Only checking the day to be between 0 and 32 (not inclusive) (not a strict checking)
    Assuming other strict constraints are handled by metaplex.
    If problem arises, might implement strict check
    """
    if day < 0 and day > 31:
        print(f'{warning}ERROR: Invalid input')

    month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    try:
        monthCode = int(input("Enter the month number like 1 for Jan, 2 for Feb etc: \n"))
    except:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    if not month.get(monthCode):
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    try:
        year = int(input("Enter year: "))
    except:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    if year < 0:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    try:
        hour = int(input("Enter hour in 24 hour format: "))
    except:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    if hour < 0 and hour > 23:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    try:
        minute = int(input("Enter minute: "))
    except:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    if minute < 0 and minute > 59:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    try:
        seconds = int(input("Enter seconds: "))
    except:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    if seconds < 0 and seconds > 59:
        print(f'{warning}ERROR: Invalid input')
        exit(1)
    
    try:
        setDropDate = subprocess.run(['ts-node', home+metaplexCLI, 'update_candy_machine', '--date', f'{day} {month.get(monthCode)} {year} {hour}:{minute}:{seconds} GMT',
                                 '--env', 'devnet', '--keypair', home+'/.config/solana/devnet.json'])
    except:
        print(f'{warning}ERROR: Failed setting drop date')

    print('✔️', 'Drop date set')
    


if __name__ == "__main__":
    main()