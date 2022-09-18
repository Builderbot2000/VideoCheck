from os import path
from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import askyesno

# Quirky import for autocomplete to work
import numpy
from cv2 import cv2
import pandas
import time
import random

todo_list = []
done_list = []
results_list = []

# Variable indicating whether the analysis process is running
running = True


# Updates the to do bar or the done bar based on the two lists, flag 0 is to do and flag 1 is done
def update_bars(frame, flag):
    if flag == 0:
        for widget in frame.winfo_children():
            widget.destroy()
        index = 0
        for todo in todo_list:
            Label(frame, text=path.basename(todo), wraplength=100).grid(row=index, column=0, padx=20)
    if flag == 1:
        for widget in frame.winfo_children():
            widget.destroy()
        index = 0
        for done in done_list:
            Label(frame, text=results_list[index]).grid(row=index, column=0, padx=(20, 0))
            Label(frame, text=path.basename(done), wraplength=100).grid(row=index, column=1, padx=(0, 20))
            index += 1


# Processing screen that pops up after clicking on "Analyze Videos"
def process(filenames):
    # Extract settings variable
    threshold = 30

    # Initialize to do list
    for filename in filenames:
        todo_list.append(filename)
    global running
    running = True

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
        answer = askyesno(title="Confirmation", message="Are you sure you want to abort the analysis?")
        if answer:
            global running
            if running:
                running = False
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

        stutter = 0
        no_diff = 0

        # Process each frame in video
        prev_frame = None
        while frame_index != frame_total-2 and running:
            # Get frame and convert to greyscale
            check, frame = video.read()
            grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Skip initial frame and set it as reference previous frame
            if prev_frame is None:
                prev_frame = grey_frame
                continue

            # Determine difference between frame and reference previous frame
            diff = 0
            height, width = grey_frame.shape
            for x in range(0, width):
                for y in range(0, height):
                    # Check if pixel is equal between two frames
                    # print("Current Pixel: " + str(grey_frame[y, x]))
                    # print("Previous Pixel: " + str(prev_frame[y, x]))
                    if grey_frame[y, x] != prev_frame[y, x]:
                        # cv2.imshow("previous frame", prev_frame)
                        # cv2.imshow("current frame", grey_frame)
                        diff += 1
                    if diff >= 5:
                        break
                    # print("x=" + str(x) + "  y=" + str(y))
            if diff < 5:
                print("SAME")
                no_diff += 1
            if no_diff > 3:
                stutter += 1

            # Update progress display to current progress
            progress_percentage = str(frame_index) + "/" + str(frame_total)
            progress_percentage_label.configure(text=progress_percentage)
            process_screen.update()

            frame_index += 1

        # Restore progress display to default state
        if running:
            done_list.append(todo)

            # Determine pass/fail
            passed = True
            if stutter >= 2:
                passed = False

            # Attach pass/fail tag to done items
            pass_status = "[PASS]"
            if not passed:
                pass_status = "[FAIL]"
            results_list.insert(done_list.index(todo), pass_status)

            update_bars(todo_frame, 0)
            update_bars(done_frame, 1)
            progress_percentage_label.configure(text="0/0")
            process_screen.update()

    if running:
        current_label.configure(text="None")
