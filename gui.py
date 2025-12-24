import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import sys
import os
import time

# Import functionalities from existing scripts
# We need to make sure we can import them. 
# Assuming they are in the same directory.
try:
    from encode import create_video
    from decode_video import decode_video
    from youtube_decode import youtube_decode
    from common import global_reedEC, global_gridSize
except ImportError as e:
    print(f"Error importing modules: {e}")
    # Fallback to prevent immediate crash if dependencies aren't set up yet
    global_reedEC = 10
    global_gridSize = 256

    def create_video(*args, **kwargs): print("Mock create_video")
    def decode_video(*args, **kwargs): print("Mock decode_video")
    def youtube_decode(*args, **kwargs): print("Mock youtube_decode")
    
import cv2 # needed for decode wrapper

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        try:
            self.widget.configure(state="normal")
            self.widget.insert("end", str, (self.tag,))
            self.widget.see("end")
            self.widget.configure(state="disabled")
        except Exception:
            # Widget likely destroyed
            pass
    
    def flush(self):
        pass

class File2VideoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File2Video GUI")
        self.geometry("800x600")
        
        # Theme basics
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Tab View
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_view.add("Encode")
        self.tab_view.add("Decode")
        self.tab_view.add("YouTube")

        self.setup_encode_tab()
        self.setup_decode_tab()
        self.setup_youtube_tab()
        
        # Log Area
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.grid_rowconfigure(1, weight=1) # Make log expanding
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)
        
        self.log_label = ctk.CTkLabel(self.log_frame, text="Logs & Progress", anchor="w")
        self.log_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.log_text = ctk.CTkTextbox(self.log_frame, font=("Consolas", 12))
        self.log_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.log_text.configure(state="disabled")

        # Redirect stdout/stderr
        sys.stdout = TextRedirector(self.log_text, "stdout")
        sys.stderr = TextRedirector(self.log_text, "stderr")

    def setup_encode_tab(self):
        tab = self.tab_view.tab("Encode")
        tab.grid_columnconfigure(1, weight=1)

        # Source File
        ctk.CTkLabel(tab, text="Source File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.enc_src_entry = ctk.CTkEntry(tab)
        self.enc_src_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(tab, text="Browse", width=100, command=self.browse_enc_src).grid(row=0, column=2, padx=10, pady=10)

        # Output Video
        ctk.CTkLabel(tab, text="Output Video:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.enc_out_entry = ctk.CTkEntry(tab)
        self.enc_out_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(tab, text="Browse", width=100, command=self.browse_enc_out).grid(row=1, column=2, padx=10, pady=10)

        # Settings
        ctk.CTkLabel(tab, text="ReedEC (Default: 10):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.enc_reed_entry = ctk.CTkEntry(tab, placeholder_text=str(global_reedEC))
        self.enc_reed_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(tab, text="Grid Size (Default: 270):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.enc_grid_entry = ctk.CTkEntry(tab, placeholder_text=str(global_gridSize))
        self.enc_grid_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Action
        self.enc_btn = ctk.CTkButton(tab, text="Start Encoding", fg_color="green", hover_color="darkgreen", command=self.start_encoding)
        self.enc_btn.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

    def setup_decode_tab(self):
        tab = self.tab_view.tab("Decode")
        tab.grid_columnconfigure(1, weight=1)

        # Source Video
        ctk.CTkLabel(tab, text="Source Video:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.dec_src_entry = ctk.CTkEntry(tab)
        self.dec_src_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(tab, text="Browse", width=100, command=self.browse_dec_src).grid(row=0, column=2, padx=10, pady=10)

        # Destination Folder
        ctk.CTkLabel(tab, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.dec_dest_entry = ctk.CTkEntry(tab)
        self.dec_dest_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(tab, text="Browse", width=100, command=self.browse_dec_dest).grid(row=1, column=2, padx=10, pady=10)

        # Action
        self.dec_btn = ctk.CTkButton(tab, text="Start Decoding", fg_color="green", hover_color="darkgreen", command=self.start_decoding)
        self.dec_btn.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

    def setup_youtube_tab(self):
        tab = self.tab_view.tab("YouTube")
        tab.grid_columnconfigure(1, weight=1)

        # URL
        ctk.CTkLabel(tab, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.yt_url_entry = ctk.CTkEntry(tab)
        self.yt_url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Destination Folder
        ctk.CTkLabel(tab, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.yt_dest_entry = ctk.CTkEntry(tab)
        self.yt_dest_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(tab, text="Browse", width=100, command=self.browse_yt_dest).grid(row=1, column=2, padx=10, pady=10)

        # Action
        self.yt_btn = ctk.CTkButton(tab, text="Download & Decode", fg_color="red", hover_color="darkred", command=self.start_youtube)
        self.yt_btn.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="ew")


    # Browsing Helpers
    def browse_enc_src(self):
        file = filedialog.askopenfilename()
        if file:
            self.enc_src_entry.delete(0, "end")
            self.enc_src_entry.insert(0, file)
            # Auto-suggest output
            if not self.enc_out_entry.get():
                self.enc_out_entry.insert(0, file + ".mp4")

    def browse_enc_out(self):
        file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Video", "*.mp4")])
        if file:
            self.enc_out_entry.delete(0, "end")
            self.enc_out_entry.insert(0, file)

    def browse_dec_src(self):
        file = filedialog.askopenfilename(filetypes=[("MP4 Video", "*.mp4"), ("All Files", "*.*")])
        if file:
            self.dec_src_entry.delete(0, "end")
            self.dec_src_entry.insert(0, file)
            # Auto-suggest output folder
            if not self.dec_dest_entry.get():
               self.dec_dest_entry.insert(0, os.path.dirname(file))

    def browse_dec_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dec_dest_entry.delete(0, "end")
            self.dec_dest_entry.insert(0, folder)
    
    def browse_yt_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.yt_dest_entry.delete(0, "end")
            self.yt_dest_entry.insert(0, folder)

    # Logic execution
    def get_params(self, tab="encode"):
        try:
            reed = int(self.enc_reed_entry.get()) if self.enc_reed_entry.get() else global_reedEC
            grid = int(self.enc_grid_entry.get()) if self.enc_grid_entry.get() else global_gridSize
            return reed, grid
        except ValueError:
            print("Invalid numeric settings, using defaults.")
            return global_reedEC, global_gridSize

    def toggle_buttons(self, state="disabled"):
        self.enc_btn.configure(state=state)
        self.dec_btn.configure(state=state)
        self.yt_btn.configure(state=state)

    def start_encoding(self):
        src = self.enc_src_entry.get()
        dest = self.enc_out_entry.get()
        if not src or not dest:
            messagebox.showwarning("Missing Input", "Please select source and output files.")
            return
        
        reed, grid = self.get_params()
        self.toggle_buttons("disabled")
        
        def run():
            try:
                print(f"Starting Encoding: {src} -> {dest}")
                create_video(src, dest, reed, grid)
                print("Encoding Finished Successfully!")
                messagebox.showinfo("Success", "Encoding completed!")
            except Exception as e:
                print(f"Encoding Failed: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Encoding failed: {e}")
            finally:
                self.toggle_buttons("normal")

        threading.Thread(target=run, daemon=True).start()

    def start_decoding(self):
        src = self.dec_src_entry.get()
        dest_folder = self.dec_dest_entry.get()
        if not src or not dest_folder:
            messagebox.showwarning("Missing Input", "Please select source video and output folder.")
            return

        reed, grid = self.get_params()
        self.toggle_buttons("disabled")

        def run():
            try:
                print(f"Starting Decoding: {src} -> {dest_folder}")
                # decode_video expects a cv2 Capture object
                cap = cv2.VideoCapture(src)
                decode_video(cap, dest_folder, reed, grid)
                print("Decoding Finished!")
                messagebox.showinfo("Success", "Decoding completed!")
            except Exception as e:
                print(f"Decoding Failed: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Decoding failed: {e}")
            finally:
                self.toggle_buttons("normal")
        
        threading.Thread(target=run, daemon=True).start()

    def start_youtube(self):
        url = self.yt_url_entry.get()
        dest_folder = self.yt_dest_entry.get()
        if not url or not dest_folder:
            messagebox.showwarning("Missing Input", "Please enter URL and output folder.")
            return

        reed, grid = self.get_params()
        self.toggle_buttons("disabled")

        def run():
            try:
                print(f"Starting YouTube Download & Decode: {url}")
                youtube_decode(url, dest_folder, reed, grid)
                print("Process Finished!")
                messagebox.showinfo("Success", "Process completed!")
            except Exception as e:
                print(f"Task Failed: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Task failed: {e}")
            finally:
                self.toggle_buttons("normal")

        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    app = File2VideoApp()
    app.mainloop()
