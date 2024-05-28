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

def on_submit():
    accession_id = textbox.get()
    gene_data, extracted_info, title = fetch_genbank_data(accession_id)
    display_data(gene_data, extracted_info, title)

def display_data(gene_data, extracted_info, title):
    for widget in result_frame.winfo_children():
        widget.destroy()

    title_label = CTkLabel(master=result_frame, text=f"Source and definition: {title}", font=("Helvetica", 14))
    title_label.pack(anchor="w", pady=2)

    for key, value in gene_data.items():
        label = CTkLabel(master=result_frame, text=f"{key.capitalize()}: {value}", font=("Helvetica", 12))
        label.pack(anchor="w", pady=2)

    if extracted_info['source']:
        source_label = CTkLabel(master=result_frame, text=f"Source: {extracted_info['source']['range']}", font=("Helvetica", 12))
        source_label.pack(anchor="w", pady=2)
        details_label = CTkLabel(master=result_frame, text=extracted_info['source']['details'], font=("Helvetica", 12))
        details_label.pack(anchor="w", pady=2)

    if extracted_info['mRNA']:
        mrna_label = CTkLabel(master=result_frame, text="mRNA Details", font=("Helvetica", 14))
        mrna_label.pack(anchor="w", pady=2)
        mrna_range = CTkLabel(master=result_frame, text=f"Range: {extracted_info['mRNA']['range']}", font=("Helvetica", 12))
        mrna_range.pack(anchor="w", pady=2)
        mrna_product = CTkLabel(master=result_frame, text=f"Product: {extracted_info['mRNA']['product']}", font=("Helvetica", 12))
        mrna_product.pack(anchor="w", pady=2)

    if extracted_info['CDS']:
        cds_label = CTkLabel(master=result_frame, text="CDS Details", font=("Helvetica", 14))
        cds_label.pack(anchor="w", pady=2)
        cds_range = CTkLabel(master=result_frame, text=f"Range: {extracted_info['CDS']['range']}", font=("Helvetica", 12))
        cds_range.pack(anchor="w", pady=2)
        cds_details = CTkLabel(master=result_frame, text=extracted_info['CDS']['details'], font=("Helvetica", 12))
        cds_details.pack(anchor="w", pady=2)

app = CTk()
app.geometry("600x600")
checkbox_frame = CTkFrame(master=app)
checkbox_frame.pack(pady=20)

label = CTkLabel(master=app, text="Welcome to BioScrape", font=("Helvetica", 20), text_color="#EAECEE")
label.pack(pady=10)

textbox = CTkEntry(master=app, width=300)
textbox.insert(0, "Enter your molecule")
textbox.bind("<FocusIn>", on_entry_click)
textbox.bind("<FocusOut>", on_focus_out)
textbox.pack(pady=10)

btn = CTkButton(master=app, text="Submit", corner_radius=3, hover_color="#4158D0", command=on_submit)
btn.pack(pady=10)

result_frame = CTkFrame(master=app)
result_frame.pack(pady=20, fill="both", expand=True)

set_appearance_mode("dark")
app.mainloop()
