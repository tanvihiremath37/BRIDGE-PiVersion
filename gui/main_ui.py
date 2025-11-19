"""
BRIDGE - Main UI Controller
A beautiful Tkinter-based interface for multi-modal accessibility system
Designed for Raspberry Pi 4 touchscreen (800x480)
"""

import tkinter as tk
from tkinter import Canvas, Label, Frame, Text, Entry, Button, Scrollbar
from PIL import Image, ImageTk
import pygame
import os
import sys
import threading

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class BRIDGEApp:
    """Main application class for BRIDGE accessibility system"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("BRIDGE - Accessibility System")
        self.root.geometry("800x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#FADDEA")
        
        # Initialize pygame for audio (optional - won't crash if audio unavailable)
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Audio initialization warning: {e}")
        
        self.click_sound = None
        self.load_click_sound()
        
        # Asset paths
        self.assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        
        # Load mascot images
        self.mascot_normal = None
        self.mascot_smile = None
        self.mascot_wink = None
        self.load_mascot_images()
        
        # Current page tracker
        self.current_page = None
        
        # Running module tracker (prevents double execution)
        self.module_running = False
        self.stop_speech_to_sign = False  # Flag to stop speech to sign loop
        
        # Show home screen
        self.show_home_screen()
    
    def load_click_sound(self):
        """Load button click sound"""
        try:
            sound_path = os.path.join(os.path.dirname(__file__), "assets", "click.wav")
            if os.path.exists(sound_path):
                self.click_sound = pygame.mixer.Sound(sound_path)
        except Exception as e:
            # Silently fail if audio not available
            pass
    
    def play_click_sound(self):
        """Play button click sound"""
        try:
            if self.click_sound:
                self.click_sound.play()
        except Exception as e:
            # Silently fail if audio not available
            pass
    
    def load_mascot_images(self):
        """Load and resize mascot images"""
        try:
            normal_path = os.path.join(self.assets_dir, "mascot_normal.png")
            smile_path = os.path.join(self.assets_dir, "mascot_smile.png")
            wink_path = os.path.join(self.assets_dir, "mascot_wink.png")
            
            if os.path.exists(normal_path):
                img = Image.open(normal_path)
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                self.mascot_normal = ImageTk.PhotoImage(img)
            
            if os.path.exists(smile_path):
                img = Image.open(smile_path)
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                self.mascot_smile = ImageTk.PhotoImage(img)
            
            if os.path.exists(wink_path):
                img = Image.open(wink_path)
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                self.mascot_wink = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Could not load mascot images: {e}")
    
    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_home_screen(self):
        """Display the main home screen with mascot and buttons"""
        self.clear_screen()
        self.current_page = "home"
        
        # Main container
        main_frame = Frame(self.root, bg="#FADDEA")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Mascot
        left_frame = Frame(main_frame, bg="#FADDEA", width=350)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=20)
        left_frame.pack_propagate(False)
        
        # Mascot name label
        mascot_name = Label(left_frame, text="Meet Rubi!", 
                           font=("Arial", 20, "bold"), bg="#FADDEA", fg="#FF1493")
        mascot_name.pack(pady=(10, 5))
        
        # Mascot description
        mascot_desc = Label(left_frame, text="Your friendly accessibility assistant\nPet me for a surprise!", 
                           font=("Arial", 11), bg="#FADDEA", fg="#666", justify=tk.CENTER)
        mascot_desc.pack(pady=(0, 10))
        
        # Mascot label with animation
        mascot_label = Label(left_frame, bg="#FADDEA", image=self.mascot_normal)
        mascot_label.pack(expand=True)
        
        # Mascot animation bindings
        def on_mascot_enter(event):
            if self.mascot_smile:
                mascot_label.config(image=self.mascot_smile)
        
        def on_mascot_leave(event):
            if self.mascot_normal:
                mascot_label.config(image=self.mascot_normal)
        
        def on_mascot_click(event):
            if self.mascot_wink:
                mascot_label.config(image=self.mascot_wink)
                self.root.after(300, lambda: mascot_label.config(image=self.mascot_normal))
        
        mascot_label.bind("<Enter>", on_mascot_enter)
        mascot_label.bind("<Leave>", on_mascot_leave)
        mascot_label.bind("<Button-1>", on_mascot_click)
        
        # Right side - Buttons
        right_frame = Frame(main_frame, bg="#FADDEA")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = Label(right_frame, text="BRIDGE", font=("Arial", 32, "bold"), 
                           bg="#FADDEA", fg="#FF1493")
        title_label.pack(pady=(0, 10))
        
        subtitle_label = Label(right_frame, text="Accessibility System", 
                              font=("Arial", 14), bg="#FADDEA", fg="#666")
        subtitle_label.pack(pady=(0, 20))
        
        # Button definitions
        buttons = [
            ("Sign → Text", self.open_sign_to_text),
            ("Speech → Sign", self.open_speech_to_sign),
            ("Text → Sign", self.open_text_to_sign),
            ("Text → Braille", self.open_text_to_braille),
            ("Speech → Text", self.open_speech_to_text),
            ("Text → Speech", self.open_text_to_speech),
            ("User Profile", self.open_profile)
        ]
        
        # Create buttons
        for text, command in buttons:
            btn = self.create_rounded_button(right_frame, text, command)
            btn.pack(pady=5)
    
    def create_rounded_button(self, parent, text, command):
        """Create a rounded button using Canvas"""
        # Button dimensions
        width = 320
        height = 45
        
        # Create canvas for button
        canvas = Canvas(parent, width=width, height=height, 
                       bg="#FADDEA", highlightthickness=0)
        
        # Draw rounded rectangle
        def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, fill, outline=""):
            points = [
                x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1
            ]
            return canvas.create_polygon(points, smooth=True, fill=fill, outline=outline)
        
        # Initial button
        rect = draw_rounded_rect(canvas, 5, 5, width-5, height-5, 20, "#FF9ECF")
        text_id = canvas.create_text(width//2, height//2, text=text, 
                                     font=("Arial", 12, "bold"), fill="white")
        
        # Hover effects
        def on_enter(event):
            canvas.itemconfig(rect, fill="#FFB7DA")
        
        def on_leave(event):
            canvas.itemconfig(rect, fill="#FF9ECF")
        
        def on_click(event):
            self.play_click_sound()
            canvas.itemconfig(rect, fill="#FF85B5")
            self.root.after(100, lambda: command())
        
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)
        canvas.tag_bind(rect, "<Enter>", on_enter)
        canvas.tag_bind(rect, "<Leave>", on_leave)
        canvas.tag_bind(rect, "<Button-1>", on_click)
        canvas.tag_bind(text_id, "<Enter>", on_enter)
        canvas.tag_bind(text_id, "<Leave>", on_leave)
        canvas.tag_bind(text_id, "<Button-1>", on_click)
        
        return canvas
    
    def create_tool_page(self, title, content_frame_setup=None):
        """Create a generic tool page with back button and content area"""
        self.clear_screen()
        
        # Main container
        main_frame = Frame(self.root, bg="#FADDEA")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with back button
        header_frame = Frame(main_frame, bg="#FF9ECF", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Back button
        back_btn = self.create_rounded_button(header_frame, "← Back", self.show_home_screen)
        back_btn.pack(side=tk.LEFT, padx=10, pady=7)
        
        # Title
        title_label = Label(header_frame, text=title, font=("Arial", 18, "bold"),
                           bg="#FF9ECF", fg="white")
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Content area
        content_frame = Frame(main_frame, bg="#FADDEA")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # If a setup function is provided, call it with the content frame
        if content_frame_setup:
            content_frame_setup(content_frame)
        
        return content_frame
    
    def open_sign_to_text(self):
        """Open Sign to Text module page - runs in separate OpenCV window"""
        self.current_page = "sign_to_text"
        
        def setup_content(content_frame):
            info_label = Label(content_frame, 
                             text="Sign to Text Converter\n\nPress 'Start Camera' to begin.\nPress 'Q' in the camera window to stop.",
                             font=("Arial", 14), bg="#FADDEA", fg="#333",
                             justify=tk.CENTER)
            info_label.pack(pady=30)
            
            status_label = Label(content_frame, text="Status: Ready", 
                               font=("Arial", 12), bg="#FADDEA", fg="#666")
            status_label.pack(pady=10)
            
            def start_module():
                if self.module_running:
                    status_label.config(text="Already running! Please wait...")
                    return
                
                self.module_running = True
                status_label.config(text="Status: Camera Running (Press Q to stop)")
                
                def run_thread():
                    try:
                        from modules import sign_to_text
                        sign_to_text.run()
                    except Exception as e:
                        status_label.config(text=f"Error: {str(e)[:50]}")
                    finally:
                        self.module_running = False
                        status_label.config(text="Status: Camera Stopped")
                
                threading.Thread(target=run_thread, daemon=True).start()
            
            start_btn = self.create_rounded_button(content_frame, "Start Camera", start_module)
            start_btn.pack(pady=10)
        
        self.create_tool_page("Sign → Text", setup_content)
    
    def open_speech_to_sign(self):
        """Open Speech to Sign module page"""
        self.current_page = "speech_to_sign"
        
        def setup_content(content_frame):
            info_label = Label(content_frame,
                             text="Speech to Sign Language\n\nClick 'Start Listening' and speak.\nClick 'Stop' to exit.",
                             font=("Arial", 14), bg="#FADDEA", fg="#333",
                             justify=tk.CENTER)
            info_label.pack(pady=30)
            
            status_label = Label(content_frame, text="Status: Ready", 
                               font=("Arial", 12), bg="#FADDEA", fg="#666")
            status_label.pack(pady=10)
            
            button_frame = Frame(content_frame, bg="#FADDEA")
            button_frame.pack(pady=10)
            
            def start_module():
                if self.module_running:
                    status_label.config(text="Already running! Please wait...")
                    return
                
                self.module_running = True
                self.stop_speech_to_sign = False
                status_label.config(text="Status: Listening... (Say 'goodbye' or click Stop)")
                
                def run_thread():
                    try:
                        # Import the function components directly
                        import numpy as np
                        import matplotlib.pyplot as plt
                        import cv2
                        from PIL import Image, ImageTk
                        from itertools import count
                        import tkinter as tk
                        import string
                        import json
                        import sounddevice as sd
                        from vosk import Model, KaldiRecognizer
                        
                        # Load Vosk model
                        vosk_model_path = os.path.join(
                            os.path.dirname(os.path.dirname(__file__)),
                            "models", "vosk-model"
                        )
                        vosk_model = Model(vosk_model_path)
                        recognizer = KaldiRecognizer(vosk_model, 16000)
                        
                        # Record audio function
                        def record_audio(seconds=4, samplerate=16000):
                            print("Listening...")
                            audio = sd.rec(int(seconds * samplerate), samplerate=samplerate,
                                         channels=1, dtype='int16')
                            sd.wait()
                            return audio.tobytes()
                        
                        # GIF list
                        isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 
                                  'hello', 'thank you', 'please', 'sorry', 'good morning', 'good night']
                        
                        arr = list(string.ascii_lowercase)
                        
                        # Main loop with stop flag
                        while not self.stop_speech_to_sign:
                            try:
                                data = record_audio()
                                
                                if self.stop_speech_to_sign:
                                    break
                                
                                if recognizer.AcceptWaveform(data):
                                    result = json.loads(recognizer.Result())
                                    a = result.get("text", "")
                                else:
                                    result = json.loads(recognizer.PartialResult())
                                    a = result.get("partial", "")
                                
                                a = a.lower()
                                print("You Said:", a)
                                
                                for c in string.punctuation:
                                    a = a.replace(c, "")
                                
                                if a in ["goodbye", "good bye", "bye"]:
                                    print("Exiting...")
                                    status_label.config(text="Status: Stopped (goodbye)")
                                    break
                                
                                # Show GIF or letters
                                if a in isl_gif:
                                    class ImageLabel(tk.Label):
                                        def load(self, im):
                                            if isinstance(im, str):
                                                im = Image.open(im)
                                            self.frames = []
                                            try:
                                                for i in count(1):
                                                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                                                    im.seek(i)
                                            except EOFError:
                                                pass
                                            self.delay = im.info.get('duration', 100)
                                            if len(self.frames) == 1:
                                                self.config(image=self.frames[0])
                                            else:
                                                self.next_frame()
                                        
                                        def next_frame(self):
                                            if self.frames:
                                                self.loc = (getattr(self, 'loc', 0) + 1) % len(self.frames)
                                                self.config(image=self.frames[self.loc])
                                                self.after(self.delay, self.next_frame)
                                    
                                    root = tk.Toplevel()
                                    root.title(f"Sign: {a}")
                                    lbl = ImageLabel(root)
                                    lbl.pack()
                                    
                                    gif_path = os.path.join(
                                        os.path.dirname(os.path.dirname(__file__)),
                                        "ISL_Gifs", f"{a}.gif"
                                    )
                                    
                                    if os.path.exists(gif_path):
                                        lbl.load(gif_path)
                                else:
                                    for ch in a:
                                        if ch in arr:
                                            img_path = os.path.join(
                                                os.path.dirname(os.path.dirname(__file__)),
                                                "letters", f"{ch}.jpg"
                                            )
                                            if os.path.exists(img_path):
                                                img = Image.open(img_path)
                                                img_np = np.asarray(img)
                                                plt.imshow(img_np)
                                                plt.draw()
                                                plt.pause(0.8)
                            
                            except Exception as e:
                                print("Error:", e)
                                if self.stop_speech_to_sign:
                                    break
                            
                            plt.close()
                        
                    except Exception as e:
                        status_label.config(text=f"Error: {str(e)[:50]}")
                        print(f"Full error: {e}")
                    finally:
                        self.module_running = False
                        self.stop_speech_to_sign = False
                        status_label.config(text="Status: Stopped")
                
                threading.Thread(target=run_thread, daemon=True).start()
            
            def stop_module():
                if self.module_running:
                    self.stop_speech_to_sign = True
                    status_label.config(text="Status: Stopping...")
                else:
                    status_label.config(text="Nothing is running")
            
            start_btn = self.create_rounded_button(button_frame, "Start Listening", start_module)
            start_btn.pack(side=tk.LEFT, padx=5)
            
            stop_btn = self.create_rounded_button(button_frame, "Stop", stop_module)
            stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.create_tool_page("Speech → Sign", setup_content)
    
    def open_text_to_sign(self):
        """Open Text to Sign module page with text input"""
        self.current_page = "text_to_sign"
        
        def setup_content(content_frame):
            info_label = Label(content_frame,
                             text="Text to Sign Language\n\nType text below and click 'Show Sign'",
                             font=("Arial", 14), bg="#FADDEA", fg="#333",
                             justify=tk.CENTER)
            info_label.pack(pady=20)
            
            # Text input
            input_frame = Frame(content_frame, bg="#FADDEA")
            input_frame.pack(pady=10)
            
            text_entry = Entry(input_frame, font=("Arial", 14), width=40)
            text_entry.pack(pady=5)
            
            status_label = Label(content_frame, text="", 
                               font=("Arial", 11), bg="#FADDEA", fg="#666")
            status_label.pack(pady=5)
            
            def show_sign():
                if self.module_running:
                    status_label.config(text="Already showing signs! Please wait...")
                    return
                
                text = text_entry.get().strip()
                if not text:
                    status_label.config(text="Please enter some text!")
                    return
                
                self.module_running = True
                status_label.config(text=f"Showing signs for: {text}")
                
                # Run sign display in thread
                def run_thread():
                    try:
                        import string
                        from PIL import Image, ImageTk
                        import numpy as np
                        import matplotlib
                        matplotlib.use('TkAgg')  # Use TkAgg backend
                        import matplotlib.pyplot as plt
                        from itertools import count
                        
                        text_lower = text.lower()
                        
                        # Check if it's a full phrase GIF
                        isl_gif_list = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 
                                       'are you sick', 'be careful', 'hello', 'thank you', 'please', 
                                       'sorry', 'good morning', 'good night', 'good afternoon', 
                                       'good evening', 'yes', 'no']
                        
                        if text_lower in isl_gif_list:
                            # Show GIF in separate window
                            gif_path = os.path.join(
                                os.path.dirname(os.path.dirname(__file__)),
                                "ISL_Gifs",
                                f"{text_lower}.gif"
                            )
                            
                            if os.path.exists(gif_path):
                                class ImageLabel(tk.Label):
                                    def load(self, im):
                                        if isinstance(im, str):
                                            im = Image.open(im)
                                        self.frames = []
                                        try:
                                            for i in count(1):
                                                self.frames.append(ImageTk.PhotoImage(im.copy()))
                                                im.seek(i)
                                        except EOFError:
                                            pass
                                        self.delay = im.info.get('duration', 100)
                                        if len(self.frames) == 1:
                                            self.config(image=self.frames[0])
                                        else:
                                            self.next_frame()
                                    
                                    def next_frame(self):
                                        if self.frames:
                                            self.loc = (getattr(self, 'loc', 0) + 1) % len(self.frames)
                                            self.config(image=self.frames[self.loc])
                                            self.after(self.delay, self.next_frame)
                                
                                win = tk.Toplevel()
                                win.title(f"Sign: {text}")
                                lbl = ImageLabel(win)
                                lbl.pack()
                                lbl.load(gif_path)
                                status_label.config(text="Showing GIF...")
                            else:
                                status_label.config(text=f"GIF not found: {text_lower}.gif")
                        else:
                            # Show letter by letter using matplotlib
                            for ch in text_lower:
                                if ch == ' ':
                                    continue  # Skip spaces
                                if ch in string.ascii_lowercase:
                                    img_path = os.path.join(
                                        os.path.dirname(os.path.dirname(__file__)),
                                        "letters",
                                        f"{ch}.jpg"
                                    )
                                    
                                    if os.path.exists(img_path):
                                        img = Image.open(img_path)
                                        img_np = np.asarray(img)
                                        
                                        plt.figure(figsize=(6, 6))
                                        plt.imshow(img_np)
                                        plt.axis('off')
                                        plt.title(f"Letter: {ch.upper()}", fontsize=16)
                                        plt.tight_layout()
                                        plt.show(block=False)
                                        plt.pause(1.5)
                                        plt.close()
                                    else:
                                        print(f"Letter image not found: {ch}.jpg")
                        
                        status_label.config(text="Done!")
                    except Exception as e:
                        status_label.config(text=f"Error: {str(e)[:50]}")
                        print(f"Full error: {e}")
                    finally:
                        self.module_running = False
                
                threading.Thread(target=run_thread, daemon=True).start()
            
            show_btn = self.create_rounded_button(content_frame, "Show Sign", show_sign)
            show_btn.pack(pady=10)
        
        self.create_tool_page("Text → Sign", setup_content)
    
    def open_text_to_braille(self):
        """Open Text to Braille module page"""
        self.current_page = "text_to_braille"
        
        def setup_content(content_frame):
            info_label = Label(content_frame,
                             text="Text to Braille\n\nType text to send to Arduino Braille display",
                             font=("Arial", 14), bg="#FADDEA", fg="#333",
                             justify=tk.CENTER)
            info_label.pack(pady=20)
            
            # Text input
            input_frame = Frame(content_frame, bg="#FADDEA")
            input_frame.pack(pady=10)
            
            text_entry = Entry(input_frame, font=("Arial", 14), width=40)
            text_entry.pack(pady=5)
            
            status_label = Label(content_frame, text="", 
                               font=("Arial", 11), bg="#FADDEA", fg="#666")
            status_label.pack(pady=5)
            
            def send_braille():
                if self.module_running:
                    status_label.config(text="Already sending! Please wait...")
                    return
                
                text = text_entry.get().strip()
                if not text:
                    status_label.config(text="Please enter some text!")
                    return
                
                self.module_running = True
                status_label.config(text="Sending to Arduino...")
                
                def run_thread():
                    try:
                        from modules import text_to_braille
                        text_to_braille.send_to_braille(text)
                        status_label.config(text=f"Sent: {text}")
                    except Exception as e:
                        status_label.config(text=f"Error: {str(e)[:50]}")
                    finally:
                        self.module_running = False
                
                threading.Thread(target=run_thread, daemon=True).start()
            
            send_btn = self.create_rounded_button(content_frame, "Send to Braille", send_braille)
            send_btn.pack(pady=10)
        
        self.create_tool_page("Text → Braille", setup_content)
    
    def open_speech_to_text(self):
        """Open Speech to Text module page"""
        self.current_page = "speech_to_text"
        
        def setup_content(content_frame):
            info_label = Label(content_frame,
                             text="Speech to Text\n\nClick 'Start Listening' and speak for 5 seconds",
                             font=("Arial", 14), bg="#FADDEA", fg="#333",
                             justify=tk.CENTER)
            info_label.pack(pady=20)
            
            # Output text area with scrollbar
            output_frame = Frame(content_frame, bg="white", relief=tk.SUNKEN, borderwidth=2)
            output_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
            
            scrollbar = Scrollbar(output_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            output_text = Text(output_frame, font=("Arial", 12), height=8, width=60, 
                             wrap=tk.WORD, yscrollcommand=scrollbar.set)
            output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            scrollbar.config(command=output_text.yview)
            
            status_label = Label(content_frame, text="Status: Ready", 
                               font=("Arial", 11), bg="#FADDEA", fg="#666")
            status_label.pack(pady=5)
            
            def start_listening():
                if self.module_running:
                    status_label.config(text="Already listening! Please wait...")
                    return
                
                self.module_running = True
                status_label.config(text="Status: Listening... (5 seconds)")
                output_text.insert(tk.END, "Listening...\n")
                
                def run_thread():
                    try:
                        import json
                        import sounddevice as sd
                        from vosk import Model, KaldiRecognizer
                        
                        # Load Vosk model
                        vosk_model_path = os.path.join(
                            os.path.dirname(os.path.dirname(__file__)),
                            "models", "vosk-model"
                        )
                        
                        if not os.path.exists(vosk_model_path):
                            raise FileNotFoundError("Vosk model missing in models/vosk-model/")
                        
                        model = Model(vosk_model_path)
                        rec = KaldiRecognizer(model, 16000)
                        fs = 16000
                        duration = 5
                        
                        # Record audio
                        recording = sd.rec(int(duration * fs),
                                         samplerate=fs,
                                         channels=1,
                                         dtype="int16")
                        sd.wait()
                        data = recording.tobytes()
                        
                        # Process with Vosk
                        if rec.AcceptWaveform(data):
                            res = json.loads(rec.Result())
                        else:
                            res = json.loads(rec.FinalResult())
                        
                        transcribed_text = res.get("text", "")
                        
                        if transcribed_text:
                            output_text.insert(tk.END, f"You said: {transcribed_text}\n\n")
                            status_label.config(text="Status: Done!")
                        else:
                            output_text.insert(tk.END, "No speech detected. Please try again.\n\n")
                            status_label.config(text="Status: No speech detected")
                        
                    except Exception as e:
                        status_label.config(text=f"Error: {str(e)[:50]}")
                        output_text.insert(tk.END, f"Error: {e}\n\n")
                        print(f"Full error: {e}")
                    finally:
                        self.module_running = False
                
                threading.Thread(target=run_thread, daemon=True).start()
            
            start_btn = self.create_rounded_button(content_frame, "Start Listening", start_listening)
            start_btn.pack(pady=10)
        
        self.create_tool_page("Speech → Text", setup_content)
    
    def open_text_to_speech(self):
        """Open Text to Speech module page"""
        self.current_page = "text_to_speech"
        
        def setup_content(content_frame):
            info_label = Label(content_frame,
                             text="Text to Speech\n\nType text below and click 'Speak'",
                             font=("Arial", 14), bg="#FADDEA", fg="#333",
                             justify=tk.CENTER)
            info_label.pack(pady=20)
            
            # Text input with larger text area
            input_frame = Frame(content_frame, bg="#FADDEA")
            input_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
            
            text_input = Text(input_frame, font=("Arial", 12), height=6, width=60, wrap=tk.WORD)
            text_input.pack(pady=5)
            
            status_label = Label(content_frame, text="", 
                               font=("Arial", 11), bg="#FADDEA", fg="#666")
            status_label.pack(pady=5)
            
            def speak():
                if self.module_running:
                    status_label.config(text="Already speaking! Please wait...")
                    return
                
                text = text_input.get("1.0", tk.END).strip()
                if not text:
                    status_label.config(text="Please enter some text!")
                    return
                
                self.module_running = True
                status_label.config(text="Speaking...")
                
                def run_thread():
                    try:
                        import pyttsx3
                        
                        # Initialize TTS engine
                        engine = pyttsx3.init()
                        engine.setProperty("rate", 150)
                        engine.setProperty("volume", 1.0)
                        
                        # Speak the text
                        print(f"Speaking: {text}")
                        engine.say(text)
                        engine.runAndWait()
                        
                        status_label.config(text="Done!")
                    except Exception as e:
                        status_label.config(text=f"Error: {str(e)[:50]}")
                        print(f"Full TTS error: {e}")
                    finally:
                        self.module_running = False
                
                threading.Thread(target=run_thread, daemon=True).start()
            
            speak_btn = self.create_rounded_button(content_frame, "Speak", speak)
            speak_btn.pack(pady=10)
        
        self.create_tool_page("Text → Speech", setup_content)
    
    def open_profile(self):
        """Open User Profile Setup page"""
        self.current_page = "profile"
        
        def setup_content(content_frame):
            info_label = Label(content_frame,
                             text="User Profile Setup\n\nConfigure your user preferences",
                             font=("Arial", 14), bg="#FADDEA", fg="#333",
                             justify=tk.CENTER)
            info_label.pack(pady=30)
            
            def open_profile_module():
                try:
                    from gui import profile_gui
                    profile_gui.open_profile()
                except Exception as e:
                    print(f"Error opening profile: {e}")
            
            start_btn = self.create_rounded_button(content_frame, "Open Profile", open_profile_module)
            start_btn.pack(pady=10)
        
        self.create_tool_page("User Profile", setup_content)


def main():
    """Main entry point for BRIDGE application"""
    root = tk.Tk()
    app = BRIDGEApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()