from socket import *
import threading
import subprocess

def html(output,filename):
    daftar = ''
    # Mengecek apakah di dalam folder ini terdapat file
    if not output[0] == "" :
        # Jika tidak ada, maka akan dibuat tabel yang berisi file yang ada di dalam server
        for i in output:
            daftar += f'<tr><td><a href="http://127.0.0.1:10000/{filename}{i}" title="{i}">> {i}</a></td></tr>'
    # Jika folder di dalamnya kosong
    else:
        # Maka akan menampilkan tulisan "Folder Kosong"
        daftar = f'<tr><td><a href="http://127.0.0.1:10000/" title="Homescreen">Folder Kosong</a></td></tr>'
    html = '<html><body style="background-image: url(http://127.0.0.1:10000/FII1.webp), linear-gradient(#2491ef,#60b2f2,#60d6f2); background-repeat: repeat-x; background-position: bottom center; "><title>Homescreen</title><h1 style=" text-align: center; font-family: Century Gothic; color: white; text-decoration: none; text-shadow: 1px 1px rgba(0,0,0,0.5); font-weight: bold; padding-bottom: 40px; ">Database Server</h1><style> a {text-align: center; font-family: Century Gothic; color: white; text-decoration: none; text-shadow: 1px 1px rgba(0,0,0,0.5); font-weight: bold} </style>'+f'<table style="width:50%">{daftar}</table></body></html>'
    return html

def error422():
    ConnectionSocket.send('<html lang="en"><head><title>Error 422</title> </head><body style=" background-image: url(http://127.0.0.1:10000/FII1.webp), linear-gradient(#2491ef,#60b2f2,#60d6f2); background-repeat: repeat-x; background-position: bottom center;"> <style> .yaini{ text-align: center; font-size: 20px; font-family: Century Gothic; color: white; } </style> <teks class="yaini"> <h1 style="padding-top: 20%;">422</h1> <h3>Maaf, file ini tidak dapat ditampilkan</h3> </teks> </body></html>'.encode())

def handle_client(ConnectionSocket, html):
    try:
        # Menunggu client menekan sesuatu
        message = ConnectionSocket.recv(1024).decode()
        # Mengecek apakah client menekan sesuatu
        if not message == "":
            # Mengambil nama file yang client ingin akses
            filename = message.split()[1]  
            # Mengecek apakah nama file yang di inginkan client terdapat kata %20 
            if "%20" in filename:
                # Jika beneran ada, maka di gantikan dengan spasi
                filename = filename.replace("%20", " ")
            ConnectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            # Apabila client mengakses server dengan cara menuliskan IPnya saja
            if filename == "/":
                # Program akan mengecek seluruh folder yang ada di direktori server
                output = subprocess.getoutput(f"dir /b").split("\n")
                # Memanggil dan memproses file HTML
                html = html(output,"")
                # Mengirim kode HTML kepada client
                ConnectionSocket.send(html.encode())
            # Apabila client ingin mengakses file yang ada formatnya (misal: pdf, word, txt, dll)
            elif "." in filename:
                # Server akan membuka file yang ingin client akses di server
                with open(filename[1:], 'rb') as file_to_send:
                    # Program akan ngecompile file
                    for data in file_to_send:
                        # File akan dikirim ke client
                        ConnectionSocket.sendall(data)
            # Apabila client ingin mengakses folder
            else:
                # Menghapus '/' di awalan 
                filename = filename.split("/", 1)
                # Server akan membuka folder yang ingin client akses di server lalu mengecek seluruh folder yang ada di direktori server
                output = subprocess.getoutput(f"cd {''.join(filename)} & dir /b").split("\n")
                # Mengecek apakah folder ini ada di server
                if "The system cannot find the path specified." in output:
                    # Jika tidak ada, maka akan di alihkan ke error 404
                    raise IOError
                # Mengecek apakah folder ini valid atau tidak
                elif "The directory name is invalid." in output:
                    # Jika tidak ada, maka akan di alihkan ke error 422
                    error422()
                # Jika foldernya ada
                else:
                    # Memanggil dan memproses file HTML
                    html = html(output, f"{''.join(filename)}/")
                    # Mengirim kode HTML kepada client
                    ConnectionSocket.send(html.encode())
    except IOError:
        # Menampilkan HTML Error 404
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

        # Memanggil function HTML
        client = threading.Thread(target=handle_client, args=(ConnectionSocket, html))
        client.start()
