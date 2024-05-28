from customtkinter import *
from tkinter import *
from scrape_genbank import fetch_genbank_data

def on_entry_click(event):
    if textbox.get() == "Enter your molecule":
        textbox.delete(0, "end")
        textbox.configure(text_color='white')

def on_focus_out(event):
    if textbox.get() == "":
        textbox.insert(0, "Enter your molecule")
        textbox.configure(text_color='grey')

def on_submit():
    accession_id = textbox.get()
    gene_data, extracted_info, title = fetch_genbank_data(accession_id)
    display_data(gene_data, extracted_info, title)

def clean_text(text):
    cleaned_text = ' '.join(text.split())
    return cleaned_text.replace('"', '')

def display_data(gene_data, extracted_info, title):
    for widget in result_frame.winfo_children():
        widget.destroy()

    title_label = CTkLabel(master=result_frame, text="Source and definition", font=("Helvetica", 14, "bold"), bg_color="#444444", text_color="#FFFFFF")
    title_label.pack(anchor="w", pady=2, padx=10, fill="x")

    for key, value in gene_data.items():
        label = CTkLabel(master=result_frame, text=f"{key.capitalize()}: {clean_text(value)}", font=("Helvetica", 12), wraplength=result_frame.winfo_width())
        label.pack(anchor="w", pady=2, padx=10, fill="x")

    if extracted_info.get('source'):
        source_heading = CTkLabel(master=result_frame, text="Source Details", font=("Helvetica", 14, "bold"), bg_color="#444444", text_color="#FFFFFF", wraplength=result_frame.winfo_width())
        source_heading.pack(anchor="w", pady=2, padx=10, fill="x")

        source_range = CTkLabel(master=result_frame, text=f"Range: {clean_text(extracted_info['source']['range'])}", font=("Helvetica", 12), wraplength=result_frame.winfo_width())
        source_range.pack(anchor="w", pady=2, padx=10, fill="x")
        
        source_details = extracted_info['source']['details']
        source_details_lines = source_details.split("                     ")
        for detail in source_details_lines:
            detail = detail.strip()
            if detail:
                detail_label = CTkLabel(master=result_frame, text=clean_text(detail), font=("Helvetica", 12), wraplength=result_frame.winfo_width())
                detail_label.pack(anchor="w", pady=2, padx=10, fill="x")

    if extracted_info.get('mRNA'):
        mrna_label = CTkLabel(master=result_frame, text="mRNA Details", font=("Helvetica", 14, "bold"), bg_color="#555555", text_color="#FFFFFF", wraplength=result_frame.winfo_width())
        mrna_label.pack(anchor="w", pady=2, padx=10, fill="x")
        mrna_range = CTkLabel(master=result_frame, text=f"Range: {clean_text(extracted_info['mRNA']['range'])}", font=("Helvetica", 12), wraplength=result_frame.winfo_width())
        mrna_range.pack(anchor="w", pady=2, padx=10, fill="x")
        mrna_product = CTkLabel(master=result_frame, text=f"Product: {clean_text(extracted_info['mRNA']['product'])}", font=("Helvetica", 12), wraplength=result_frame.winfo_width())
        mrna_product.pack(anchor="w", pady=2, padx=10, fill="x")

    if extracted_info.get('CDS'):
        cds_label = CTkLabel(master=result_frame, text="CDS Details", font=("Helvetica", 14, "bold"), bg_color="#666666", text_color="#FFFFFF", wraplength=result_frame.winfo_width())
        cds_label.pack(anchor="w", pady=2, padx=10, fill="x")

        cds_details = extracted_info['CDS']['details'].split("                     ")
        cds_details = [clean_text(detail.strip()) for detail in cds_details if detail.strip()]
        for detail in cds_details:
            detail_label = CTkLabel(master=result_frame, text=detail, font=("Helvetica", 12), wraplength=result_frame.winfo_width())
            detail_label.pack(anchor="w", pady=2, padx=10, fill="x")

app = CTk()
app.geometry("600x600")

label = CTkLabel(master=app, text="Welcome to BioScrape", font=("Helvetica", 20), text_color="#EAECEE")
label.pack(pady=10)

textbox = CTkEntry(master=app, width=300)
textbox.insert(0, "Enter your molecule")
textbox.bind("<FocusIn>", on_entry_click)
textbox.bind("<FocusOut>", on_focus_out)
textbox.pack(pady=10)

btn = CTkButton(master=app, text="Submit", corner_radius=3, hover_color="#4158D0", command=on_submit)
btn.pack(pady=10)

result_container = CTkFrame(master=app)
result_container.pack(pady=20, fill="both", expand=True)

canvas = Canvas(result_container, bg="#2A2D2E", bd=0, highlightthickness=0)
scrollbar = CTkScrollbar(master=result_container, orientation="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.configure(yscrollcommand=scrollbar.set)

result_frame = CTkFrame(master=canvas)
result_frame_id = canvas.create_window((0, 0), window=result_frame, anchor="center")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

result_frame.bind("<Configure>", on_configure)

def on_canvas_resize(event):
    canvas_width = event.width
    canvas_height = event.height
    canvas.itemconfig(result_frame_id, width=canvas_width - 20)  # Adjust for padding
    canvas.coords(result_frame_id, canvas_width / 2, canvas_height / 2)

canvas.bind("<Configure>", on_canvas_resize)

set_appearance_mode("dark")
app.mainloop()
