import os
import subprocess

def main():
    """Delete .cache folder and print some information for user
       for further use
    """
    # delete the .cache folder (Still under consideration -- might add in future but not now)
    # this is because metaplex reads the candy machine id from .cache to set the drop  date

    with open('.path', 'r') as f:
       path = f.read()
   
    print('To use solana CLI, run this command in the command line first')
    print(f'PATH={path}:$PATH')

if __name__ == "__main__":
   main()