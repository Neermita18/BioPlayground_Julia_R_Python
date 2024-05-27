from customtkinter import *
from tkinter import *
from scrape_genbank import fetch_genbank_data

def on_entry_click(event):
    if textbox.get() == "Enter your molecule":
        textbox.delete(0, "end")
        textbox.configure(text_color='white')  # Change text color to black

def on_focus_out(event):
    if textbox.get() == "":
        textbox.insert(0, "Enter your molecule")
        textbox.configure(text_color='grey')  # Change text color to grey

app = CTk()
app.geometry("300x500")
checkbox_frame = CTkFrame(master=app)

checkbox_frame.place(relx=0.5, rely=0.2, anchor="center")
label = CTkLabel(master=app, text="Welcome to BioScrape", font=("Helvetica", 20), text_color="#EAECEE")
label.place(relx=0.5, rely=0.2, anchor="center")

textbox = CTkEntry(master=app)
textbox.insert(0, "Enter your molecule")

textbox.bind("<FocusIn>", on_entry_click)
textbox.bind("<FocusOut>", on_focus_out)
textbox.place(relx=0.5, rely=0.35, anchor="center")

btn = CTkButton(master=app, text="Submit", corner_radius=3, hover_color="#4158D0")
btn.place(relx=0.5, rely=0.5, anchor="center")

set_appearance_mode("dark")
app.mainloop()
