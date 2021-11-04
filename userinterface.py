import tkinter as tk
window = tk.Tk()
welcome_frame = tk.Frame()
greeting = tk.Label(
    text="Remote Heart Diagnosis System",
    width=100,
    height=50,
    master=welcome_frame)
button = tk.Button(
    text="Get Started",
    width=25,
    height = 10
)
entry = tk.Entry(width = 50)
text = tk.Text()
welcome_frame.pack()
button.pack()
entry.pack()
text.pack()
window.mainloop()
