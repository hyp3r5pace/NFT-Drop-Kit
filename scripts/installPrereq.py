import os
import subprocess
import re

def main():
    # running command to check if git is installed
    data = subprocess.Popen(['git', '--version'], stdout = subprocess.PIPE)
    output = data.communicate()[0].decode('utf-8')

    if output.startswith("git version"):
        version = output.strip().split(' ')[-1]
        print('✔️', "Git installed --- Version {}".format(version))
    else:
        print('❌', 'Git not installed')
        exit(1)

    # executing command to check if node is installed
    data = subprocess.Popen(['node', '-v'], stdout=subprocess.PIPE)
    output = data.communicate()[0].decode('utf-8')

    pattern = re.compile('v\d+\.\d+\.\d+')

    if pattern.search(output):
        print('✔️', "Node installed --- Version {}".format(output[1:].strip()))
    else:
        print('❌', "Node not installed")
        exit(1)

    # executing command to check if npm is installed
    data = subprocess.Popen(['npm', '-v'], stdout=subprocess.PIPE)
    output = data.communicate()[0].decode('utf-8')

    pattern = re.compile('\d+\.\d+\.\d+')

    if pattern.search(output):
        print('✔️', "npm installed --- Version {}".format(output.strip()))
    else:
        print('❌', "npm not installed")
        exit(1)

    # executing command to check if yarn is installed
    data = subprocess.Popen(['yarn', '--version'], stdout=subprocess.PIPE)
    output = data.communicate()[0].decode('utf-8')

    pattern = re.compile('\d+\.\d+\.\d+')

    if pattern.search(output):
        print('✔️', "yarn installed --- Version {}".format(output.strip()))
    else:
        print('❌', "yarn not installed")
        exit(1)

    # executing command to check if ts-node is installed
    data = subprocess.Popen(['ts-node', '-v'], stdout=subprocess.PIPE)
    output = data.communicate()[0].decode('utf-8')

    pattern = re.compile('v\d+\.\d+\.\d+')

    if pattern.search(output):
        print('✔️', "ts-node installed --- Version {}".format(output[1:].strip()))
    else:
        print('❌', "ts-node not installed")
        exit(1)

if __name__ == "__main__":
    main()