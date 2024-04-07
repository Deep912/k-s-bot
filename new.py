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
        self.button_frame.grid(row=1, column=0, sticky="ew")  # Place at bottom

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

    # Remaining methods remain the same...
def on_canvas_resize(self, event):
    # Update positions of A and B when canvas is resized
    self.a_button.place(relx=self.a_x_cm, rely=self.a_y, anchor="center")
    self.b_button.place(relx=self.b_x, rely=self.b_y, anchor="center")


def main():
    root = tk.Tk()
    root.geometry("1400x600")  # Initial window size
    app = DrawingApp(root)
    root.grid_rowconfigure(1, weight=1)  # Allow button frame to expand horizontally
    root.grid_columnconfigure(0, weight=1)  # Allow button frame to expand vertically
    root.mainloop()

if __name__ == "__main__":
    main()
