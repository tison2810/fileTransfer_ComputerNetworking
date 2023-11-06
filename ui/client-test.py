import os
import json
import socket
import threading
import time
import random
import sys
import platform
from Base import Base
 
# GUI
import tkinter
import tkinter.messagebox
import tkinter.filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from PIL import ImageTk 
from PIL import Image
import customtkinter

# aid
from hashfunction import MD5_hash
import asset

# ----CONSTANT----#
FORMAT = "utf-8"
BUFFER_SIZE = 2048
OFFSET = 10000

# --------------- #

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

# popup notification
def display_noti(title, content):
    tkinter.messagebox.showinfo(title, content)

# popup window class for files 
## to do: add clients' files to this list
class ClientFilesList(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("550x290")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollable_files_frame = customtkinter.CTkScrollableFrame(self, label_text="List of Files")
        self.scrollable_files_frame.grid(row=0, column=0, rowspan=4, padx=(10, 0), pady=(10, 0), sticky="nsew")
        
        self.scrollable_clients_files = []
        for i in range(100):
            client_label = customtkinter.CTkLabel(master=self.scrollable_files_frame, text="File's Name")
            client_label.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_clients_files.append(client_label)

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # __init__ function for class CTk
        # customtkinter.CTk.__init__(self, *args, **kwargs)

        # configure windows
        self.title("P2P Server")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (3x?)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="P2P Server", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button = customtkinter.CTkButton(self.sidebar_frame, text="Quit", command=self.sidebar_button_event)
        self.sidebar_button.grid(row=1, column=0, padx=20, pady=10)

        # change appearance mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # change scaling
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create scrollable frame for clients list
        ## to do: add clients to this frame
        self.scrollable_clients_frame = customtkinter.CTkScrollableFrame(self, label_text="Clients")
        self.scrollable_clients_frame.grid(row=0, column=1, rowspan=4, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.scrollable_clients_frame.grid_columnconfigure((0), weight=1)
        self.scrollable_clients_names = []
        ## to do: modify range to number of current clients
        for i in range(100):
            client_label = customtkinter.CTkLabel(master=self.scrollable_clients_frame, text="Client's Name")
            client_label.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_clients_names.append(client_label)

            view_button = customtkinter.CTkButton(master=self.scrollable_clients_frame, text="View Files", command=self.view_client_files)
            view_button.grid(row=i, column=1, padx=10, pady=(0, 20))
            self.files_list = None

            ping_button = customtkinter.CTkButton(master=self.scrollable_clients_frame, text="Ping", command=self.ping_client)
            ping_button.grid(row=i, column=2, padx=10, pady=(0, 20))


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    ## to do: stop server
    def sidebar_button_event(self):
        print("huhu")

    def view_client_files(self):
        print("button pressed")
        if self.files_list is None or not self.files_list.winfo_exists():
            self.files_list = ClientFilesList(self)  # create window if its None or destroyed
        else:
            self.files_list.focus()  # if window exists focus it

    ## to do:
    def ping_client():
        print("button pressed")

## ====================GUI IMPLEMENT======================##

# _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
# _fgcolor = '#000000'  # X11 color: 'black'
# _compcolor = 'gray40' # X11 color: #666666
# _ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
# _ana2color = 'beige' # X11 color: #f5f5dc
# _tabfg1 = 'black' 
# _tabfg2 = 'black' 
# _tabbg1 = 'grey75' 
# _tabbg2 = 'grey89' 
# _bgmode = 'light'

# _style_code_ran = 0
# def _style_code():
#     global _style_code_ran
#     if _style_code_ran:
#        return
#     style = ttk.Style()
#     if sys.platform == "win32":
#        style.theme_use('winnative')
#     style.configure('.',background=_bgcolor)
#     style.configure('.',foreground=_fgcolor)
#     style.configure('.',font='TkDefaultFont')
#     style.map('.',background =
#        [('selected', _compcolor), ('active',_ana2color)])
#     if _bgmode == 'dark':
#        style.map('.',foreground =
#          [('selected', 'white'), ('active','white')])
#     else:
#        style.map('.',foreground =
#          [('selected', 'black'), ('active','black')])
#     style.configure('Vertical.TScrollbar',  background=_bgcolor,
#         arrowcolor= _fgcolor)
#     style.configure('Horizontal.TScrollbar',  background=_bgcolor,
#         arrowcolor= _fgcolor)
#     _style_code_ran = 1

class tkinterApp(customtkinter.CTk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        customtkinter.CTk.__init__(self, *args, **kwargs)

        # creating a container
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.chatroom_textCons = None

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, RegisterPage, LoginPage, RepoPage):
            frame = F(container, self, *args, **kwargs)
            # initializing frame of that object from
            # startpage, registerpage, loginpage, chatpage respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg_color='white')
        self.show_frame(StartPage)

    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)

        # start page title
        customtkinter.CTkLabel(self, text="P2P File Sharing", bg_color="#bf8bff", fg_color="white",
                                font=("Verdana", 18)).pack(fill='x')
        customtkinter.CTkLabel(self, text="", bg_color='white').pack()

        # set port label
        customtkinter.CTkLabel(self, text="Set Port (1024 -> 65535)", bg_color='white').pack()

        # set port entry
        self.port_entry = customtkinter.CTkEntry(self, font=("Verdana", 11))
        self.port_entry.pack()
        customtkinter.CTkLabel(self, text="", bg_color='white').pack()

        # create a register button
        customtkinter.CTkButton(self, text="Đăng ký", bg_color="#5D0CB5", fg_color="white", command=lambda: self.enter_app(
            controller=controller, port=self.port_entry.get(), page=RegisterPage)).pack()
        customtkinter.CTkButton(self, text="", bg_color='white').pack()

        # create a login button
        customtkinter.CTkButton(self, text="Đăng nhập", bg_color="#A021E2", fg_color="white", command=lambda: self.enter_app(
            controller=controller, port=self.port_entry.get(), page=LoginPage)).pack()

    def enter_app(self, controller, port, page):
        try:
            # get peer current ip address -> assign to serverhost
            hostname=socket.gethostname()   
            IPAddr=socket.gethostbyname(hostname)  

            # init server
            global network_peer
            network_peer = NetworkPeer(serverhost=IPAddr, serverport=int(port))
           
            # A child thread for receiving message
            recv_t = threading.Thread(target=network_peer.input_recv)
            recv_t.daemon = True
            recv_t.start()

            # A child thread for receiving file
            recv_file_t = threading.Thread(target=network_peer.recv_file_content)
            recv_file_t.daemon = True
            recv_file_t.start()
            controller.show_frame(page)
        except:
            self.port_entry.delete(0, customtkinter.END)
            display_noti("Port Error!",  "Cổng đã được sử dụng hoặc chứa giá trị rỗng")

class RegisterPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)

        # Sign Up Image
        signup_pic = ImageTk.PhotoImage(asset.signup_image)
        signupImg = tkinter.Label(self, image=signup_pic, bg='white')
        signupImg.image = signup_pic
        signupImg.place(x=50, y=50)

        # Title
        customtkinter.CTkLabel(self, text='Đăng ký',
                 fg_color='#bf8bff', bg_color='white',
                 font=("Roboto", 24, 'bold')).place(x=670, y=100)
        # Username
        customtkinter.CTkLabel(self, text='Tên đăng nhập', bg_color='white',
                 fg_color='#57a1f8', font=("Roboto", 11)).place(x=670, y=175)
        self.username_entry = customtkinter.CTkEntry(self, fg_color='black',
                                       bg_color='white', font=("Roboto", 10))
        self.username_entry.place(x=675, y=200)
        customtkinter.CTkFrame(self, bg_color='#777777').place(x=675, y=225)

        # Password
        customtkinter.CTkLabel(self, text='Mật khẩu', bg_color='white',
                 fg_color='#57a1f8', font=("Roboto", 11)).place(x=670, y=250)
        self.password_entry = customtkinter.CTkEntry(self, fg_color='black',
                                       bg_color='white', font=("Roboto", 10), show='*')
        self.password_entry.place(x=675, y=275)
        customtkinter.CTkFrame(self, width=275, bg_color='#777777').place(x=675, y=300)

        # Submit
        customtkinter.CTkButton(self, text='Đăng ký', bg_color='#bf8bff',
                  fg_color='white', command=lambda: self.register_user(self.username_entry.get(), self.password_entry.get())).place(x=675, y=325)
        customtkinter.CTkLabel(self, text="Đã có tài khoản ?",
                 fg_color='black', bg_color='white', font=("Roboto", 10)).place(x=675, y=375)
        customtkinter.CTkButton(self, text='Đăng nhập',
                  bg_color='white', cursor='hand2', fg_color='#57a1f8', command=lambda: controller.show_frame(LoginPage)).place(x=670, y=400)

    def register_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        network_peer.send_register()

class LoginPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        # Login Image
        login_pic = ImageTk.PhotoImage(asset.login_image)
        loginImg = tkinter.Label(self, image=login_pic)
        loginImg.image = login_pic
        loginImg.place(x=50, y=50)

        # Title
        customtkinter.CTkLabel(self, text='Đăng nhập',
                 fg_color='#bf8bff', bg_color='white',
                 font=("Roboto", 24, 'bold')).place(x=670, y=100)

        # Username
        customtkinter.CTkLabel(self, text="Username", fg_color='#57a1f8', font=("Roboto", 11)).place(x=670, y=175)
        self.username_entry = customtkinter.CTkEntry(self, fg_color='black',
                                       bg_color='white', font=("Roboto", 10))
        self.username_entry.place(x=675, y=200)
        customtkinter.CTkFrame(self, width=275, bg_color='#777777').place(x=675, y=225)

        # Password
        customtkinter.CTkLabel(self, text='Mật khẩu', bg_color='white',
                 fg_color='#57a1f8', font=("Roboto", 11)).place(x=670, y=250)
        self.password_entry = customtkinter.CTkEntry(self, fg_color='black',
                                       bg_color='white', font=("Roboto", 10), show='*')
        self.password_entry.place(x=675, y=275)
        customtkinter.CTkFrame(self, bg_color='#777777').place(x=675, y=300)

        # Submit
        customtkinter.CTkButton(self, text='Đăng nhập', bg_color='#bf8bff',
                  fg_color='white', command=lambda: self.login_user(username=self.username_entry.get(), password=self.password_entry.get())).place(x=675, y=325)
        customtkinter.CTkLabel(self, text="Bạn không có tài khoản ?",
                 fg_color='black', bg_color='white', font=("Roboto", 10)).place(x=675, y=375)
        customtkinter.CTkButton(self, text='Đăng ký',
                  bg_color='white', cursor='hand2', fg_color='#57a1f8', command=lambda: controller.show_frame(RegisterPage)).place(x=670, y=400)

    def login_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        network_peer.send_login()

class RepoPage(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        customtkinter.CTkFrame.__init__(self, parent)
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        
        # configure grid layout (3x?)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets
        # start of sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="P2P Server", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button = customtkinter.CTkButton(self.sidebar_frame, text="Quit", command=self.sidebar_button_event)
        self.sidebar_button.grid(row=1, column=0, padx=20, pady=10)

        # sidebar buttons
        self.sidebar_button = customtkinter.CTkButton(self.sidebar_frame, text="Quit", command=self.sidebar_button_event)
        self.sidebar_button.grid(row=1, column=0, padx=20, pady=10)
        self.logout_button = customtkinter.CTkButton(self.sidebar_frame, text="Log Out", command=self.sidebar_button_event)
        self.logout_button.grid(row=2, column=0, padx=20, pady=10)
        # change appearance mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        # change scaling
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        # end of sidebar

        #### create frame for repo
        self.repo_frame = customtkinter.CTkFrame(self, fg_color_color="transparent")
        self.repo_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
        self.repo_frame.grid_rowconfigure(0, weight=1)
        self.repo_frame.grid_columnconfigure(0, weight=1)
        # create scrollable frame for repo list
        ## to do: add file names to this frame
        self.scrollable_repo_frame = customtkinter.CTkScrollableFrame(self.repo_frame, label_text="Repository")
        self.scrollable_repo_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_repo_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_repo_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_file_names = []
        ## to do: modify range to number of current files
        for i in range(100):
            file_label = customtkinter.CTkLabel(master=self.scrollable_repo_frame, text="File's Name")
            file_label.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_file_names.append(file_label)
        # create repo buttons
        # create temp frame
        self.temp_frame = customtkinter.CTkFrame(master=self.repo_frame, fg_color_color="transparent")
        self.temp_frame.grid(row=1, column=0, sticky="nsew")
        self.temp_frame.grid_rowconfigure(0, weight=1)
        self.temp_frame.grid_columnconfigure(0, weight=1)
        self.temp_frame.grid_columnconfigure(1, weight=1)
        # create delete button
        self.delete_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Delete from Repo")
        self.delete_button.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create choose file button
        self.add_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Add to Repo")
        self.add_button.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create update to server button
        self.update_button = customtkinter.CTkButton(master=self.repo_frame, border_width=2, text="Update to Server")
        self.update_button.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create reload repo button
        self.update_button = customtkinter.CTkButton(master=self.repo_frame, border_width=2, text="Reload Repo")
        self.update_button.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        ### create frame for peer list
        self.peer_frame = customtkinter.CTkFrame(self, fg_color_color="transparent")
        self.peer_frame.grid(row=0, column=2, rowspan=3, sticky="nsew")
        self.peer_frame.grid_rowconfigure(0, weight=1)
        self.peer_frame.grid_columnconfigure(0, weight=1)
        # create scrollable peer list
        ## to do: add peer names to this frame
        self.scrollable_peer_frame = customtkinter.CTkScrollableFrame(self.peer_frame, label_text="Peer List")
        self.scrollable_peer_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_peer_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_peer_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_peer_names = []
        ## to do: modify range to number of current peers
        for i in range(100):
            peer_label = customtkinter.CTkLabel(master=self.scrollable_peer_frame, text="Peer's Name")
            peer_label.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_peer_names.append(peer_label)
        # create search for file
        self.search_frame = customtkinter.CTkFrame(self.peer_frame, fg_color_color="transparent")
        self.search_frame.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.search_frame.grid_rowconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_entry = customtkinter.CTkEntry(master=self.search_frame, placeholder_text="Search...")
        self.search_entry.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.search_button = customtkinter.CTkButton(master=self.search_frame, text="Search", border_width=2)
        self.search_button.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        # create send connect request button
        self.request_button = customtkinter.CTkButton(master=self.peer_frame, border_width=2,
                                                     command=lambda:self.chooseFile(), text="Send Connect Request")
        self.request_button.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # create CLI
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Command...")
        self.entry.grid(row=3, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # self.main_button_1 = customtkinter.CTkButton(master=self, text="Enter", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        # self.main_button_1.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def sendFile(self, friend_name):
        file_path = tkinter.filedialog.askopenfilename(initialdir="/",
                                                       title="Select a File",
                                                       filetypes=(("All files", "*.*"),))
        file_name = os.path.basename(file_path)
        msg_box = tkinter.messagebox.askquestion('File Explorer', 'Are you sure to send {} to {}?'.format(file_name, friend_name),
                                                 icon="question")
        if msg_box == 'yes':
            sf_t = threading.Thread(
                target=network_peer.transfer_file, args=(self.friend_name, file_path))
            sf_t.daemon = True
            sf_t.start()
            tkinter.messagebox.showinfo(
                "File Transfer", '{} has been sent to {}!'.format(file_name, friend_name))

    def chooseFile(self):
        file_path = tkinter.filedialog.askopenfilename(initialdir="/",
                                                       title="Select a File",
                                                       filetypes=(("All files", "*.*"),))
        # file_name = os.path.basename(file_path)
        file_name = file_path
        msg_box = tkinter.messagebox.askquestion('File Explorer', 'Upload {} to local repository?'.format(file_name),
                                                 icon="question")
        if msg_box == 'yes':
            popup = simpledialog.askstring("Input","Nhập tên file trên Localrepo",parent = self)
            file_name = popup + "(" + file_name + ")"
            self.Scrolledlistbox1.insert(0,file_name)
            tkinter.messagebox.showinfo(
                "Local Repository", '{} has been added to localrepo!'.format(file_name))
    
    def deleteSelectedFile(self):
        file_name = self.Scrolledlistbox1.get(customtkinter.ANCHOR)
        self.Scrolledlistbox1.delete(customtkinter.ANCHOR)
        network_peer.deleteFileServer(file_name)

# ------ end of GUI ------- #
class NetworkPeer(Base):
    def __init__(self, serverhost='localhost', serverport=30000, server_info=('192.168.137.1', 40000)):
        super(NetworkPeer, self).__init__(serverhost, serverport)

        # init host and port of central server
        self.server_info = server_info

        # peer name
        self.name = ""
        # peer password
        self.password = ""

        # all peers it can connect (network peers)
        self.connectable_peer = {}

        # peers it has connected (friend)
        self.friendlist = {}

        self.message_format = '{peername}: {message}'
        # file buffer
        self.file_buf = []

        # define handlers for received message of network peer
        handlers = {
            'REGISTER_SUCCESS': self.register_success,
            'REGISTER_ERROR': self.register_error,
            'LOGIN_SUCCESS': self.login_success,
            'LOGIN_ERROR': self.login_error,
            'LIST_USER_SHARE_FILE': self.get_users_share_file,
            'FILE_REQUEST': self.file_request,
            'FILE_ACCEPT': self.file_accept,
            'FILE_REFUSE': self.file_refuse,
        }
        for msgtype, function in handlers.items():
            self.add_handler(msgtype, function)

    ## ==========implement protocol for user registration - network peer==========##
    def send_register(self):
        """ Send a request to server to register peer's information. """
        peer_info = {
            'peername': self.name,
            'password': self.password,
            'host': self.serverhost,
            'port': self.serverport
        }
        self.client_send(self.server_info,
                         msgtype='PEER_REGISTER', msgdata=peer_info)

    def register_success(self, msgdata):
        """ Processing received message from server: Successful registration on the server. """
        display_noti('Register Noti', 'Đăng ký thành công')
        print('Register Successful.')

    def register_error(self, msgdata):
        """ Processing received message from server: Registration failed on the server. """
        display_noti('Register Noti',
                     'Đăng ký thất bại. Tên đăng nhập đã tồn tại hoặc không hợp lệ!')
        print('Register Error. Username existed. Login!')
    ## ===========================================================##

    ## ==========implement protocol for authentication (log in) - network peer==========##
    def send_login(self):
        """ Send a request to server to login. """
        peer_info = {
            'peername': self.name,
            'password': self.password,
            'host': self.serverhost,
            'port': self.serverport
        }
        self.client_send(self.server_info,
                         msgtype='PEER_LOGIN', msgdata=peer_info)

    def login_success(self, msgdata):
        """ Processing received message from server: Successful login on the server. """
        print('Login Successful.')
        display_noti('Login Noti', 'Login Successful.')
        app.geometry("1100x600")
        app.resizable(False, False)
        app.show_frame(RepoPage)

    def login_error(self, msgdata):
        """ Processing received message from server: Login failed on the server. """
        display_noti('Login Noti', 'Login Error. Username not existed!')
        print('Login Error. Username not existed. Register!')
    ## ===========================================================##

    ## ==========implement protocol for getting online user list who have file that client find==========##
    def send_listpeer(self, filename):
        """ Send a request to server to get all online peers who have file that client find. """
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': filename
        }
        self.client_send(self.server_info,
                         msgtype='PEER_SEARCH', msgdata=peer_info)

    def get_users_share_file(self, msgdata):
        """ Processing received message from server:
            Output username of all peers that have file which client is finding."""
        self.connectable_peer.clear()
        for key, value in msgdata['online_user_list_have_file'].items():
            self.connectable_peer[key] = tuple(value)
        if self.name in self.connectable_peer:
            self.connectable_peer.pop(self.name)
    ## ===========================================================##

    ## ==========implement protocol for file request==========##
    def send_request(self, peername, filename):
        """ Send a chat request to an online user. """
        try:
            server_info = self.connectable_peer[peername]
        except KeyError:
            display_noti("File Request Error",
                         'This peer ({}) is not available.'.format(peername))
        else:
            data = {
                'peername': self.name,
                'host': self.serverhost,
                'port': self.serverport,
                'filename': filename
            }
            self.client_send(
                server_info, msgtype='FILE_REQUEST', msgdata=data)

    ##=====NEED MODIFY: Hàm này dùng để hiển thị có yêu cầu chia sẻ file để người dùng chọn đồng ý hoặc không====#
    def file_request(self, msgdata):
        """ Processing received file request message from peer. """
        peername = msgdata['peername']
        host, port = msgdata['host'], msgdata['port']
        filename = msgdata['filename']
        msg_box = tkinter.messagebox.askquestion('File Request', 'Do you want to accept {} - {}:{}?'.format(peername, host, port),
                                            icon="question")
        if msg_box == 'yes':
            # if request is agreed, connect to peer (add to friendlist)
            data = {
                'peername': self.name,
                'host': self.serverhost,
                'port': self.serverport
            }
            self.client_send((host, port), msgtype='CHAT_ACCEPT', msgdata=data)
            display_noti("Chat Request Accepted",
                         "Update to get in touch with new friend!")
            self.friendlist[peername] = (host, port)
        else:
            self.client_send((host, port), msgtype='CHAT_REFUSE', msgdata={})

    #=======Hàm này dùng để chuyển file cho máy khách sau khi đã chọn đồng ý=======#
    def file_accept(self, msgdata):
        """ Processing received accept chat request message from peer.
            Add the peer to collection of friends. """
        peername = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        display_noti("Chat Request Result",
                     'CHAT ACCEPTED: {} --- {}:{}. Update to get in touch with new friend!'.format(peername, host, port))
        self.friendlist[peername] = (host, port)

    def file_refuse(self, msgdata):
        """ Processing received refuse chat request message from peer. """
        display_noti("File Request Result", 'FILE REFUSED!')
    ## ===========================================================##
    
    def recv_public_message(self, msgdata):
        """ Processing received public chat message from central server."""
        # insert messages to text box
        message = msgdata['name'] + ": " + msgdata['message']
        app.chatroom_textCons.config(state=tkinter.NORMAL)
        app.chatroom_textCons.insert(tkinter.END, message+"\n\n")
        app.chatroom_textCons.config(state=tkinter.DISABLED)
        app.chatroom_textCons.see(tkinter.END)
    ## ===========================================================##

    # def recv_message(self, msgdata):
    #     """ Processing received chat message from peer."""
    #     friend_name = msgdata['friend_name']
    #     if friend_name in self.friendlist:
    #         # insert messages to text box
    #         message = friend_name + ": " + msgdata['message']
    #         app.frames[ChatPage].frame_list[friend_name].message_area.config(
    #             state=tk.NORMAL)
    #         app.frames[ChatPage].frame_list[friend_name].message_area.insert(
    #             tk.END, message+"\n\n")
    #         app.frames[ChatPage].frame_list[friend_name].message_area.config(
    #             state=tk.DISABLED)
    #         app.frames[ChatPage].frame_list[friend_name].message_area.see(
    #             tk.END)
    ## ===========================================================##

    ## ==========implement protocol for file tranfering==========##
    def transfer_file(self, peer, file_path):
        """ Transfer a file to friend. """
        try:
            peer_info = self.friendlist[peer]
        except KeyError:
            display_noti("File Transfer Result", 'Friend does not exist!')
        else:
            file_name = os.path.basename(file_path)
            def fileThread(filename):
                file_sent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                file_sent.connect((peer_info[0], peer_info[1]+OFFSET))

                # send filename and friendname
                fileInfo = {
                    'filename': filename,
                    'friendname': peer,
                }

                fileInfo = json.dumps(fileInfo).encode(FORMAT)
                file_sent.send(fileInfo)
                
                msg = file_sent.recv(BUFFER_SIZE).decode(FORMAT)
                print(msg)

                with open(file_path, "rb") as f:
                    while True:
                        # read the bytes from the file
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        file_sent.sendall(bytes_read)
                file_sent.shutdown(socket.SHUT_WR)
                file_sent.close()
                display_noti("File Transfer Result", 'File has been sent!')
                return
            t_sf = threading.Thread(target=fileThread,args=(file_name,))
            t_sf.daemon = True
            t_sf.start()

    def recv_file_content(self):
        """ Processing received file content from peer."""
        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to our local address
        self.file_socket.bind((self.serverhost, int(self.serverport) + OFFSET))
        self.file_socket.listen(5)

        while True:
            conn, addr = self.file_socket.accept()
            buf = conn.recv(BUFFER_SIZE)
            message = buf.decode(FORMAT)

            # deserialize (json type -> python type)
            recv_file_info = json.loads(message)

            conn.send("Filename received.".encode(FORMAT))
            print(recv_file_info)

            file_name = str(random.randint(1, 100000000))+ "_" + recv_file_info['filename']
            friend_name = recv_file_info['friendname']

            with open(file_name, "wb") as f:
                while True:
                    bytes_read = conn.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)

            conn.shutdown(socket.SHUT_WR)
            conn.close()

            display_noti("File Transfer Result", 'You receive a file with name ' + file_name + ' from ' + friend_name)
    
    ## ===========================================================##
    
    ## ==========implement protocol for log out & exit ===================##

    def send_logout_request(self):
        """ Central Server deletes user out of online user list """
        peer_info = {
            'peername': self.name,
        }
        self.client_send(self.server_info,
                         msgtype='PEER_LOGOUT', msgdata=peer_info)

    ## ===========================================================##
    def deleteFileServer(self,file_name):
        """ Delete file from server. """
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': file_name
        }
        self.client_send(self.server_info,
                         msgtype='DELETE_FILE', msgdata=peer_info)
        
    def updateToServer(self,file_name):
        """ Upload repo to server. """
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': file_name
        }
        self.client_send(self.server_info,
                         msgtype='FILE_REPO', msgdata=peer_info)


# ------ app run ---------- #
app = tkinterApp()
app.title('P2P File Sharing')
app.geometry("1024x600")
app.resizable(False, False)

def handle_on_closing_event():
    if tkinter.messagebox.askokcancel("Thoát", "Bạn muốn thoát khỏi ứng dụng?"):
        app.destroy()

app.protocol("WM_DELETE_WINDOW", handle_on_closing_event)
app.mainloop()