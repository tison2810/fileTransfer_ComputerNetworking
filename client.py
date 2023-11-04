import os
import json
import socket
import threading
import time
import random
from Base import Base
 
# GUI
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from PIL import ImageTk 

# aid
from hashfunction import MD5_hash
import asset

# ----CONSTANT----#
FORMAT = "utf-8"
BUFFER_SIZE = 2048
OFFSET = 10000

## ====================GUI IMPLEMENT======================##


def display_noti(title, content):
    tkinter.messagebox.showinfo(title, content)


class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.chatroom_textCons = None

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, RegisterPage, LoginPage):
            frame = F(container, self)
            # initializing frame of that object from
            # startpage, registerpage, loginpage, chatpage respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg='white')
        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="ShareFile", bg="#bf8bff", fg="white",
                 height="2", font=("Verdana", 18)).pack(fill='x')
        tk.Label(self, text="", bg='white').pack()

        # Set port label
        tk.Label(self, text="Set Port (1024 -> 65535)", bg='white').pack()
        # Set port entry
        self.port_entry = tk.Entry(
            self, width="20", font=("Verdana", 11))
        self.port_entry.pack()
        tk.Label(self, text="", bg='white').pack()

        # create a register button
        tk.Button(self, text="Đăng ký", height="2", width="30", bg="#5D0CB5", fg="white", command=lambda: self.enter_app(
            controller=controller, port=self.port_entry.get(), page=RegisterPage)).pack()
        tk.Label(self, text="", bg='white').pack()

        # create a login button
        tk.Button(self, text="Đăng nhập", height="2", width="30", bg="#A021E2", fg="white", command=lambda: self.enter_app(
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
            self.port_entry.delete(0, tk.END)
            display_noti("Port Error!",  "Cổng đã được sử dụng hoặc chứa giá trị rỗng")


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Sign Up Image
        signup_pic = ImageTk.PhotoImage(asset.signup_image)
        signupImg = tk.Label(self, image=signup_pic, bg='white')
        signupImg.image = signup_pic
        signupImg.place(x=50, y=50)

        # Title
        tk.Label(self, text='Đăng ký',
                 fg='#bf8bff', bg='white',
                 font=("Roboto", 24, 'bold')).place(x=670, y=100)
        # Username
        tk.Label(self, text='Tên đăng nhập', bg='white',
                 fg='#57a1f8', font=("Roboto", 11)).place(x=670, y=175)
        self.username_entry = tk.Entry(self, width=25, fg='black', border=0,
                                       bg='white', font=("Roboto", 10))
        self.username_entry.place(x=675, y=200)
        tk.Frame(self, width=275, height=2, bg='#777777').place(x=675, y=225)

        # Password
        tk.Label(self, text='Mật khẩu', bg='white',
                 fg='#57a1f8', font=("Roboto", 11)).place(x=670, y=250)
        self.password_entry = tk.Entry(self, width=25, fg='black', border=0,
                                       bg='white', font=("Roboto", 10), show='*')
        self.password_entry.place(x=675, y=275)
        tk.Frame(self, width=275, height=2, bg='#777777').place(x=675, y=300)

        # Submit
        tk.Button(self, width=39, pady=7, text='Đăng ký', bg='#bf8bff',
                  fg='white', border=0, command=lambda: self.register_user(self.username_entry.get(), self.password_entry.get())).place(x=675, y=325)
        tk.Label(self, text="Đã có tài khoản ?",
                 fg='black', bg='white', font=("Roboto", 10)).place(x=675, y=375)
        tk.Button(self, width=6, text='Đăng nhập', border=0,
                  bg='white', cursor='hand2', fg='#57a1f8', command=lambda: controller.show_frame(LoginPage)).place(x=670, y=400)

    def register_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        network_peer.send_register()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Login Image
        login_pic = ImageTk.PhotoImage(asset.login_image)
        loginImg = tk.Label(self, image=login_pic, bg='white')
        loginImg.image = login_pic
        loginImg.place(x=50, y=50)

        # Title
        tk.Label(self, text='Đăng nhập',
                 fg='#bf8bff', bg='white',
                 font=("Roboto", 24, 'bold')).place(x=670, y=100)

        # Username
        tk.Label(self, text='Tên đăng nhập', bg='white',
                 fg='#57a1f8', font=("Roboto", 11)).place(x=670, y=175)
        self.username_entry = tk.Entry(self, width=25, fg='black', border=0,
                                       bg='white', font=("Roboto", 10))
        self.username_entry.place(x=675, y=200)
        tk.Frame(self, width=275, height=2, bg='#777777').place(x=675, y=225)

        # Password
        tk.Label(self, text='Mật khẩu', bg='white',
                 fg='#57a1f8', font=("Roboto", 11)).place(x=670, y=250)
        self.password_entry = tk.Entry(self, width=25, fg='black', border=0,
                                       bg='white', font=("Roboto", 10), show='*')
        self.password_entry.place(x=675, y=275)
        tk.Frame(self, width=275, height=2, bg='#777777').place(x=675, y=300)

        # Submit
        tk.Button(self, width=39, pady=7, text='Đăng nhập', bg='#bf8bff',
                  fg='white', border=0, command=lambda: self.login_user(username=self.username_entry.get(), password=self.password_entry.get())).place(x=675, y=325)
        tk.Label(self, text="Bạn không có tài khoản ?",
                 fg='black', bg='white', font=("Roboto", 10)).place(x=675, y=375)
        tk.Button(self, width=6, text='Đăng ký', border=0,
                  bg='white', cursor='hand2', fg='#57a1f8', command=lambda: controller.show_frame(RegisterPage)).place(x=670, y=400)

    def login_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        network_peer.send_login()

class NetworkPeer(Base):
    def __init__(self, serverhost='localhost', serverport=30000, server_info=('192.168.1.155', 40000)):
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
        app.show_frame(ChatPage)

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
        msg_box = tk.messagebox.askquestion('File Request', 'Do you want to accept {} - {}:{}?'.format(peername, host, port),
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
        app.chatroom_textCons.config(state=tk.NORMAL)
        app.chatroom_textCons.insert(tk.END, message+"\n\n")
        app.chatroom_textCons.config(state=tk.DISABLED)
        app.chatroom_textCons.see(tk.END)
    ## ===========================================================##

    def recv_message(self, msgdata):
        """ Processing received chat message from peer."""
        friend_name = msgdata['friend_name']
        if friend_name in self.friendlist:
            # insert messages to text box
            message = friend_name + ": " + msgdata['message']
            app.frames[ChatPage].frame_list[friend_name].message_area.config(
                state=tk.NORMAL)
            app.frames[ChatPage].frame_list[friend_name].message_area.insert(
                tk.END, message+"\n\n")
            app.frames[ChatPage].frame_list[friend_name].message_area.config(
                state=tk.DISABLED)
            app.frames[ChatPage].frame_list[friend_name].message_area.see(
                tk.END)
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

## ===========================================================##
## ===========================================================##
app = tkinterApp()
app.title('Share File')
app.geometry("1024x600")
app.resizable(False, False)

def handle_on_closing_event():
    if tkinter.messagebox.askokcancel("Thoát", "Bạn muốn thoát khỏi ứng dụng?"):
        app.destroy()

app.protocol("WM_DELETE_WINDOW", handle_on_closing_event)
app.mainloop()
