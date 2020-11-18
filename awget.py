import sys
import os
import argparse
import getopt
import random
import socket
import pickle
#aw

#argParser = argparse.ArgumentParser()
#argParser.add_argument('-c')
#args = argParser.parse_args()

#print(args)

def main(argv):
    url = ""
    chainfile = "chaingang.txt"
    #args = str(sys.argv[1:])
    try:
        opts, args = getopt.getopt(argv, "hc:", ["chainfile="])
    except getopt.GetoptError:
        print('Usage: awget <URL> [-c chainfile]')
        sys.exit(2)
    print("args:", args)
    print("opt:" , opts)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: awget <URL> [-c chainfile]')
            sys.exit()
        elif opt in ("-c"):
            print("we got here")
            chainfile = arg 

    print("Chainfile: ", chainfile)
    SSnum = 3
    stones = [("129.82.44.69", "7812"), ("129.82.44.73", "1542"), ("129.82.44.80", "5000")]
    chaingang = [SSnum, stones, url]

    firstSSnum = random.randrange(0, len(stones))
    firstSS = stones[firstSSnum]

    print(firstSS)

    awget_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    firstSS = stones[2]
    awget_socket.connect((firstSS[0],int(firstSS[1])))
    #del chaingang[firstSSnum]
    chaingang[0] = chaingang[0] - 1 

    print(stones[:2])
    del stones[2]
    data=pickle.dumps(chaingang)
    awget_socket.send(data)

if __name__ == "__main__":
   main(sys.argv[1:])#aw
