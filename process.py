from os import path
import random
from tkinter import *
from tkinter.font import Font

import cv2
import pandas
import time

todo_list = []
done_list = []
results_list = []
# Variable indicating whether the analysis process is running
run = True


# Updates the to do bar or the done bar based on the two lists, flag 0 is to do and flag 1 is done
def update_bars(frame, flag):
    if flag == 0:
        for widget in frame.winfo_children():
            widget.destroy()
        index = 0
        for todo in todo_list:
            Label(frame, text=path.basename(todo), wraplength=100).pack()
    if flag == 1:
        for widget in frame.winfo_children():
            widget.destroy()
        index = 0
        for done in done_list:
            Label(frame, text=results_list[index]).grid(row=index, column=0, padx=(20, 0))
            Label(frame, text=path.basename(done), wraplength=100).grid(row=index, column=1)
            index += 1


# Processing screen that pops up after clicking on "Analyze Videos"
def process(filenames):
    # Initialize to do list
    for filename in filenames:
        todo_list.append(filename)
    global run
    run = True

    # Process screen layout setup
    process_screen = Toplevel()
    process_screen.title("Processing Videos...")
    process_screen.iconbitmap("resources/processing.ico")
    process_screen.geometry("500x300")

    # Process window close event handler: clear lists after process end
    def on_process_close():
        todo_list.clear()
        done_list.clear()
        results_list.clear()
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

    # Abort button setup
    def abort_process():
        global run
        if run:
            run = False
            abort_alert = Label(progress_frame, text="Process Aborted!", fg="red")
            abort_alert.pack()

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
        while frame_index != frame_total and run:
            # Get frame
            check, frame = video.read()

            # Update progress display
            progress_percentage = str(frame_index) + "/" + str(frame_total)
            progress_percentage_label.configure(text=progress_percentage)
            process_screen.update()

            frame_index += 1

        # Restore progress display to default state
        if run:
            done_list.append(todo)

            # Determine pass/fail
            passed = bool(random.getrandbits(1))

            # Attach pass/fail tag to done items
            pass_status = "[PASS]"
            if not passed:
                pass_status = "[FAIL]"
            results_list.insert(done_list.index(todo), pass_status)

            update_bars(todo_frame, 0)
            update_bars(done_frame, 1)
            progress_percentage_label.configure(text="0/0")
            process_screen.update()

    if run:
        current_label.configure(text="None")
