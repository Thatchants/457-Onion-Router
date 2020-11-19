import sys
import socket
import _thread
import pickle
import os
import requests
import random

def connection(c, addr):
    print('received connection from', addr)
    recvd_data = c.recv(1024)
    data = pickle.loads(recvd_data)
    print(data)
    #data = [2, [('129.82.44.69', '7812'), ('129.82.44.73', '1542')], 'http://google.com']
    if data[0] == 0:
        end_of_chain(data[2])
    else:
        next_address_index = random.randint(0, data[0]-1)       #Random next ss
        next_address = data[1][next_address_index]              #next_address holds
        next_address = (next_address[0], int(next_address[1]))  #tuple with port as int
        data[1].pop(next_address_index)                         #remove next from list
        data[0] = data[0] - 1                                   #decrement addr count

        ss_socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("attemptint to connect to", next_address)
        ss_socket_client.connect(next_address)
        print("connected with", next_address)
        pickle_data=pickle.dumps(data)
        ss_socket_client.send(pickle_data)
        client_receive(ss_socket_client)
    server_send(c)
    os.remove('tmp.html')

def server_send(socket):
    #with open('tmp.html', 'r', encoding="ISO-8859-1") as file:
    #    data = file.read()
    #file_length = len(data)
    #for i in range(0, file_length, 1024):
    #    upper_bound = (i + 1024) if (1024<len(data)-i) else len(data)
    #    socket.send(data[i:upper_bound].encode())
    in_file = open('tmp.html', 'rb')
    data = in_file.read()
    data += b'EOF'
    print('len data after read: ', len(data))
    in_file.close()
    
    file_length = len(data)
    for i in range(0, file_length, 1024):
        if file_length - i < 1024:
            print('sending', len(data[i:]))
            socket.send(data[i:])
        else:
            print('sending', len(data[i:i+1024]))
            socket.send(data[i:i + 1024])

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

def end_of_chain(url):
    print('doing the actual wget')
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
