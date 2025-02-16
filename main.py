import tkinter as tk
from tkinter import scrolledtext
import pygame
from utils.chat_handler import ChatHandler
import threading

class StressReliefApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stress Relief Assistant")
        self.chat_handler = ChatHandler()
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
        self._setup_ui()

    def _setup_ui(self):
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Label(
            main_frame,
            text="🧘 Stress Relief Assistant",
            font=("Helvetica", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        header.pack(pady=(0, 10))

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=("Helvetica", 10)
        )
        self.chat_display.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        # Input area
        self.input_field = tk.Entry(
            main_frame,
            width=50,
            font=("Helvetica", 10)
        )
        self.input_field.pack(pady=(0, 10), fill=tk.X)
        self.input_field.bind("<Return>", self._on_submit)

        # Send button
        send_button = tk.Button(
            main_frame,
            text="Send",
            command=self._on_submit,
            bg='#2c3e50',
            fg='white',
            padx=20
        )
        send_button.pack()

    def _on_submit(self, event=None):
        text = self.input_field.get()
        if not text.strip():
            return

        # Clear input field
        self.input_field.delete(0, tk.END)

        # Display user message
        self.chat_display.insert(tk.END, f"\nYou: {text}\n")
        self.chat_display.see(tk.END)

        # Process message in a separate thread
        threading.Thread(target=self._process_message, args=(text,)).start()

    def _process_message(self, text):
        try:
            # Get response from chat handler
            response = self.chat_handler.process_message(text)
            
            # Display AI response
            self.chat_display.insert(tk.END, f"\nAI: {response['text_response']}\n")
            self.chat_display.see(tk.END)
            
            # Play audio response
            pygame.mixer.music.load(response['audio_file'])
            pygame.mixer.music.play()
            
        except Exception as e:
            self.chat_display.insert(tk.END, f"\nError: {str(e)}\n")
            self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StressReliefApp(root)
    root.mainloop()