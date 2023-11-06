import tkinter
import customtkinter

def upload_file():
    try:
        f = file.get()
        finishLabel.configure(text="Uploaded!")
    except:
        finishLabel.configure(text="Upload Error!")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_uploaded = total_size - bytes_remaining;
    percentage = bytes_uploaded / total_size * 100
    per = str(int(percentage))
    pPer.configure(text=per + '%')
    pPer.update()

    pBar.set(float(percentage) / 100)

#System settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Progress Bar")

#UI elements
title = customtkinter.CTkLabel(app, text="Choose a file to transfer")
title.pack(padx=20, pady=20)

#File input
url_var = tkinter.StringVar()
file = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
file.pack()

#Button
#to do: define upload_file
upload = customtkinter.CTkButton(app, text="Upload", command=upload_file)
upload.pack(padx=20, pady=20)

#Finish uploading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

#Progress percentage
pPer = customtkinter.CTkLabel(app, text="0%")
pPer.pack()

pBar = customtkinter.CTkProgressBar(app, width=400)
pBar.set(0.5)
pBar.pack(pady=10, padx=10)


#App run
app.mainloop()