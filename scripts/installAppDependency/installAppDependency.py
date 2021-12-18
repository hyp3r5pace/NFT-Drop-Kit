import os
import subprocess

def main():
    """Spin up the app in the local host
    """
    warning = "\033[91m"
    
    # installing dependency
    try:
        dependencyInstall = subprocess.run(['npm', 'install', 'app/'])
    except:
        print(f'{warning}ERROR: Installing dependency')
        exit(1)

if __name__ == "__main__":
    main()
