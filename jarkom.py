from socket import *
import threading
import subprocess

def html(output,filename):
    # Mengecek file yang ada di local server
    daftar = ''
    if not output[0] == "" :
        for i in output:
            daftar += f'<tr><td><a href="http://127.0.0.1:10000/{filename}{i}" title="{i}">> {i}</a></td></tr>'
    else:
        daftar = f'<tr><td><a href="http://127.0.0.1:10000/" title="Homescreen">Halaman Kosong</a></td></tr>'
    html = '<html><body style="background-image: url(http://127.0.0.1:10000/FII1.webp), linear-gradient(#2491ef,#60b2f2,#60d6f2); background-repeat: repeat-x; background-position: bottom center; "><title>Homescreen</title><h1 style=" text-align: center; font-family: Century Gothic; color: white; text-decoration: none; text-shadow: 1px 1px rgba(0,0,0,0.5); font-weight: bold; padding-bottom: 40px; ">Database Server</h1><style> a {text-align: center; font-family: Century Gothic; color: white; text-decoration: none; text-shadow: 1px 1px rgba(0,0,0,0.5); font-weight: bold} </style>'+f'<table style="width:50%">{daftar}</table></body></html>'
    return html

def error422():
    ConnectionSocket.send('<html lang="en"><head><title>Error 422</title> </head><body style=" background-image: url(http://127.0.0.1:10000/FII1.webp), linear-gradient(#2491ef,#60b2f2,#60d6f2); background-repeat: repeat-x; background-position: bottom center;"> <style> .yaini{ text-align: center; font-size: 20px; font-family: Century Gothic; color: white; } </style> <teks class="yaini"> <h1 style="padding-top: 20%;">422</h1> <h3>Maaf, file ini tidak dapat ditampilkan</h3> </teks> </body></html>'.encode())

def handle_client(ConnectionSocket, html):
    try:
        message = ConnectionSocket.recv(1024).decode()
        if not message == "":
            filename = message.split()[1]   
            if "%20" in filename:
                filename = filename.replace("%20", " ")
            ConnectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            if filename == "/":
                output = subprocess.getoutput(f"dir /b").split("\n")
                html = html(output,"")
                ConnectionSocket.send(html.encode())
            elif "." in filename:
                with open(filename[1:], 'rb') as file_to_send:
                    for data in file_to_send:
                        ConnectionSocket.sendall(data)
            else:
                filename = filename.split("/", 1)
                output = subprocess.getoutput(f"cd {''.join(filename)} & dir /b").split("\n")
                print(output)
                print('=================================================================================')
                if "The system cannot find the path specified." in output:
                    raise IOError
                elif "The directory name is invalid." in output:
                    error422()
                else:
                    html = html(output, f"{''.join(filename)}/")
                    ConnectionSocket.send(html.encode())
    except IOError:
        ConnectionSocket.send('<html lang="en"><head><title>Error 404</title> </head><body style=" background-image: url(http://127.0.0.1:10000/FII1.webp), linear-gradient(#2491ef,#60b2f2,#60d6f2); background-repeat: repeat-x; background-position: bottom center;"> <style> .yaini{ text-align: center; font-size: 20px; font-family: Century Gothic; color: white; text-shadow: 2px 2px rgba(0,0,0,0.5);} </style> <teks class="yaini"> <h1 style="padding-top: 20%;">404</h1> <h3>Halaman yang anda cari tidak ada</h3> </teks> </body></html>'.encode())
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
