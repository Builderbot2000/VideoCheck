from tkinter import *
from PIL import ImageTk, Image
from tkinter.font import Font


def process(filenames):
    process_screen = Toplevel()
    process_screen.title("Processing Videos...")
    process_screen.iconbitmap("resources/processing.ico")
    process_screen.geometry("500x300")
