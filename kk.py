import tkinter as tk
import time

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Point Recorder")

        # PanedWindow to hold canvas and recorded side
        self.paned_window = tk.PanedWindow(master, orient=tk.HORIZONTAL, sashwidth=5)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Frame for recorded side
        self.coord_frame = tk.Frame(self.paned_window, width=300, bd=2, relief=tk.RAISED)
        self.paned_window.add(self.coord_frame)

        # Label to display instructions
        self.label = tk.Label(self.coord_frame, text="Click on A to start recording.")
        self.label.pack()

        # Frame for text entry and scroll bar
        self.text_frame = tk.Frame(self.coord_frame, bd=2, relief=tk.SOLID)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        # Text entry widget for typing, copying, pasting, and scrolling through code
        self.text_entry = tk.Text(self.text_frame, wrap=tk.WORD, width=40, height=20)
        self.text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add a scrollbar for the text entry widget
        self.text_scrollbar = tk.Scrollbar(self.text_frame, command=self.text_entry.yview)
        self.text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_entry.config(yscrollcommand=self.text_scrollbar.set)

        # List to store recorded coordinates
        self.coordinates = []

        # Boolean to indicate recording status
        self.recording = False

        # Boolean to indicate dragging status
        self.dragging = False

        # Frame for canvas
        self.canvas_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.canvas_frame)

        # Canvas for drawing with black border
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", highlightbackground="black", highlightthickness=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Draw A button
        self.a_size = 50 * 10  # 10 times bigger
        self.a_x_cm = 0.05  # Move 0.05 cm to the left
        self.a_y = 0.5  # Center vertically
        self.a_button = tk.Button(self.canvas, text="A", command=lambda: self.toggle_recording(tag='A'))
        self.a_button.place(relx=self.a_x_cm, rely=self.a_y, anchor="center")

        # Draw B button
        self.b_size = 50 * 10  # 10 times bigger
        self.b_x = 0.95  # Move 0.95 cm to the left (close to the right border)
        self.b_y = 0.5  # Center vertically
        self.b_button = tk.Button(self.canvas, text="B", command=lambda: self.toggle_recording(tag='B'))
        self.b_button.place(relx=self.b_x, rely=self.b_y, anchor="center")

        # Binding mouse events to the canvas
        self.canvas.bind("<B1-Motion>", self.move_point_start)
        self.canvas.bind("<ButtonRelease-1>", self.move_point_end)
        self.canvas.bind("<Motion>", self.draw_dot)

        # Buttons below recorder
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(fill=tk.X)

        self.record_button = tk.Button(self.button_frame, text="Record", command=self.toggle_recording)
        self.record_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.remove_last_button = tk.Button(self.button_frame, text="Remove Last", command=self.remove_last)
        self.remove_last_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.play_button = tk.Button(self.button_frame, text="Play", command=self.play)
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear Samples", command=self.clear_samples)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.train_button = tk.Button(self.button_frame, text="Train Model", command=self.train_model)
        self.train_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.button_frame, text="Save Model", command=self.save_model)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_button = tk.Button(self.button_frame, text="Load Model", command=self.load_model)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.test_button = tk.Button(self.button_frame, text="Test", command=self.test)
        self.test_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Timer for recording mouse movement
        self.timer_running = False
        self.last_recorded_time = 0
        self.start_time = 0

    def start_recording(self, event=None, tag=None):
        self.recording = True
        self.label.config(text="Recording...")
        self.coordinates = []  # Reset coordinates list
        self.start_time = time.time()  # Record start time

        # Start timer for recording mouse movement
        if not self.timer_running:
            self.timer_running = True
            self.record_mouse_movement()

    def stop_recording(self, event=None):
        self.recording = False
        self.label.config(text="Click on A to start recording.")
        self.timer_running = False

    def toggle_recording(self, event=None, tag=None):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording(tag=tag)

    def record_mouse_movement(self):
        if self.recording:
         x = self.canvas.canvasx(self.canvas.winfo_pointerx())
         y = self.canvas.canvasy(self.canvas.winfo_pointery())
         canvas_width = self.canvas.winfo_width()
         canvas_height = self.canvas.winfo_height()
         if 0 <= x <= canvas_width and 0 <= y <= canvas_height:
            if not self.canvas.find_withtag(tk.CURRENT) and not self.canvas.find_withtag("Button", "tag"):  # Check if the mouse is not over any button
                current_time = int((time.time() - self.start_time) * 1000)  # Time since recording started
                self.coordinates.append({"x": x, "y": y, "t": current_time})
                self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill='black', tags="dot")  # Draw smaller square on canvas
                self.update_recorded_text()  # Update recorded text
        self.master.after(500, self.record_mouse_movement)


    def update_recorded_text(self):
        # Clear the text entry widget
        self.text_entry.delete(1.0, tk.END)

        # Add A coordinates
        self.text_entry.insert(tk.END, '"A": {\n')
        self.text_entry.insert(tk.END, f'    "x": {self.coordinates[0]["x"]},\n')
        self.text_entry.insert(tk.END, f'    "y": {self.coordinates[0]["y"]},\n')
        self.text_entry.insert(tk.END, f'    "t": 0\n')
        self.text_entry.insert(tk.END, '},\n')

        # Add B coordinates
        self.text_entry.insert(tk.END, '"B": {\n')
        self.text_entry.insert(tk.END, f'    "x": {self.coordinates[-1]["x"]},\n')
        self.text_entry.insert(tk.END, f'    "y": {self.coordinates[-1]["y"]},\n')
        self.text_entry.insert(tk.END, f'    "t": {self.coordinates[-1]["t"]}\n')
        self.text_entry.insert(tk.END, '},\n')

        # Add points coordinates
        self.text_entry.insert(tk.END, '"points": [\n')
        for point in self.coordinates[1:-1]:
            self.text_entry.insert(tk.END, '    {\n')
            self.text_entry.insert(tk.END, f'        "x": {point["x"]},\n')
            self.text_entry.insert(tk.END, f'        "y": {point["y"]},\n')
            self.text_entry.insert(tk.END, f'        "t": {point["t"]}\n')
            self.text_entry.insert(tk.END, '    },\n')
        self.text_entry.insert(tk.END, '],\n')

    def move_point_start(self, event):
        if self.recording:
            if event.widget.find_withtag(tk.CURRENT):
                self.dragging = True

    def move_point_end(self, event):
        self.dragging = False

    def on_canvas_resize(self, event):
        # Update positions of A and B when canvas is resized
        self.a_button.place(relx=self.a_x_cm, rely=self.a_y, anchor="center")
        self.b_button.place(relx=self.b_x, rely=self.b_y, anchor="center")

    def remove_last(self):
        # Remove all recorded points from the canvas
        self.canvas.delete("dot")

        # Clear the recorded coordinates list
        self.coordinates = []

        # Clear the recorded text
        self.text_entry.delete(1.0, tk.END)

    def draw_dot(self, event):
        if self.recording:
            x, y = event.x, event.y
            if not self.canvas.find_withtag(tk.CURRENT):  # Check if the mouse is not over any button
                current_time = int((time.time() - self.start_time) * 1000)  # Time since recording started
                self.coordinates.append({"x": x, "y": y, "t": current_time})
                self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill='black', tags="dot")  # Draw smaller square on canvas
                self.update_recorded_text()  # Update recorded text

    def play(self):
        # Functionality to play recorded points
        pass

    def clear_samples(self):
        # Functionality to clear recorded samples
        pass

    def train_model(self):
        # Functionality to train the model
        pass

    def save_model(self):
        # Functionality to save the model
        pass

    def load_model(self):
        # Functionality to load a model
        pass

    def test(self):
        # Functionality to test the model
        pass

def main():
    root = tk.Tk()
    root.geometry("1200x600")  # Initial window size
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
