import google.generativeai as genai  # Install: pip install google-generativeai
import pyttsx3  # Install: pip install pyttsx3
import tkinter as tk  # Install: pip install tk
from tkinter import scrolledtext
import threading  # For faster response handling
from PIL import Image, ImageTk  # Install: pip install pillow
import os

# Insert Your API Key Here
GENAI_API_KEY = "AIzaSyDm22p3rw0XHDDZP-_8yMGIPcON4-ugHbk"  # Replace with your actual API key
genai.configure(api_key=GENAI_API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_response(query):
    """Generate a response for the given query using Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query, stream=False)  # Stream disabled for faster response
        return response.text if hasattr(response, "text") else "I'm not sure about that."
    except Exception as e:
        return f"Error: {e}"

# Create Main Chatbot Window
root = tk.Tk()
root.title("AI Chatbot")
root.state("zoomed")  # Fullscreen mode

# Load Background Image
bg_path = os.path.join(os.getcwd(), "background.jpg")  # Ensure correct path handling
if os.path.exists(bg_path):
    try:
        bg_image = Image.open(bg_path)
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        background_label = tk.Label(root, image=bg_photo)
        background_label.place(relwidth=1, relheight=1)  # Fit image to the entire window
    except Exception as e:
        print(f"Error loading background image: {e}")
else:
    print("Warning: background.jpg not found!")

# Chat Display Area
conversation_area = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=90, height=25, font=("Arial", 14), bg="#2b2b2b", fg="white"
)
conversation_area.place(relx=0.5, rely=0.4, anchor="center")

# User Input Field
user_input = tk.Entry(root, font=("Arial", 16), width=80, bg="#444", fg="white")
user_input.place(relx=0.5, rely=0.75, anchor="center")

def handle_user_input(event=None):
    """Processes user input and generates a chatbot response asynchronously."""
    query = user_input.get().strip()
    if query:
        conversation_area.insert(tk.END, f"You: {query}\n", "user")
        user_input.delete(0, tk.END)
        threading.Thread(target=process_response, args=(query,), daemon=True).start()

def process_response(query):
    """Runs the chatbot response in a separate thread for speed."""
    response = generate_response(query)
    conversation_area.insert(tk.END, f"Chatbot: {response}\n\n", "bot")
    conversation_area.see(tk.END)
    speak(response)

# Bind Enter key to sending messages
user_input.bind("<Return>", handle_user_input)

# Send Button
send_button = tk.Button(
    root, text="Send", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=handle_user_input
)
send_button.place(relx=0.4, rely=0.85, anchor="center")

# Exit Button
exit_button = tk.Button(
    root, text="Exit", font=("Arial", 14, "bold"), bg="red", fg="white", command=root.quit
)
exit_button.place(relx=0.6, rely=0.85, anchor="center")

# Initial Chatbot Message
conversation_area.insert(tk.END, "Chatbot: Hello! How can I assist you today?\n\n")
threading.Thread(target=speak, args=("Hello! How can I assist you today?",), daemon=True).start()

root.mainloop()
