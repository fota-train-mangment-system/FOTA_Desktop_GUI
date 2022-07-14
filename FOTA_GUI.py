import ftplib
import io
import random
from ftplib import FTP
from tkinter import *
from tkinter import messagebox, filedialog

from PIL import ImageTk, Image

# variables
Actual_host = "ftpupload.net"
Actual_username = "epiz_32106201"
Actual_password = "Dszu08oCxYUhN"

splash_root = Tk()
splash_root.configure(background='green')
splash_root.title("FOTA Desktop App")
window_height = 700
window_width = 800
screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

splash_root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

# Hide the title Bar
splash_root.wm_overrideredirect(True)
Label(splash_root, text="Welcome to FOTA Desktop Application", font=("Helvetica", 18, "bold"), fg='navy blue').pack(
    padx=10, pady=20)
splash_img = ImageTk.PhotoImage(Image.open("logo.png"))
Label(splash_root, image=splash_img).pack(pady=10)


def main():
    splash_root.destroy()

    root = Tk()
    root.title("Self Driving with FOTA")
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
        top.iconbitmap('logo.ico')
        top.title("About FOTA project")
        Label(top, text="Students from the faculty of Engineering in Mansoura University that developed\n this "
                        "Desktop Application to upload, download, delete and manipulate the FTP server to be\n the "
                        "first step in the journey of the code that will update the Microcontroller over the air\n"
                        "After you pressed upload just say goodbye to your code, because now it is burned on \nyour "
                        "Microcontroller and your system will have all these new features you coded.\n\n\n"
                        "thanks for Using ❤\n"
                        "\n\n\n\nStudents worked on this project:\n1-Abdallah El-sayed Issa\n2-Abdallah Mohammed Ragab"
                        "\n3-Fawzy Fawzy Elbayaa\n4-Mohammed Ali Mansour\n"
                        "5-Amro Mohamed Yehya\n6-Mohamed Hamdy Abdelsamie\n7-Abdelrahman Mostafa Ibrahem",
              font=("Courier", 10)).pack()
        Label(top, text="\n\n\n").pack()
        Button(top, text="Exit", command=top.destroy, padx=15, pady=15, font=("Courier", 10)).pack()
        Label(top, text="\n\n\n").pack()

    def mainframe():
        mainFrame = Toplevel()
        mainFrame.title("Self Driving with FOTA")
        mainFrame.iconbitmap('logo.ico')
        mainframe_width = mainFrame.winfo_screenwidth()
        mainframe_height = mainFrame.winfo_screenheight()
        mainFrame.geometry("%dx%d" % (mainframe_width, mainframe_height))

        def getlastupdate():
            try:
                with FTP(Actual_host) as ftp:
                    ftp.connect(host=Actual_host, port=21)
                    ftp.login(user=Actual_username, passwd=Actual_password)
                    # ftp.cwd("/Main_Directory")
                    entries = list(ftp.mlsd())
                    entries.sort(key=lambda entry: entry[1]['modify'], reverse=True)
                    latest_upload = entries[0][0]
                    print(latest_upload)
                    messagebox.showinfo(title="Hint", message="The last updated file is \n\n" + latest_upload)
            except ftplib.all_errors as error:
                popup_ftperror(error)

        def upload():
            try:
                filename = open_file()
                with open(filename, 'rb') as f:
                    with FTP(Actual_host) as ftp:
                        ftp.connect(host=Actual_host, port=21)
                        ftp.login(user=Actual_username, passwd=Actual_password)
                        ftp.encoding = "utf-8"
                        # print(f.read())
                        uploadfile = listbox_serverdir.get(ANCHOR)
                        ftp.storbinary(f'STOR {uploadfile}', f)
                        popup_upload("Your HEX file path is :  \n" + filename)
                        displayDir()
            except ftplib.all_errors as error:
                popup_ftperror(error)

        def download():
            try:
                filename = open_file()
                with open(filename, 'wb') as f:
                    with FTP(Actual_host) as ftp:
                        ftp.connect(host=Actual_host, port=21)
                        ftp.login(user=Actual_username, passwd=Actual_password)
                        # ftp.cwd("/Main_Directory")
                        todownloadfile = listbox_serverdir.get(ANCHOR)
                        ftp.retrbinary('RETR %s' % todownloadfile, f.write)
                        popup_download("Your HEX file was downloaded in the path : \n" + filename)
            except ftplib.all_errors as error:
                popup_ftperror(error)

        def displayDir():
            listbox_serverdir.insert(0, "--------------------------------------------")
            with FTP(Actual_host) as ftp:
                ftp.connect(host=Actual_host, port=21)
                ftp.login(user=Actual_username, passwd=Actual_password)
                dirlist = ftp.nlst()
                for item in dirlist:
                    listbox_serverdir.insert(0, item)

        def AddNewFile():
            e.grid(row=9, column=1)
            CreateNewFileBtn.grid(row=9, column=3)

        def createNewFile():
            fileName = e.get()
            try:
                with FTP(Actual_host) as ftp:
                    ftp.connect(host=Actual_host, port=21)
                    ftp.login(user=Actual_username, passwd=Actual_password)
                    bio = io.BytesIO(b'')
                    ftp.storbinary('STOR {0}'.format(fileName), bio)
                    displayDir()
                    e.grid_forget()
                    CreateNewFileBtn.grid_forget()
            except ftplib.all_errors as error:
                popup_ftperror(error)

        def refresh():
            listbox_serverdir.delete(0, END)
            displayDir()

        def delete():
            with FTP(Actual_host) as ftp:
                try:
                    ftp.connect(host=Actual_host, port=21)
                    ftp.login(user=Actual_username, passwd=Actual_password)
                    todelete = listbox_serverdir.get(ANCHOR)
                    ftp.delete(todelete)
                    popup_deleteDone()
                    displayDir()
                except ftplib.all_errors as error:
                    popup_ftperror(error)

        def open_file():
            file = filedialog.askopenfile(mode='r', filetypes=[("Hex Files", '*.hex')])
            if file:
                file.close()
            return file.name

        def backtologin():
            with FTP(Actual_host) as ftp:
                ftp.close()
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
        listbox_serverdir.pack(pady=15)
        Label(mainFrame, text="              ").grid(row=5, column=2)
        frame.grid(row=5, column=4)
        Label(mainFrame, text="              ").grid(row=6, column=0)
        Button(mainFrame, text="Get the last updated code", padx=30, pady=10, command=getlastupdate).grid(row=7,
                                                                                                          column=0)
        Label(mainFrame, text="              ").grid(row=8, column=0)
        Button(mainFrame, text="Add New File", padx=30, pady=10, command=AddNewFile).grid(row=9, column=0)
        e = Entry(mainFrame, width=30)
        e.grid_forget()
        Label(mainFrame, text="              ").grid(row=9, column=2)
        CreateNewFileBtn = Button(mainFrame, text="Create New File", padx=30, pady=10, command=createNewFile)
        CreateNewFileBtn.grid_forget()
        Label(mainFrame, text="              ").grid(row=10, column=0)
        Label(mainFrame, text="              ").grid(row=11, column=0)
        Label(mainFrame, text="              ").grid(row=12, column=0)
        Label(mainFrame, text="              ").grid(row=12, column=0)
        Button(mainFrame, text="refresh", padx=30, pady=10, command=refresh).grid(row=12, column=1)
        Label(mainFrame, text="              ").grid(row=12, column=3)
        Button(mainFrame, text="Disconnect and Exit", padx=30, pady=10, command=backtologin).grid(row=12, column=4)

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

    def popup_upload(message):
        messagebox.showinfo(title="Uploaded Successfully",
                             message="Upload process is done correctly ^_^\n\n" + message)

    def popup_download(message):
        messagebox.showinfo(title="downloaded Successfully",
                             message="Download process is done correctly ^_^\n\n" + message)

    def popup_nonvalidinput():
        messagebox.showerror(title="Error Occurred", message="You entered Wrong Credentials!")

    def popup_validlogin():
        messagebox.showinfo(title="You have the access", message="You've Entered the Credentials correctly ^_^")

    def popup_deleteDone():
        messagebox.showinfo(title="Success!", message="Deletion process is done correctly^_^")

    def popup_ftperror(message):
        messagebox.showerror(title="Error Occurred", message=message)

    Button(loginframe, text="connect", padx=30, pady=10, command=login).grid(row=1, column=0)
    Label(loginframe, text="                  ").grid(row=1, column=1)
    Button(loginframe, text="reset", padx=30, pady=10, command=reset).grid(row=1, column=2)
    Label(root, text="                  ").pack()
    Button(root, text="About Us", padx=30, pady=10, command=aboutus).pack()

    root.mainloop()


def color_changer():
    # choose and configure random color to the label text
    l1 = Label(splash_root, text="", font=("Helvetica", 18))
    l1.pack(pady=20)

    # create a list of different colors
    colors = ["navy blue", "red", "green", "blue"]
    # create a list of different texts
    labels = ["Thanks for your using our App ♥", "Our Team is welcoming you"]

    fg = random.choice(colors)
    l1.config(fg=fg)

    # choose and configure random text to the label
    text = random.choice(labels)
    l1.config(text=text)

    # call the color_changer() method after 100 micro seconds
    l1.after(100, color_changer)


color_changer()

splash_root.after(5000, main)
mainloop()

if __name__ == '__main__':
    main()
