import os
import sys
import subprocess
import fileinput

def main(argv):
        if os.geteuid() == 0:
                changeConfig(argv[1])
        else:
                subprocess.call(['sudo', 'python3', *sys.argv])
                sys.exit()

def getPort():
        with open('/etc/motion/motion.conf') as f:
                datafile = f.readlines()
        for line in datafile:
                if "stream_port" in line:
                        words = line.split()
                        return int(words[1])
        return -1

def changeConfig(port):
        prefix = 'stream_port'
        with fileinput.FileInput(files=('/etc/motion/motion.conf'), inplace=True) as f:
                for line in f:
                        words = line.split()
                        if len(words) == 2 and words[0] == prefix:
                                try:
                                        oldPort = int(words[1])
                                except ValueError:
                                        continue
                                line = prefix + " " + str(port)
                        print(line)

if __name__ == "__main__":
        main(sys.argv)
