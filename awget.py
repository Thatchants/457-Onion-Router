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
    #args = str(sys.argv[1:])
    try:
        opts, args = getopt.getopt(argv, "hc:", ["chainfile="])
    except getopt.GetoptError:
        print('Usage: awget <URL> [-c chainfile]')
        sys.exit(2)
    #print("b4args:", args)
    #print("b4opt:" , opts)
    url = args
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: awget <URL> [-c chainfile]')
            sys.exit()
        elif opt in ("-c"):
            #print("we got here")
            chainfile = arg 
    #print("after args:", args)
    #print("after opt:" , opts)
    if len(args) != 0:
        url = args[0]
    elif len(args) == 0:
        print('Usage: awget <URL> [-c chainfile]')
        sys.exit()
    if (len(opts) == 0 and len(args) > 1):
        chainfile = args[2]
    #print(url)
    #print("Chainfile: ", chainfile)
    
    #time to read from the chaingang file
    cf = open(chainfile, "r")
    #cf.read().splitlines()
    
    
    chainlist = cf.read().splitlines()
    
    
    #hardcoding for now
    SSnum = int(chainlist[0])
    stones = chainlist[1:]
  
    count = 0
    for stone in stones:
        stonefrag = stone.split(' ')
        
        stone = (stonefrag[0], stonefrag[1])
        stones[count] = stone
        count = count +1
 
    chaingang = [SSnum, stones, url]
    print(chaingang)
    firstSSnum = random.randrange(0, len(stones))
    firstSS = stones[firstSSnum]

    print(firstSS)

    awget_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rand_index = random.randint(0, len(stones)-1)
    firstSS = stones[rand_index]
    awget_socket.connect((firstSS[0],int(firstSS[1])))
    #del chaingang[firstSSnum]
    chaingang[0] = chaingang[0] - 1 

    print(stones[:2])
    del stones[rand_index]
    print(chaingang)
    data=pickle.dumps(chaingang)
    awget_socket.send(data)
    client_receive(awget_socket)

def client_receive(socket):
    #f = open('tmp.html', 'a')
    #while 1:
    #    print('got a chunk')
    #    data_chunk = socket.recv(1024).decode()
    #    print(data_chunk)
    #    f.write(data_chunk)
    #    if len(data_chunk) < 1024:
    #        break;
    out_file = open('tmp.html', 'ab')
    while 1:
        data_chunk = socket.recv(1024)
        print(len(data_chunk))
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
