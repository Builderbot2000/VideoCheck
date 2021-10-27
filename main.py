# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from PIL import ImageTk, Image
from tkinter.font import Font
from tkinter import filedialog

# Press the green button in the gutter to run the script.
from process import process

if __name__ == '__main__':
    # Root frame setup
    root = Tk()
    root.title("VideoCheck")
    root.iconbitmap("resources/video.ico")
    root.geometry("500x300")

    # Button frame events
    def analyze_button_event():
        filenames = \
            filedialog.askopenfilename(title="Select A Video To Process", filetypes=(("MP4 files", "*.mp4"), ("AVI files", "*.avi")))
        process(filenames)

    def settings_button_event():
        settings_screen = Toplevel()
        settings_screen.iconbitmap("resources/settings.ico")
        settings_screen.geometry("500x300")
        settings_screen.title("Settings")
        settings_screen_label = Label(settings_screen, text="Settings", pady=15)
        settings_title_font = Font(size=16)
        settings_screen_label.configure(font=settings_title_font)
        settings_screen_label.pack()

    def exit_button_event():
        root.destroy()

    # Button frame layout setup
    button_frame = Frame(root)

    analyze_button = Button(button_frame, text="Analyze Video", command=analyze_button_event, padx=30, pady=10)
    settings_button = Button(button_frame, text="Settings", command=settings_button_event, padx=30, pady=10)
    exit_button = Button(button_frame, text="Exit", command=exit_button_event, padx=30, pady=10)

    analyze_button.pack(padx=10, pady=(30, 10), fill="x")
    settings_button.pack(padx=10, pady=10, fill="x")
    exit_button.pack(padx=10, pady=(10, 30), fill="x")

    button_frame.pack(side=LEFT, fill="none", expand=True)

    # Title frame events
    def help_event():
        help_screen = Toplevel()
        help_screen.title("Help")
        help_screen.iconbitmap("resources/info.ico")
        help_screen.geometry("500x300")
        help_text = Label(help_screen, text="Help.....").pack()


    def about_event():
        about_screen = Toplevel()
        about_screen.title("About")
        about_screen.iconbitmap("resources/info.ico")
        about_screen.geometry("500x300")
        about_text = Label(about_screen, text="Build 1.0.1", pady=15).pack()

    # Title frame layout setup
    title_frame = Frame(root)
    title_label = Label(title_frame, text="Power Cycle Helper")
    title_font = Font(family="Times New Roman", size=20)
    title_label.configure(font=title_font)
    title_label.pack(pady=10)
    icon = ImageTk.PhotoImage(Image.open("resources/dvr-icon-3.jpg").resize((150, 100), Image.ANTIALIAS))
    icon_label = Label(title_frame, image=icon)
    icon_label.pack(pady=10)
    help_button = Button(title_frame, text="Help", command=help_event)
    help_button.pack(pady=5)
    about_button = Button(title_frame, text="About", command=about_event)
    about_button.pack(pady=5)

    title_frame.pack(side=LEFT, fill="none", expand=True, padx=(0, 10))

    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
