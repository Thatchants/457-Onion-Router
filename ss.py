import sys
import socket
import _thread
import pickle
import wget

def connection(c, addr):
    #recvd_data = c.recv(1024)
    #data = pickle.loads(recvd_data)
    data = [2, [('129.82.44.69', '7812'), ('129.82.44.73', '1542')], 'google.com']
    if data[0] == 0:
        end_of_chain(data[3])

def end_of_chain(url):
    tmp.txt = wget.download(url)

def main():
    #print hostname and port
    port = sys.argv[1]
    hostname = socket.gethostname()
    print(hostname, port)
    
    #create socket
    ss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss_socket.bind((hostname, int(port)))
    
    ss_socket.listen(5)
    
    while(True):
        #c, addr = ss_socket.accept()
        c, addr = "test", "this means nothing"
        _thread.start_new_thread(connection, (c, addr, ))

if __name__ == "__main__":
    main()
