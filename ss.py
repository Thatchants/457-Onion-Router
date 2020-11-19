import sys
import socket
import _thread
import pickle
import os
import requests
import random
import getopt

def connection(c, addr):
    print('received connection from', addr)
    recvd_data = c.recv(1024)
    data = pickle.loads(recvd_data)
    #data = [2, [('129.82.44.69', '7812'), ('129.82.44.73', '1542')], 'http://google.com']
    if data[0] == 0:
        print('chainlist is empty')
        end_of_chain(data[2])
    else:
        print('chainlist is')
        for ss in data[1]:
            print(ss)
        next_address_index = random.randint(0, data[0]-1)       #Random next ss
        next_address = data[1][next_address_index]              #next_address holds
        next_address = (next_address[0], int(next_address[1]))  #tuple with port as int
        data[1].pop(next_address_index)                         #remove next from list
        data[0] = data[0] - 1                                   #decrement addr count

        ss_socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("next SS is", next_address)
        ss_socket_client.connect(next_address)
        print("waiting for file...")
        pickle_data=pickle.dumps(data)
        ss_socket_client.send(pickle_data)
        client_receive(ss_socket_client)
    server_send(c)
    os.remove('tmp.html')
    print('Goodbye!')

def server_send(socket):
    print('Relaying file ...')
    in_file = open('tmp.html', 'rb')
    data = in_file.read()
    data += b'EOF'
    in_file.close()
    
    file_length = len(data)
    for i in range(0, file_length, 1024):
        if file_length - i < 1024:
            socket.send(data[i:])
        else:
            socket.send(data[i:i + 1024])

def client_receive(socket):
    out_file = open('tmp.html', 'ab')
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

def end_of_chain(url):
    print('issuing wget for file ', find_filename(url))
    tmp_file_path = os.getcwd() + '/tmp.html'
    myfile = requests.get(url)
    open(tmp_file_path, 'wb').write(myfile.content)

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

def main(argv):
    #print hostname and port
    port = 5000
    if len(argv) >= 1:
        port = sys.argv[1]
    try:
        opts, args = getopt.getopt(argv, "hp:", ["port="])
    except getopt.GetoptError:
        print('Usage: ss [-p port]')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: ss [-p port]')
            sys.exit()
        elif opt in ("-p"):
            port = arg
    #port = sys.argv[1]
    hostname = socket.gethostname()
    print('Hostname:', hostname)
    print('Port:', port)

    #create socket
    ss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss_socket.bind((hostname, int(port)))

    ss_socket.listen(5)

    while(True):
        c, addr = ss_socket.accept()
        _thread.start_new_thread(connection, (c, addr, ))

if __name__ == "__main__":
   main(sys.argv[1:])
