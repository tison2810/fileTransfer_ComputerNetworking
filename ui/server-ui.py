import tkinter
import tkinter.messagebox
import tkinter.filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from PIL import ImageTk
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

#popup notification
def display_noti(title, content):
    tkinter.messagebox.showinfo(title, content)

#define color scheme
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

#class for main app
# class tkinterApp(tk.Tk):
#     # __init__ function for class tkinterApp
#     def __init__(self, *args, **kwargs):
#         # __init__ function for class Tk
#         tk.Tk.__init__(self, *args, **kwargs)

#         # creating a container
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         self.chatroom_textCons = None

#         # initializing frames to an empty array
#         self.frames = {}

#         # iterating through a tuple consisting
#         # of the different page layouts
#         for F in (StartPage, RegisterPage, LoginPage, RepoPage):
#             frame = F(container, self)
#             # initializing frame of that object from
#             # startpage, registerpage, loginpage, chatpage respectively with
#             # for loop
#             self.frames[F] = frame
#             frame.grid(row=0, column=0, sticky="nsew")
#             frame.configure(bg='white')
#         self.show_frame(StartPage)

#     # to display the current frame passed as
#     # parameter
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
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
        # self.scrollable_frame_switches = []
        self.scrollable_clients_names = []
        ## to do: modify range to number of current clients
        for i in range(100):
            # switch = customtkinter.CTkSwitch(master=self.scrollable_clients_frame, text=f"CTkSwitch {i}")
            # switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            # self.scrollable_frame_switches.append(switch)
            client_label = customtkinter.CTkLabel(master=self.scrollable_clients_frame, text="Client's Name")
            client_label.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_clients_names.append(client_label)
            view_button = customtkinter.CTkButton(master=self.scrollable_clients_frame, text="View Files", command=self.view_client_files)
            view_button.grid(row=i, column=1, padx=10, pady=(0, 20))
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

    ## to do:
    def view_client_files():
        print("button pressed")

    ## to do:
    def ping_client():
        print("button pressed")


# def discover_clients():
#     # Add code to send 'discover' command to your network application
#     clients_list = []  # Replace with actual list of connected clients
#     result_text.set("\n".join(clients_list))

# def ping_clients():
#     # Add code to send 'ping' command to your network application
#     result_text.set("Ping sent")

# app = tk.Tk()
# app = tkinterApp()
# app.title("Network Application")

# result_text = tk.StringVar()

# frame = tk.Frame(app)
# frame.pack()

# discover_button = tk.Button(frame, text="Discover", command=discover_clients)
# discover_button.pack()

# ping_button = tk.Button(frame, text="Ping", command=ping_clients)
# ping_button.pack()

# result_label = tk.Label(frame, textvariable=result_text)
# result_label.pack()

# app.mainloop()

app = App()
app.title('P2P File Sharing')
app.geometry("1024x600")
app.resizable(False, False)

def handle_on_closing_event():
    if tkinter.messagebox.askokcancel("Thoát", "Bạn muốn thoát khỏi ứng dụng?"):
        app.destroy()

app.protocol("WM_DELETE_WINDOW", handle_on_closing_event)
app.mainloop()