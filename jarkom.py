from socket import *
import threading
import subprocess

def html(output):
    # Mengecek file yang ada di local server
    daftar = ''
    for i in output:
        daftar += f'<tr><td><a href="http://127.0.0.1:10000/{i}" title="{i}">{i}</a></td></tr>'
    html = "<html><style> table, th, td {   border:1px solid black; } </style>"+f'<table style="width:50%">{daftar}</table></html>'
    return html

def handle_client(ConnectionSocket, html):
    try:
        message = ConnectionSocket.recv(1024).decode()
        filename = message.split()[1]   
        if "%20" in filename:
            filename = filename.replace("%20", " ")
        if filename == "/":
            output = subprocess.getoutput(f"dir /b").split("\n")
        elif "." in filename:
            f = open(filename[1:])
            output = f.read()
            for i in range(0, len(output)):
                ConnectionSocket.send(output[i].encode())
        else:
            filename = filename.split("/", 1)
            output = subprocess.getoutput(f"cd {''.join(filename)} & dir /b").split("\n")
        html = html(output)
        ConnectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        ConnectionSocket.send(html.encode())
    except IOError:
        ConnectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        ConnectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
    ConnectionSocket.close()


if __name__ == "__main__":
    # Ini buat atur jaringan
    serversocket = socket(AF_INET, SOCK_STREAM)
    serverport = 10000
    serversocket.bind(('127.0.0.1', serverport))
    serversocket.listen()

    while True:
        # Kode kesepakatan client dan server
        ConnectionSocket, addr = serversocket.accept()

        # Menampilkan halaman awal
        client = threading.Thread(target=handle_client, args=(ConnectionSocket, html))
        client.start()
