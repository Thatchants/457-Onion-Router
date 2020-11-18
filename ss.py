import sys
import socket
import _thread
import pickle
import os
import requests
import random

def connection(c, addr):
    print('made it to connection')
    #recvd_data = c.recv(1024)
    #data = pickle.loads(recvd_data)
    data = [2, [('129.82.44.69', '7812'), ('129.82.44.73', '1542')], 'http://google.com']
    if data[0] == 0 or True:
        end_of_chain(data[2])
    else:
        next_address_index = random.randint(0, data[0]-1)       #Random next ss
        next_address = data[1][next_address_index]              #next_address holds
        next_address = (next_address[0], int(next_address[1]))  #tuple with port as int
        data[1].pop(next_address_index)                         #remove next from list
        data[0] = data[0] - 1                                   #decrement addr count

        ss_socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss_socket_client.connect(next_address)
        pickle_data=pickle.dumps(data)
        ss_socket_client.send(pickle_data)
        client_receive(ss_socket_client)
    server_send(c)
    os.remove('tmp.html')

def server_send(socket):
    with open('tmp.html', 'r') as file:
        data = file.read()
    file_length = len(data)
    for i in range(0, file_length, 1024):
        upper_bound = (i + 1024) if (1024<len(data)-i) else len(data)
        socket.send(data[i:upper_bound].encode())
    socket.send('EOF'.encode())

def client_receive(socket):
    f = open('tmp.html', 'a')
    while 1:
        data_chunk = socket.recv(1024).decode()
        if data_chunk == 'EOF':
            break
        else:
            f.write(data_chunk)

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

    while(True):
        c, addr = ss_socket.accept()
        _thread.start_new_thread(connection, (c, addr, ))

if __name__ == "__main__":
    main()
