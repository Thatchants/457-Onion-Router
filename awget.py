import sys
import os
import argparse
import getopt
import random
import socket
import pickle
#aw


def main(argv):
    url = ""
    chainfile = "chaingang.txt"
    try:
        opts, args = getopt.getopt(argv, "hc:", ["chainfile="])
    except getopt.GetoptError:
        print('Usage: awget <URL> [-c chainfile]')
        sys.exit(2)
    url = args
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: awget <URL> [-c chainfile]')
            sys.exit()
        elif opt in ("-c"):
            chainfile = arg
    if len(args) != 0:
        url = args[0]
    elif len(args) == 0:
        print('Usage: awget <URL> [-c chainfile]')
        sys.exit()
    if (len(opts) == 0 and len(args) > 1):
        chainfile = args[2]

    if not os.path.exists(chainfile):
        print("Chainfile", chainfile, "not found")
        exit(0)
    cf = open(chainfile, "r")
    
    
    chainlist = cf.read().splitlines()

    SSnum = int(chainlist[0])
    stones = chainlist[1:]
  
    count = 0
    for stone in stones:
        stonefrag = stone.split(' ')
        
        stone = (stonefrag[0], stonefrag[1])
        stones[count] = stone
        count = count +1
 
    chaingang = [SSnum, stones, url]

    print('Request:', url)
    print('chainlist is')
    for ss in stones:
        print(ss)

    firstSSnum = random.randrange(0, len(stones))
    firstSS = stones[firstSSnum]

    awget_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rand_index = random.randint(0, len(stones)-1)
    firstSS = stones[rand_index]
    
    print('next SS is', firstSS)
    
    awget_socket.connect((firstSS[0],int(firstSS[1])))

    chaingang[0] = chaingang[0] - 1

    del stones[rand_index]

    data=pickle.dumps(chaingang)
    awget_socket.send(data)
    print('waiting for file..')
    client_receive(awget_socket, url)
    print('Received file', find_filename(url))
    print('Goodbye!')

def find_filename(url):
    common_endings = ['com','edu','gov','org','io','uk','ca','fr','tv','net','int','mil','us']
    last_slash = url.rindex('/')
    if last_slash == len(url) - 1:
        return 'index.html'
    filename = url[last_slash+1:]
    for ending in common_endings:
        dot_ending = '.' + ending
        if filename.endswith(dot_ending):
            return 'index.html'
    return filename

def client_receive(socket, url):
    out_file = open(find_filename(url), 'ab')
    while 1:
        data_chunk = socket.recv(1024)
        breaktime = False
        if data_chunk[-3:] == b'EOF':
            data_chunk = data_chunk[:-3]
            breaktime = True
        out_file.write(data_chunk)
        if breaktime:
            break
    out_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])
