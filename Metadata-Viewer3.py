import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import exifread
import os
import datetime
import re

metadata_report_text = ""  # لتخزين تقرير الميتاداتا للنص

def extract_basic_metadata(filepath):
    metadata = {}
    stat = os.stat(filepath)
    metadata['File Name'] = os.path.basename(filepath)
    metadata['File Size'] = f"{round(stat.st_size / 1024)} KB"
    metadata['File Type'] = os.path.splitext(filepath)[1][1:].lower()
    metadata['Last Modified'] = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    return metadata

def extract_exifread_metadata(filepath):
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, details=False)
        return {str(k): str(v) for k, v in tags.items()}
    except Exception as e:
        return {"EXIF Read Error": str(e)}

def extract_icc_profile(image):
    if image.info.get("icc_profile"):
        return {"ICC Profile": "Embedded"}
    return {}

def extract_xmp_metadata(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        matches = re.findall(b'<\?xpacket[^>]*\?>.*?<\?xpacket end=[\'\"]w[\'\"]\?>', data, re.DOTALL)
        xml_blocks = []
        for match in matches:
            try:
                xml_blocks.append(match.decode('utf-8', errors='ignore'))
            except:
                continue
        return xml_blocks
    except Exception as e:
        return [f"XMP/XML Error: {str(e)}"]

def open_image():
    global metadata_report_text

    filepath = filedialog.askopenfilename(
        filetypes=[("All image files", "*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp;*.gif;*.webp")]
    )
    if not filepath:
        return

    try:
        image = Image.open(filepath)
    except Exception as e:
        metadata_text.config(state='normal')
        metadata_text.delete(1.0, tk.END)
        metadata_text.insert(tk.END, f"Error opening image: {str(e)}")
        metadata_text.config(state='disabled')
        return

    image.thumbnail((600, 600))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

    # استخراج البيانات
    basic_meta = extract_basic_metadata(filepath)
    exif_meta = extract_exifread_metadata(filepath)
    icc_meta = extract_icc_profile(image)
    xmp_blocks = extract_xmp_metadata(filepath)

    # تنسيق البيانات
    display_text = "=== Basic File Metadata ===\n"
    display_text += "\n".join(f"{k}: {v}" for k, v in basic_meta.items())

    display_text += "\n\n=== EXIF Metadata (via exifread) ===\n"
    if exif_meta:
        display_text += "\n".join(f"{k}: {v}" for k, v in exif_meta.items())
    else:
        display_text += "(No EXIF metadata found)"

    if icc_meta:
        display_text += "\n\n=== ICC Profile ===\n"
        display_text += "\n".join(f"{k}: {v}" for k, v in icc_meta.items())

    if xmp_blocks:
        for i, block in enumerate(xmp_blocks):
            display_text += f"\n\n=== XMP Metadata Block {i+1} ===\n{'-'*40}\n{block}"

    metadata_report_text = display_text  # تخزين النص للحفظ لاحقًا

    metadata_text.config(state='normal')
    metadata_text.delete(1.0, tk.END)
    metadata_text.insert(tk.END, display_text)
    metadata_text.config(state='disabled')

def save_metadata_report():
    if not metadata_report_text.strip():
        messagebox.showwarning("No Data", "There is no metadata to save.")
        return

    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")],
                                             title="Save Metadata Report")
    if filepath:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(metadata_report_text)
            messagebox.showinfo("Saved", f"Metadata report saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save the file:\n{str(e)}")

# واجهة المستخدم
root = tk.Tk()
root.title("Metadata Viewer")
root.configure(bg='#f5f0e6')

header = tk.Label(root, text="Metadata Viewer", font=("Arial", 16, "bold"), bg='#f5f0e6')
header.pack(pady=5)

main_frame = tk.Frame(root, bg='#f5f0e6')
main_frame.pack(padx=10, pady=5)

image_label = tk.Label(main_frame, bg='#f5f0e6')
image_label.pack(side='right', padx=10)

metadata_text = tk.Text(main_frame, width=60, height=35, wrap='word', font=("Arial", 10), bg='#fff9f0')
metadata_text.pack(side='left', padx=10)
metadata_text.config(state='disabled')

btn_open = tk.Button(root, text="Open Image", command=open_image, bg='#c9a066', fg='white', font=("Arial", 10, "bold"))
btn_open.pack(pady=5)

btn_save = tk.Button(root, text="Save Report", command=save_metadata_report,
                     bg='#6b8e23', fg='white', font=("Arial", 10, "bold"))
btn_save.pack(pady=5)

footer = tk.Label(root, text="By: The Cataloger\nmanuscriptscataloger@gmail.com", font=("Arial", 9), bg='#f5f0e6', fg='gray')
footer.pack(pady=5)

root.mainloop()
