
def sendMsg(connection, *msg):
    str_msg = ''
    for i in msg:
        str_msg += str(i, 'utf-8') + "$"

    connection.send(bytes(str_msg, 'utf-8'))


def recvMsg(socket):
    values = ''
    while True:
        data = socket.recv(1024)
        values += str(data, 'utf-8')

        if not data:
            break

    return values.split("$")[:-1]

