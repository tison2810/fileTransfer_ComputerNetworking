import tkinter
import tkinter.messagebox
import tkinter.filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from PIL import ImageTk
import customtkinter

# customtkinter.set_appearance_mode("System")
# customtkinter.set_default_color_theme("dark-blue")

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
        self.scrollable_files_frame.grid(row=0, column=0, rowspan=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
        
        self.scrollable_clients_files = []
        for i in range(100):
            client_label = customtkinter.CTkLabel(master=self.scrollable_files_frame, text="File's Name")
            client_label.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_clients_files.append(client_label)

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        ### create frame for REPO
        self.repo_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.repo_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.repo_frame.grid_rowconfigure(0, weight=1)
        self.repo_frame.grid_columnconfigure(0, weight=1)
        # create scrollable frame for repo list
        ## to do: add file names to this frame
        self.scrollable_repo_frame = customtkinter.CTkScrollableFrame(self.repo_frame, label_text="Repository")
        self.scrollable_repo_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_repo_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_file_names = []
        ## to do: modify range to number of current files
        for i in range(100):
            file = customtkinter.CTkLabel(master=self.scrollable_repo_frame, text="File's Name")
            file.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_file_names.append(file)
        # create listbox
        repo_items = ["hehe", "huhu", "hihi"] ##### to be replaced with scrollable_peer_names after adding to list
        self.repo_list = customtkinter.CTkComboBox(self.repo_frame, values=repo_items, command=self.listbox_callback)
        self.repo_list.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create temp frame
        self.temp_frame = customtkinter.CTkFrame(master=self.repo_frame, fg_color="transparent")
        self.temp_frame.grid(row=2, column=0, sticky="nsew")
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
        self.update_button.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create reload repo button
        self.update_button = customtkinter.CTkButton(master=self.repo_frame, border_width=2, text="Reload Repo")
        self.update_button.grid(row=4, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")


        # create frame for peer list
        self.peer_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.peer_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.peer_frame.grid_rowconfigure(0, weight=1)
        self.peer_frame.grid_columnconfigure(0, weight=1)
        # create scrollable peer list
        ## to do: add peer names to this frame
        self.scrollable_peer_frame = customtkinter.CTkScrollableFrame(self.peer_frame, label_text="Peer List")
        self.scrollable_peer_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_peer_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_peer_names = []
        ## to do: modify range to number of current peers
        for i in range(100):
            peer = customtkinter.CTkLabel(master=self.scrollable_peer_frame, text="Peer's Name")
            peer.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_peer_names.append(peer)
        # create listbox
        list_items = ["hehe", "huhu", "hihi"] ##### to be replaced with scrollable_peer_names after adding to list
        self.list_box = customtkinter.CTkComboBox(self.peer_frame, values=list_items, command=self.listbox_callback)
        self.list_box.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create search for file
        self.search_frame = customtkinter.CTkFrame(self.peer_frame, fg_color="transparent")
        self.search_frame.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.search_frame.grid_rowconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_entry = customtkinter.CTkEntry(master=self.search_frame, placeholder_text="Search...")
        self.search_entry.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.search_button = customtkinter.CTkButton(master=self.search_frame, text="Search", border_width=2)
        self.search_button.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        # create send connect request button
        self.request_button = customtkinter.CTkButton(master=self.peer_frame, border_width=2,
                                                     command=lambda:self.chooseFile(), text="Send Connect Request")
        self.request_button.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # create CLI
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Command...")
        self.entry.grid(row=4, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # self.main_button_1 = customtkinter.CTkButton(master=self, text="Enter", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        # self.main_button_1.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    # def sendFile(self, friend_name):
    #     file_path = tkinter.filedialog.askopenfilename(initialdir="/",
    #                                                    title="Select a File",
    #                                                    filetypes=(("All files", "*.*"),))
    #     file_name = os.path.basename(file_path)
    #     msg_box = tkinter.messagebox.askquestion('File Explorer', 'Are you sure to send {} to {}?'.format(file_name, friend_name),
    #                                              icon="question")
    #     if msg_box == 'yes':
    #         sf_t = threading.Thread(
    #             target=network_peer.transfer_file, args=(self.friend_name, file_path))
    #         sf_t.daemon = True
    #         sf_t.start()
    #         tkinter.messagebox.showinfo(
    #             "File Transfer", '{} has been sent to {}!'.format(file_name, friend_name))

    # def chooseFile(self):
    #     file_path = tkinter.filedialog.askopenfilename(initialdir="/",
    #                                                    title="Select a File",
    #                                                    filetypes=(("All files", "*.*"),))
    #     # file_name = os.path.basename(file_path)
    #     file_name = file_path
    #     msg_box = tkinter.messagebox.askquestion('File Explorer', 'Upload {} to local repository?'.format(file_name),
    #                                              icon="question")
    #     if msg_box == 'yes':
    #         popup = simpledialog.askstring("Input","Nhập tên file trên Localrepo",parent = self)
    #         file_name = popup + "(" + file_name + ")"
    #         self.Scrolledlistbox1.insert(0,file_name)
    #         tkinter.messagebox.showinfo(
    #             "Local Repository", '{} has been added to localrepo!'.format(file_name))
    
    # def deleteSelectedFile(self):
    #     file_name = self.Scrolledlistbox1.get(customtkinter.ANCHOR)
    #     self.Scrolledlistbox1.delete(customtkinter.ANCHOR)
    #     network_peer.deleteFileServer(file_name)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    ## to do: stop server
    def sidebar_button_event(self):
        print("huhu")

    ## to do: 
    def listbox_callback():
        print("done")

        

app = App()
app.title('P2P File Sharing')
app.geometry("1024x600")
app.resizable(False, False)

# def handle_on_closing_event():
#     if tkinter.messagebox.askokcancel("Thoát", "Bạn muốn thoát khỏi ứng dụng?"):
#         app.destroy()

# app.protocol("WM_DELETE_WINDOW", handle_on_closing_event)
app.mainloop()
