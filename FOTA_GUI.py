import ftplib
from ftplib import FTP
from tkinter import *
from tkinter import messagebox, filedialog

# TODO
#  logo and name of our team with colors and fonts
#  login activity with 3 editText (Host, user and password) and 1 button :
#  if the credentials are WRONG must popup a message and still be in the login activity
#  and if the credentials are correct it should take me to :
#  second activity which have
#  - the list of what FTP server have
#  - the last updated code that raspberry pi have RN
#  - Upload Button
#  - Download Button (with specifying the location to where it downloaded)
#  - Delete Button (From FTP server)
#  - Back to login activity
#  - with handling the Exceptions of directory not found, file not found,etc..


# variables
Actual_host = "52.21.174.251"
Actual_username = "abdo"
Actual_password = "01096839681_Dv"

root = Tk()
root.title("FOTA FTP App")
root.iconbitmap('logo.ico')
root.geometry("1200x300")

loginframe = LabelFrame(root, text="Login Form", padx=10, pady=10)
loginframe.pack()

hostframe = LabelFrame(loginframe, text="Enter the host :", padx=10, pady=10)
hostframe.grid(row=0, column=0)
hostEntry = Entry(hostframe, width=50, borderwidth=5)
hostEntry.pack()
# todo delete after testing
hostEntry.insert(0, Actual_host)
usernameframe = LabelFrame(loginframe, text="Enter the username :", padx=10, pady=10)
usernameframe.grid(row=0, column=1)
usernameEntry = Entry(usernameframe, width=50, borderwidth=5)
usernameEntry.pack()
# todo delete after testing
usernameEntry.insert(0, Actual_username)
passwordframe = LabelFrame(loginframe, text="Enter the password :", padx=10, pady=10)
passwordframe.grid(row=0, column=2)
passwordEntry = Entry(passwordframe, show='*', width=50, borderwidth=5)
passwordEntry.pack()
# todo delete after testing
passwordEntry.insert(0, Actual_password)


def aboutus():
    top = Toplevel()
    top.title("About FOTA project")
    Label(top, text="Students from the faculty of Engineering in Mansoura University that developed this "
                    "Desktop Application to upload, download, delete and manipulate the FTP server to be the first "
                    "step in the journey of the code that will update the Microcontroller over the air\n"
                    "After you pressed upload just say goodbye to your code, because now it is burned on your "
                    "Microcontroller and your system will have all these new features you coded.\n"
                    "thanks for Using ❤\n"
                    "\n\n\n\nStudents worked on this project:\n1-Abdallah El-sayed Issa\n2-Abdallah Mohammed Ragab"
                    "\n3-Fawzy Fawzy Elbayaa\n4-Mohammed Ali Mansour\n"
                    "5-Amro Mohamed Yehya\n6-Mohamed Hamdy Abdelsamie\n7-Abdelrahman Mostafa Ibrahem",
          font=("Courier", 10)).pack()
    top.iconbitmap('logo.ico')
    Button(top, text="Exit the New Window", command=top.destroy).pack()


def mainframe():
    mainFrame = Toplevel()
    mainFrame.title("FOTA FTP APP")
    mainFrame.iconbitmap('logo.ico')
    mainFrame.geometry("1200x500")

    # buttonClicked = False

    def getlastupdated():
        # global buttonClicked
        #
        # if buttonClicked:
        #     buttonClicked = False
        #     Label(mainFrame, text='Hi').grid(row=10, column=2)
        # if not buttonClicked:
        #     buttonClicked = True

        try:
            with FTP(Actual_host) as ftp:
                ftp.connect(host=Actual_host, port=21)
                ftp.login(user=Actual_username, passwd=Actual_password)
                # ftp.cwd("/Main_Directory")
                lastfile = sorted(ftp.nlst(), key=lambda x: ftp.voidcmd(f"MDTM {x}"))[-1]
                l1 = Label(mainFrame, text=lastfile)
                l1.grid(row=7, column=1)
                displayDir()
        except ftplib.all_errors as e:
            popup_ftperror(e)

    def upload():
        try:
            filename = open_file()
            with open(filename, 'rb') as f:
                with FTP(Actual_host) as ftp:
                    ftp.connect(host=Actual_host, port=21)
                    ftp.login(user=Actual_username, passwd=Actual_password)
                    ftp.encoding = "utf-8"
                    # print(f.read())
                    # ftp.cwd("/Main_Directory")
                    uploadfile = listbox_serverdir.get(ANCHOR)
                    ftpResponseMessage = ftp.storbinary(f'STOR {uploadfile}', f)
                    l1 = Label(mainFrame, text="Your HEX file path is : " + filename)
                    l1.grid(row=1, column=2)  # todo 2->3
                    print(ftpResponseMessage)
                    print(ftp.size(uploadfile))
                    popup_UploadDone()
                    displayDir()
        except ftplib.all_errors as e:
            popup_ftperror(e)

    def download():
        # try:
        filename = open_file()
        with open(filename, 'wb') as f:
            with FTP(Actual_host) as ftp:
                ftp.connect(host=Actual_host, port=21)
                ftp.login(user=Actual_username, passwd=Actual_password)
                # ftp.cwd("/Main_Directory")
                todownloadfile = listbox_serverdir.get(ANCHOR)
                ftp.retrbinary('RETR %s' % todownloadfile, f.write)
                l1 = Label(mainFrame, text="Your HEX file will be downloaded in the path : " + filename)
                l1.grid(row=3, column=2)
                popup_DownloadDone()
                displayDir()

    def displayDir():
        # todo : refresh the displayDir after every operation
        listbox_serverdir.insert(0, "--------------------------------------------")
        with FTP(Actual_host) as ftp:
            ftp.connect(host=Actual_host, port=21)
            ftp.login(user=Actual_username, passwd=Actual_password)
            dirlist = ftp.nlst()
            for item in dirlist:
                listbox_serverdir.insert(0, item)

    def refresh():
        listbox_serverdir.delete(0, END)
        displayDir()

    # except ftplib.all_errors as e:
    #     popup_ftperror(e)

    def delete():
        with FTP(Actual_host) as ftp:
            try:
                ftp.connect(host=Actual_host, port=21)
                ftp.login(user=Actual_username, passwd=Actual_password)
                todelete = listbox_serverdir.get(ANCHOR)
                ftp.delete(todelete)
                popup_deleteDone()
                displayDir()
            except ftplib.all_errors as e:
                popup_ftperror(e)

    def open_file():
        file = filedialog.askopenfile(mode='r', filetypes=[("Hex Files", '*.hex')])
        if file:
            file.close()
        return file.name

    def backtologin():
        root.deiconify()
        mainFrame.destroy()

    Label(mainFrame, text="              ").grid(row=0, column=0)
    Label(mainFrame, text="Enter both the path of Hex file you want to upload and the file to upload in",
          font='Georgia 12').grid(row=1, column=0)
    Button(mainFrame, text="Upload", padx=30, pady=10, command=upload).grid(row=1, column=1)
    Label(mainFrame, text="              ").grid(row=2, column=0)
    Label(mainFrame, text="Enter both the file you want to download and path to get the file in",
          font='Georgia 12').grid(row=3,
                                  column=0)
    Button(mainFrame, text="Download", padx=22, pady=10, command=download).grid(row=3, column=1)
    Label(mainFrame, text="              ").grid(row=4, column=0)
    Label(mainFrame, text="Choose the file from listBox to delete", font='Georgia 12').grid(row=5, column=0)
    Button(mainFrame, text="Delete", padx=32, pady=10, command=delete).grid(row=5, column=1)
    frame = Frame(mainFrame)
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    listbox_serverdir = Listbox(frame, width=40, height=10, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox_serverdir.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    frame.grid(row=5, column=3)
    listbox_serverdir.pack(pady=15)
    Label(mainFrame, text="              ").grid(row=6, column=0)
    Button(mainFrame, text="Get the last updated code", padx=30, pady=10, command=getlastupdated).grid(row=7, column=0)
    Label(mainFrame, text="              ").grid(row=8, column=0)
    Label(mainFrame, text="              ").grid(row=9, column=0)
    Label(mainFrame, text="              ").grid(row=9, column=1)
    Button(mainFrame, text="refresh", padx=30, pady=10, command=refresh).grid(row=9, column=2)
    Button(mainFrame, text="Disconnect and Exit", padx=30, pady=10, command=backtologin).grid(row=9, column=3)

    displayDir()

    mainFrame.protocol('WM_DELETE_WINDOW', backtologin)


def connecttoftp():
    try:
        with FTP(Actual_host) as ftp:
            ftp.login(user=Actual_username, passwd=Actual_password)
            print(ftp.getwelcome())
    except ftplib.all_errors as e:
        print(e)
        popup_ftperror(e)


def login():
    if (hostEntry.get() == Actual_host) and (usernameEntry.get() == Actual_username) and (
            passwordEntry.get() == Actual_password):
        connecttoftp()
        popup_validlogin()
        mainframe()
        root.withdraw()
    else:
        reset()
        popup_nonvalidinput()


def reset():
    hostEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)


def popup_nonvalidinput():
    messagebox.showerror("Error Occurred", "You entered Wrong Credentials!")


def popup_validlogin():
    messagebox.showinfo(title="You have the access", message="You Entered the Credentials correctly ^_^")


def popup_deleteDone():
    messagebox.showinfo(title="Success!", message="Deletion process is done correctly^_^")


def popup_UploadDone():
    messagebox.showinfo(title="Success!", message="Upload process is done correctly^_^")


def popup_DownloadDone():
    messagebox.showinfo(title="some thing!", message="Download process is done correctly^_^")


def popup_ftperror(message):
    messagebox.showerror("Error Occurred", message)


Button(loginframe, text="connect", padx=30, pady=10, command=login).grid(row=1, column=0)
Label(loginframe, text="                  ").grid(row=1, column=1)
Button(loginframe, text="reset", padx=30, pady=10, command=reset).grid(row=1, column=2)
Button(root, text="About Us", padx=30, pady=10, command=aboutus).pack()

root.mainloop()
