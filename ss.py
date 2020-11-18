import sys
import socket
import _thread
import pickle
import os
import requests

def connection(c, addr):
    print('made it to connection')
    #recvd_data = c.recv(1024)
    #data = pickle.loads(recvd_data)
    data = [2, [('129.82.44.69', '7812'), ('129.82.44.73', '1542')], 'http://google.com']
    if data[0] == 0 or True:
        end_of_chain(data[2])

def end_of_chain(url):
    tmp_file_path = os.getcwd() + '/tmp.html'
    myfile = requests.get(url)
    open(tmp_file_path, 'wb').write(myfile.content)

def main():
    #print hostname and port
    port = sys.argv[1]
    hostname = socket.gethostname()
    print(hostname, port)
    
    #create socket
    ss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss_socket.bind((hostname, int(port)))
    
    ss_socket.listen(5)
    
    c, addr = "test", "this means nothing"
    _thread.start_new_thread(connection, (c, addr, ))
    while(True):
        continue
    '''
    while(True):
        #c, addr = ss_socket.accept()
        c, addr = "test", "this means nothing"
        _thread.start_new_thread(connection, (c, addr, ))
    '''

if __name__ == "__main__":
    main()
