import subprocess
import os

def main():
    # path to home directory
    home = os.path.expanduser("~")
    # check if metaplex git repo is already downloaded or not
    if not os.path.isdir(home+'/metaplex-foundation/metaplex'):
        print('❌', 'Metaplex CLI not installed')
        print('Installing Metaplex CLI...')
        # since the directory doesn't exist, download the git repo
        try:
            if not os.path.isfile('.metaplexConf'):
                raise Exception("Metaplex config file (.metaplexConf) not found")
        except:
            # unicode for coloring text on terminal
            warning = '\033[91m'
            print(f"{warning}ERROR:","Metaplex config file (.metaplexConf) not found")
            print("Please add the metaplex configuration file")
            print("If you have deleted the file accidentally,\nyou can download it from the project repo")
            print("CAUTION: Add the file to the root of this project directory")
            exit(1)
        
        try:
            with open('.metaplexConf', 'r') as f:
                repoInfo = f.read()
        except:
            warning = '\033[91m'
            print(f"{warning} ERROR: error reading .metaplexConf file")
            exit(1)
        
        version = repoInfo.split('\n')[1].strip().split('=')[1]
        repo = repoInfo.split('\n')[0].strip().split('=')[1]

        try:
            gitProcess = subprocess.Popen(['git', 'clone', '--branch', version, repo, home+'/metaplex-foundation/metaplex'])
            gitProcess.wait()
        except:
            warning = '\033[91m'
            print(f"{warning}ERROR: Cloning of {repo} failed")
            exit(1)

    path = home+"/metaplex-foundation/metaplex/"
    # create a child process to install dependency
    try:
        installDependency = subprocess.Popen(['yarn', 'install', '--cwd', path+'js/'])
        installDependency.wait()
    except:
        warning = '\033[91m'
        print(f'{warning}ERROR: yarn -- dependency install/upgrade failed')
        exit(1)
    
    checkVersion = subprocess.Popen(['ts-node', path+'js/packages/cli/src/candy-machine-cli.ts', '--version'], stdout=subprocess.PIPE)
    checkVersion.wait()
    print('✔️', 'Metaplex CLI installed --- Version {}'.format(checkVersion.communicate()[0].decode('utf-8')))

    
    