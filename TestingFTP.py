from ftplib import FTP
from tkinter import filedialog

Actual_host = "52.21.174.251"
Actual_username = "abdo"
Actual_password = "01096839681_Dv"


# with FTP(Actual_host) as ftp:
#     ftp.login(user=Actual_username, passwd=Actual_password)
#     print(ftp.getwelcome())

# Download from FTP server

def open_file():
    file = filedialog.askopenfile(mode='r', filetypes=[("Hex Files", '*.hex')])
    if file:
        file.close()
    return file.name


with open('mytest.txt', 'wb') as f:
    with FTP(Actual_host) as ftp:
        try:
            ftp.connect(host=Actual_host, port=21)
            ftp.retrbinary('RETR %s' % "test.txt", f.write)

    # Upload to FTP server
    # filename = open_file()
    # with open(filename, 'rb') as f:
    #     with FTP(Actual_host) as ftp:
    #         try:
    #             ftp.connect(host=Actual_host, port=21)
    #             ftp.login(user=Actual_username, passwd=Actual_password)
    #             print(len(f.read()))
    #             ftp.cwd("/Main_Directory")
    #             ftpResponseMessage = ftp.storbinary('STOR filetotest.txt', f)
    #             print(ftpResponseMessage)
    #             print(ftp.size("filetotest.txt"))
    #             f.close()
    #         except ftplib.all_errors as e:
    #             print(e)

# Delete


# with FTP(Actual_host) as ftp:
#     try:
#         ftp.connect(host=Actual_host, port=21)
#         ftp.login(user=Actual_username, passwd=Actual_password)
#         ftp.cwd("/Main_Directory")
#         ftp.delete('todelete.txt')
#     except ftplib.all_errors as e:
#         print(e)
