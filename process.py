from tkinter import *
from tkinter.font import Font
from os import path


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

    # Process loop
    # Process each video
    print(todo_list)
    for todo in todo_list:
        print(todo)
        print("Do Nothing!")
        current_label.configure(text=path.basename(todo))

        # Process each frame in video
        # EMPTY

        done_list.append(todo_list.pop(0))
        update_bars(todo_frame, 0)
        update_bars(done_frame, 1)

    current_label.configure(text="None")
