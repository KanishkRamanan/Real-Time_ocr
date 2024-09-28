import tkinter as tk
from tkinter import scrolledtext
import threading
from webcam_ocr import start_ocr_detection

# Create the main GUI window using Tkinter
root = tk.Tk()
root.title("Real-Time OCR Detection")

# Add a label to guide the user
label = tk.Label(root, text="Click 'Start OCR' to begin real-time text detection.")
label.pack(pady=10)

# Add a scrolled text area to display OCR results
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
text_area.pack(padx=10, pady=10)

# Function to update the text area in the GUI with detected text
def update_text(ocr_text):
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, ocr_text)

# Function to run the OCR detection in a separate thread
def start_ocr_thread():
    threading.Thread(target=start_ocr_detection, args=(update_text,)).start()  # Passing the update_text callback

# Add a button to start OCR detection
start_button = tk.Button(root, text="Start OCR", command=start_ocr_thread)
start_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
