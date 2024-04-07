
import tkinter as tk
import time

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Point Recorder")

        # Frame for recorded side
        self.coord_frame = tk.Frame(master, width=300, bd=2, relief=tk.RAISED)
        self.coord_frame.pack(side=tk.LEFT, fill=tk.Y)

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

        # Canvas frame
        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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
        self.a_button.bind("<Enter>", self.on_enter_button)
        self.a_button.bind("<Leave>", self.on_leave_button)

        # Draw B button
        self.b_size = 50 * 10  # 10 times bigger
        self.b_x = 0.95  # Move 0.95 cm to the left (close to the right border)
        self.b_y = 0.5  # Center vertically
        self.b_button = tk.Button(self.canvas, text="B", command=lambda: self.toggle_recording(tag='B'))
        self.b_button.place(relx=self.b_x, rely=self.b_y, anchor="center")
        self.b_button.bind("<Enter>", self.on_enter_button)
        self.b_button.bind("<Leave>", self.on_leave_button)

        # Binding mouse events to the A and B buttons for dragging
        self.a_button.bind("<ButtonPress-1>", self.start_dragging)
        self.a_button.bind("<B1-Motion>", self.drag)
        self.a_button.bind("<ButtonRelease-1>", self.stop_dragging)

        self.b_button.bind("<ButtonPress-1>", self.start_dragging)
        self.b_button.bind("<B1-Motion>", self.drag)
        self.b_button.bind("<ButtonRelease-1>", self.stop_dragging)

        # Binding mouse events to the canvas
        self.canvas.bind("<B1-Motion>", self.move_point_start)
        self.canvas.bind("<ButtonRelease-1>", self.move_point_end)
        self.canvas.bind("<Motion>", self.draw_dot)

        # Frame for buttons below canvas
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Buttons below recorder
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

        # Boolean flag to indicate if mouse is over A or B buttons
        self.mouse_over_button = False

        # Store drawn dots during playback
        self.play_dots = []

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
        self.update_recorded_text()  # Update recorded text
        self.redraw_dots()  # Redraw dots on canvas

    def toggle_recording(self, event=None, tag=None):
        if not self.recording:
            self.start_recording(tag=tag)
        else:
            self.stop_recording()
            self.master.after(5000, self.clear_dots)  # Clear dots after 5 seconds

    def clear_dots(self):
        if not self.recording:
            self.canvas.delete("dot")

    def record_mouse_movement(self):
        if self.recording:
            x = self.canvas.canvasx(self.canvas.winfo_pointerx())
            y = self.canvas.canvasy(self.canvas.winfo_pointery())
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Check if the mouse is within the canvas boundaries and not over A or B buttons
            if 0 <= x <= canvas_width and 0 <= y <= canvas_height and not self.mouse_over_button:
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

    def redraw_dots(self):
        # Redraw dots on the canvas based on recorded coordinates
        self.canvas.delete("dot")  # Clear existing dots
        for point in self.coordinates:
            x = point["x"]
            y = point["y"]
            self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill='black', tags="dot")  # Draw dot

    def draw_dot(self, event):
        if self.recording and not self.mouse_over_button:
            x, y = event.x, event.y
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Check if the mouse is within the canvas boundaries and not over A or B buttons
            if 0 <= x <= canvas_width and 0 <= y <= canvas_height and not self.mouse_over_button:
                current_time = int((time.time() - self.start_time) * 1000)  # Time since recording started
                self.coordinates.append({"x": x, "y": y, "t": current_time})
                self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill='black', tags="dot")  # Draw smaller square on canvas

    def on_enter_button(self, event):
        self.mouse_over_button = True

    def on_leave_button(self, event):
        self.mouse_over_button = False

    def start_dragging(self, event):
        if event.widget == self.a_button or event.widget == self.b_button:
            self.dragging = True
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root

    def drag(self, event):
        if self.dragging:
            # Calculate the movement distance
            delta_x = event.x_root - self.drag_start_x
            delta_y = event.y_root - self.drag_start_y

            # Get the canvas position
            canvas_x = self.canvas.winfo_rootx()
            canvas_y = self.canvas.winfo_rooty()

            # Move the button by the calculated distance relative to the canvas position
            event.widget.place(x=event.widget.winfo_x() + delta_x - canvas_x, y=event.widget.winfo_y() + delta_y - canvas_y)

            # Redraw the A and B buttons at their new positions
            self.redraw_buttons()

            # Update the starting position for the next movement
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root

    def stop_dragging(self, event):
        self.dragging = False

    def redraw_buttons(self):
        # Redraw A button
        a_x = self.a_button.winfo_rootx() - self.canvas.winfo_rootx()
        a_y = self.a_button.winfo_rooty() - self.canvas.winfo_rooty()
        self.a_button.place(x=a_x, y=a_y)

        # Redraw B button
        b_x = self.b_button.winfo_rootx() - self.canvas.winfo_rootx()
        b_y = self.b_button.winfo_rooty() - self.canvas.winfo_rooty()
        self.b_button.place(x=b_x, y=b_y)

    def play(self):
        if self.coordinates:
            self.clear_play_dots()  # Clear previously stored dots

            # Calculate total time elapsed from the first recorded point to the last
            total_time = self.coordinates[-1]["t"]

            # Display dots sequentially with delays to simulate recorded timeline
            for point in self.coordinates:
                x = point["x"]
                y = point["y"]
                t = point["t"]
                delay = (t / total_time) * 1000  # Convert time to milliseconds

                # Schedule the display of each dot with the appropriate delay
                self.master.after(int(delay), lambda x=x, y=y: self.display_play_dot(x, y))

    def display_play_dot(self, x, y):
        # Display a single dot at given coordinates
        dot = self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill='red', tags="play_dot")
        self.play_dots.append(dot)  # Store dot reference for future manipulation

    def clear_play_dots(self):
        # Clear dots created during playback
        for dot in self.play_dots:
            self.canvas.delete(dot)
        self.play_dots = []

    def remove_last(self):
        # Remove all recorded points from the canvas
        self.canvas.delete("dot")

        # Clear the recorded coordinates list
        self.coordinates = []

        # Clear the recorded text
        self.text_entry.delete(1.0, tk.END)

        # Clear dots created during playback
        self.clear_play_dots()

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

def main():
    root = tk.Tk()
    root.geometry("1400x600")  # Initial window size
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

