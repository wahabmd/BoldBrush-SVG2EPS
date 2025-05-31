import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading
import queue
import shutil
from PIL import Image, ImageTk
import tempfile

class SVGConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BoldBrush SVG2EPS")
        self.root.geometry("800x600")

        # Load and display logo
        try:
            logo_path = os.path.join("assets", "bold-brush--var1 1.png")
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                img.thumbnail((50, 50), Image.Resampling.LANCZOS) # Resize while maintaining aspect ratio
                self.logo_img = ImageTk.PhotoImage(img)
                
                header_frame = tk.Frame(self.root)
                header_frame.pack(fill=tk.X, padx=10, pady=10)

                logo_label = tk.Label(header_frame, image=self.logo_img)
                logo_label.pack(side=tk.LEFT, padx=10)

                title_label = tk.Label(header_frame, text="BoldBrush SVG2EPS", font=("Arial", 16, "bold"))
                title_label.pack(side=tk.LEFT)
            else:
                self.progress_queue.put("Warning: Logo file not found at assets/bold-brush--var1 1.png")
                header_frame = tk.Frame(self.root)
                header_frame.pack(fill=tk.X, padx=10, pady=10)
                title_label = tk.Label(header_frame, text="BoldBrush SVG2EPS", font=("Arial", 16, "bold"))
                title_label.pack(side=tk.LEFT)

        except Exception as e:
            self.progress_queue.put(f"Error loading logo: {str(e)}")
            header_frame = tk.Frame(self.root)
            header_frame.pack(fill=tk.X, padx=10, pady=10)
            title_label = tk.Label(header_frame, text="BoldBrush SVG2EPS", font=("Arial", 16, "bold"))
            title_label.pack(side=tk.LEFT)

        self.setup_ui()
        self.progress_queue = queue.Queue()
        self.selected_files = []
        self.inkscape_path = r"C:\Program Files\Inkscape\bin\inkscape.exe"
        self.check_inkscape()
        
    def check_inkscape(self):
        # Check if Inkscape exists at the specified path
        if not os.path.exists(self.inkscape_path):
            messagebox.showerror(
                "Inkscape Not Found",
                f"Inkscape not found at: {self.inkscape_path}\n\n"
                "Please make sure Inkscape is installed at the correct location."
            )
            self.root.destroy()
            return False
        self.progress_queue.put(f"Inkscape found at: {self.inkscape_path}")
        return True
        
    def setup_ui(self):
        # File selection
        file_frame = tk.Frame(self.root, pady=10)
        file_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(file_frame, text="Select SVG Files:").pack(side=tk.LEFT)
        self.files_listbox = tk.Listbox(file_frame, width=70, height=10, selectmode=tk.MULTIPLE)
        self.files_listbox.pack(side=tk.LEFT, padx=5)
        
        # Buttons frame
        button_frame = tk.Frame(file_frame)
        button_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Add Files", command=self.select_files).pack(pady=5)
        tk.Button(button_frame, text="Remove Selected", command=self.remove_selected).pack(pady=5)
        tk.Button(button_frame, text="Clear All", command=self.clear_files).pack(pady=5)
        
        # Output directory selection
        output_frame = tk.Frame(self.root, pady=10)
        output_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(output_frame, text="Output Directory:").pack(side=tk.LEFT)
        self.output_path = tk.StringVar()
        tk.Entry(output_frame, textvariable=self.output_path, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(output_frame, text="Browse", command=self.select_output_dir).pack(side=tk.LEFT)
        
        # Progress display
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(progress_frame, text="Progress:").pack(anchor=tk.W)
        self.progress_text = tk.Text(progress_frame, height=10, width=70)
        self.progress_text.pack(fill=tk.BOTH, expand=True)
        
        # Convert button
        tk.Button(self.root, text="Convert Files", command=self.start_conversion).pack(pady=10)

        # Footer label
        footer_label = tk.Label(self.root, text="Tool By Wahab Muhammad", bd=1, relief=tk.SUNKEN, anchor=tk.E)
        footer_label.pack(side=tk.BOTTOM, fill=tk.X)
        
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select SVG Files",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
        )
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
            self.progress_queue.put(f"Added {len(files)} files to the list")
            
    def remove_selected(self):
        selected_indices = self.files_listbox.curselection()
        for index in reversed(selected_indices):
            self.files_listbox.delete(index)
            self.selected_files.pop(index)
        self.progress_queue.put("Removed selected files from the list")
            
    def clear_files(self):
        self.files_listbox.delete(0, tk.END)
        self.selected_files.clear()
        self.progress_queue.put("Cleared all files from the list")
            
    def select_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)
            self.progress_queue.put(f"Selected output directory: {directory}")
            
    def convert_svg_to_eps(self, svg_file, output_dir):
        try:
            # Convert SVG to EPS using Inkscape
            eps_file = os.path.join(output_dir, Path(svg_file).stem + '.eps')
            self.progress_queue.put(f"Converting {os.path.basename(svg_file)} to EPS...")
            
            # Run Inkscape with the specific path
            subprocess.run([self.inkscape_path, '--export-filename=' + eps_file, svg_file], 
                         check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            self.progress_queue.put(f"Error converting {os.path.basename(svg_file)} to EPS: {str(e)}")
            return False
        except FileNotFoundError as e:
            self.progress_queue.put(f"Error: {str(e)}")
            messagebox.showerror(
                "Inkscape Not Found",
                f"Inkscape not found at: {self.inkscape_path}\n\n"
                "Please make sure Inkscape is installed at the correct location."
            )
            return False

    def convert_svg_to_jpeg(self, svg_file, output_dir):
        try:
            # Create a temporary directory for intermediate files
            with tempfile.TemporaryDirectory() as temp_dir:
                # First convert to PNG using Inkscape with lower DPI for faster processing
                temp_png = os.path.join(temp_dir, Path(svg_file).stem + '.png')
                self.progress_queue.put(f"Converting {os.path.basename(svg_file)} to JPEG...")
                
                # Run Inkscape to convert to PNG with optimized settings
                result = subprocess.run([
                    self.inkscape_path,
                    '--export-area-page',
                    '--export-dpi=150',  # Reduced DPI for faster processing
                    '--export-background=white',
                    '--export-background-opacity=1',
                    '--export-filename=' + temp_png,
                    svg_file
                ], check=True, capture_output=True, text=True)
                
                if result.stderr:
                    self.progress_queue.put(f"Inkscape PNG conversion warnings: {result.stderr}")
                
                # Now convert PNG to JPEG using PIL with optimized settings
                if os.path.exists(temp_png):
                    # Open the PNG and convert to RGB (in case it has an alpha channel)
                    with Image.open(temp_png) as img:
                        # Convert to RGB mode directly
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Save as JPEG with optimized settings for Pinterest
                        jpeg_file = os.path.join(output_dir, Path(svg_file).stem + '.jpg')
                        img.save(jpeg_file, 'JPEG', quality=75, optimize=True)
                        
                        file_size = os.path.getsize(jpeg_file)
                        self.progress_queue.put(f"JPEG file created at: {jpeg_file} (size: {file_size} bytes)")
                        return True
                else:
                    self.progress_queue.put(f"Error: PNG file was not created at {temp_png}")
                    return False
                
        except subprocess.CalledProcessError as e:
            self.progress_queue.put(f"Error converting {os.path.basename(svg_file)} to JPEG: {str(e)}")
            if e.stdout:
                self.progress_queue.put(f"Command output: {e.stdout}")
            if e.stderr:
                self.progress_queue.put(f"Command errors: {e.stderr}")
            return False
        except Exception as e:
            self.progress_queue.put(f"Unexpected error during JPEG conversion: {str(e)}")
            return False
            
    def conversion_worker(self):
        output_dir = self.output_path.get()
        
        if not self.selected_files:
            self.progress_queue.put("Please select at least one SVG file")
            return
            
        if not output_dir:
            self.progress_queue.put("Please select an output directory")
            return
            
        try:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            for svg_file in self.selected_files:
                # Convert to EPS
                if self.convert_svg_to_eps(svg_file, output_dir):
                    self.progress_queue.put(f"Successfully converted {os.path.basename(svg_file)} to EPS")
                
                # Convert to JPEG
                if self.convert_svg_to_jpeg(svg_file, output_dir):
                    self.progress_queue.put(f"Successfully converted {os.path.basename(svg_file)} to JPEG")
                    
            self.progress_queue.put("Conversion completed!")
            
        except Exception as e:
            self.progress_queue.put(f"Error during conversion: {str(e)}")
        
    def update_progress(self):
        try:
            while True:
                message = self.progress_queue.get_nowait()
                self.progress_text.insert(tk.END, message + "\n")
                self.progress_text.see(tk.END)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.update_progress)
            
    def start_conversion(self):
        # Clear progress text
        self.progress_text.delete(1.0, tk.END)
        
        # Start conversion in a separate thread
        conversion_thread = threading.Thread(target=self.conversion_worker)
        conversion_thread.daemon = True
        conversion_thread.start()
        
    def run(self):
        if self.check_inkscape():
            self.update_progress()
            self.root.mainloop()

if __name__ == "__main__":
    converter = SVGConverter()
    converter.run()