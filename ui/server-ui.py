import tkinter
import tkinter.messagebox
import tkinter.filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from PIL import ImageTk
import customtkinter

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

app = App()
app.title('P2P File Sharing')
app.geometry("1024x600")
app.resizable(False, False)

def handle_on_closing_event():
    if tkinter.messagebox.askokcancel("Thoát", "Bạn muốn thoát khỏi ứng dụng?"):
        app.destroy()

app.protocol("WM_DELETE_WINDOW", handle_on_closing_event)
app.mainloop()