from os import path
from tkinter import *
from tkinter.font import Font

import cv2
import pandas
import time

todo_list = []
done_list = []


# Updates the to do bar or the done bar based on the two lists, flag 0 is to do and flag 1 is done
def update_bars(frame, flag):
    if flag == 0:
        for widget in frame.winfo_children():
            widget.destroy()
        for todo in todo_list:
            todo_label = Label(frame, text=path.basename(todo), wraplength=100)
            todo_label.pack()
    if flag == 1:
        for widget in frame.winfo_children():
            widget.destroy()
        for done in done_list:
            done_label = Label(frame, text=path.basename(done), wraplength=100)
            done_label.pack()


def abort_process():
    print("EMPTY")


# Processing screen that pops up after clicking on "Analyze Videos"
def process(filenames):

    # Initialize to do list
    for filename in filenames:
        todo_list.append(filename)

    # Process screen layout setup
    process_screen = Toplevel()
    process_screen.title("Processing Videos...")
    process_screen.iconbitmap("resources/processing.ico")
    process_screen.geometry("500x300")

    # Process window close event handler: clear lists after process end
    def on_process_close():
        todo_list.clear()
        done_list.clear()
        process_screen.destroy()
    process_screen.protocol("WM_DELETE_WINDOW", on_process_close)

    # Left "To Do" bar setup
    todo_frame = LabelFrame(process_screen, text="To Do")
    update_bars(todo_frame, 0)
    todo_frame.pack(side=LEFT, expand=True, fill="both", padx=10, pady=10)

    # Middle progress bar setup
    progress_frame = Frame(process_screen)
    process_label = Label(progress_frame, text="Currently processing:", pady=10)
    process_label.configure(font=Font(size=14))
    process_label.pack()
    current_label = Label(progress_frame, text="None")
    current_label.configure(font=Font(size=12))
    current_label.pack()
    progress_percentage_label = Label(progress_frame, text="0/0")
    progress_percentage_label.pack()
    abort_button = Button(progress_frame, text="Abort", command=abort_process)
    abort_button.pack(pady=15)
    progress_frame.pack(side=LEFT, expand=True, pady=10)

    # Right "Done" bar setup
    done_frame = LabelFrame(process_screen, text="Done")
    update_bars(done_frame, 1)
    done_frame.pack(side=LEFT, expand=True, fill="both", padx=10, pady=10)
    process_screen.update()

    # Process loop
    # Process each video in to do list
    while todo_list:
        todo = todo_list.pop()
        current_label.configure(text=path.basename(todo))

        # Prepare video for processing
        df = pandas.DataFrame(columns=["Start", "End"])
        # noinspection PyUnresolvedReferences
        video = cv2.VideoCapture(todo)
        frame_index = 0
        # noinspection PyUnresolvedReferences
        frame_total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Process each frame in video
        while frame_index != frame_total:
            # Get frame
            check, frame = video.read()

            # Update progress display
            progress_percentage = str(frame_index) + "/" + str(frame_total)
            progress_percentage_label.configure(text=progress_percentage)
            process_screen.update()

            frame_index += 1

        done_list.append(todo)
        update_bars(todo_frame, 0)
        update_bars(done_frame, 1)
        progress_percentage_label.configure(text="0/0")
        process_screen.update()

    current_label.configure(text="None")
