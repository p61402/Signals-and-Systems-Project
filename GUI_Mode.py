import tkinter as tk
import tkinter.ttk as ttk
from tkinter import IntVar
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

x_coef = {}
y_coef = {}
func_text = "y[n]="


def is_term_full(num_of_term):
    if num_of_term >= 5:
        return True


def remove_plus_mark(value):
    new_value_list = list(value)
    del new_value_list[0]
    new_value = "".join(new_value_list)
    return new_value


def add_x(x_coef_dict):
    global number_of_terms
    if is_term_full(number_of_terms):
        value_error("Too Many Terms")
        return False

    x_delay = x_delay_spinbox.get()
    x_coefficient = x_coefficient_entry.get()

    try:
        if len(x_delay) > 5 or len(x_coefficient) > 5:
            value_error("Too Long Error")
            return False
        if not check_delay(int(x_delay)):
            value_error("Delay Error")
            return False
        if not check_coefficient(float(x_coefficient)):
            value_error("Coefficient Error")
            return False
        if int(x_delay) in x_coef_dict:
            value_error("Term Already Exists Error")
            return False
    except ValueError:
        message_list.insert(tk.END, "Wrong X Input.")
        message_list.yview(tk.END)
        return False

    if x_delay[0] == "+":
        x_delay = remove_plus_mark(x_delay)

    if x_coefficient[0] == "+":
        x_coefficient = remove_plus_mark(x_coefficient)

    number_of_terms += 1

    text = func_label["text"]
    try:
        if float(x_coefficient) > 0:
            if number_of_terms == 1:
                text += (x_coefficient + "x[n-" + x_delay + "]")
            else:
                text += ("+" + x_coefficient + "x[n-" + x_delay + "]")
            x_coef_dict[int(x_delay)] = float(x_coefficient)
        elif float(x_coefficient) < 0:
            text += (x_coefficient + "x[n-" + x_delay + "]")
            x_coef_dict[int(x_delay)] = float(x_coefficient)
        else:
            pass
        func_label["text"] = text
    except ValueError:
        pass

    return True


def add_y(y_coef_dict):
    global number_of_terms
    if is_term_full(number_of_terms):
        value_error("Too Many Terms")
        return False

    y_delay = y_delay_spinbox.get()
    y_coefficient = y_coefficient_entry.get()

    try:
        if len(y_delay) > 5 or len(y_coefficient) > 5:
            value_error("Too Long Error")
            return False
        if not check_delay(int(y_delay)) or int(y_delay) == 0:
            value_error("Delay Error")
            return False
        if not check_coefficient(float(y_coefficient)):
            value_error("Coefficient Error")
            return False
        if int(y_delay) in y_coef_dict:
            value_error("Term Already Exists Error")
            return False
    except ValueError:
        message_list.insert(tk.END, "Wrong Y Input.")
        message_list.yview(tk.END)
        return False

    if y_delay[0] == "+":
        y_delay = remove_plus_mark(y_delay)

    if y_coefficient[0] == "+":
        y_coefficient = remove_plus_mark(y_coefficient)

    number_of_terms += 1

    text = func_label["text"]
    try:
        if float(y_coefficient) > 0:
            if number_of_terms == 1:
                text += (y_coefficient + "y[n-" + y_delay + "]")
            else:
                text += ("+" + y_coefficient + "y[n-" + y_delay + "]")
            y_coef_dict[int(y_delay)] = float(y_coefficient)
        elif float(y_coefficient) < 0:
            text += (y_coefficient + "y[n-" + y_delay + "]")
            y_coef_dict[int(y_delay)] = float(y_coefficient)
        else:
            pass
        func_label["text"] = text
    except ValueError:
        pass

    return True


def press_reset(x_coef_dict, y_coef_dict):
    global number_of_terms
    global x_coefficient_entry
    global y_coefficient_entry

    x_coefficient_entry.delete(0, tk.END)
    y_coefficient_entry.delete(0, tk.END)

    number_of_terms = 0

    func_label.config(text="y[n]=")

    x_coef_dict.clear()
    y_coef_dict.clear()

    a.clear()

    show_canvas = FigureCanvasTkAgg(f, master=root)
    show_canvas.show()
    show_canvas.get_tk_widget().grid(row=0, column=6, rowspan=50)

    message_list.insert(tk.END, "Reset")
    message_list.yview(tk.END)


def press_plot(number_of_print_points, x_coef_dict, y_coef_dict):
    # Initialize unit-sample and unit-step function
    unit_sample_x = [1]
    for i in range(100):
        unit_sample_x.append(0)

    unit_step_x = []
    for i in range(50):
        unit_step_x.append(1)
    for i in range(50):
        unit_step_x.append(0)

    y = []
    for i in range(100):
        y.append(0)

    if mode.get() == 1:
        x = unit_sample_x
    else:
        x = unit_step_x

    for count in range(number_of_print_points):
        for a1 in x_coef_dict.keys():
            y[count] += x_coef_dict[a1] * x[count - a1]

        for a2 in y_coef_dict.keys():
            y[count] += y_coef_dict[a2] * y[count - a2]

        print("Output Values:")
        print("y[{0}]={1}".format(count, y[count]))
    print()

    # plotting
    a.clear()
    a.stem(range(number_of_print_points), y[:number_of_print_points])
    show_canvas = FigureCanvasTkAgg(f, master=root)
    show_canvas.show()
    show_canvas.get_tk_widget().grid(row=0, column=6, rowspan=50)
    message_list.insert(tk.END, "Plot")
    message_list.yview(tk.END)


def check_delay(delay_value):
    if delay_value < 0 or delay_value > 10:
        return False
    elif type(delay_value) is float:
        return False
    else:
        return True


def check_coefficient(coefficient_value):
    if coefficient_value < -100 or coefficient_value > 100:
        return False
    else:
        return True


def value_error(error_type):
    if error_type == "Delay Error":
        message_list.insert(tk.END, "Delay Error: X[0, 10], Y[1, 10], type: integer.")
    elif error_type == "Coefficient Error":
        message_list.insert(tk.END, "Coefficient Error: [-100, 100], type: float.")
    elif error_type == "Too Long Error":
        message_list.insert(tk.END, "Too Long Error: Must be less than or equal to 5 characters.")
    elif error_type == "Too Many Terms":
        message_list.insert(tk.END, "Too Many Terms: Only five terms you can insert.")
    elif error_type == "Term Already Exists Error":
        message_list.insert(tk.END, "Term Already Exists!")
    else:
        print("Unknown Error Type.")
    message_list.yview(tk.END)


# main
root = tk.Tk()
root.title("Simulation")

number_of_terms = 0
# function-area
func_frame = ttk.LabelFrame(root, text="Function")
func_frame.grid(row=0, column=0, columnspan=6, ipadx=20, ipady=5)
func_label = ttk.Label(func_frame, text=func_text)
func_label.grid()

# x-area
x_frame = ttk.LabelFrame(root, text="Add X")
x_frame.grid(row=3, column=0, columnspan=3, ipadx=20)

x_delay_label = ttk.Label(x_frame, text="X-Delay", width=15, anchor="center").grid(row=0, column=0)
x_coefficient_label = ttk.Label(x_frame, text="X-Coefficient", width=15, anchor="center").grid(row=1, column=0)

x_delay_spinbox = tk.Spinbox(x_frame, from_=0, to=10, width=3)
x_delay_spinbox.grid(row=0, column=1)
x_coefficient_entry = ttk.Entry(x_frame, width=4)
x_coefficient_entry.grid(row=1, column=1)

x_submit_button =\
    ttk.Button(x_frame, text="Add", width=6, command=lambda: add_x(x_coef)).grid(row=2, column=1)

# y-area
y_frame = ttk.LabelFrame(root, text="Add Y")
y_frame.grid(row=3, column=3, columnspan=3, ipadx=20)

y_delay_label = ttk.Label(y_frame, text="Y-Delay", width=15, anchor="center").grid(row=0, column=0)
y_coefficient_label = ttk.Label(y_frame, text="Y-Coefficient", width=15, anchor="center").grid(row=1, column=0)

y_delay_spinbox = tk.Spinbox(y_frame, from_=1, to=10, width=3)
y_delay_spinbox.grid(row=0, column=1)
y_coefficient_entry = ttk.Entry(y_frame, width=4)
y_coefficient_entry.grid(row=1, column=1)

y_submit_button = \
    ttk.Button(y_frame, text="Add", width=6, command=lambda: add_y(y_coef)).grid(row=2, column=1)
# input-area
input_frame = ttk.LabelFrame(root, text="Input")
input_frame.grid(row=4, column=0, columnspan=3, ipady=8)

mode = IntVar()
mode.set(1)
input_radioButton01 = ttk.Radiobutton(input_frame, text="Unit Sample Function", variable=mode, value=1, width=22)
input_radioButton01.pack(anchor=tk.E)
input_radioButton02 = ttk.Radiobutton(input_frame, text="Unit Step Function", variable=mode, value=2, width=22)
input_radioButton02.pack(anchor=tk.E)

# button-area
button_frame = ttk.LabelFrame(root, text="Button")
button_frame.grid(row=4, column=3)

number_of_nodes = 20
reset_button =\
    ttk.Button(button_frame, text="Reset", width=12, command=lambda: press_reset(x_coef, y_coef))
reset_button.grid(row=0, column=0)
plot_button =\
    ttk.Button(button_frame, text="Plot", width=12, command=lambda: press_plot(number_of_nodes, x_coef, y_coef))
plot_button.grid(row=0, column=1)

# message-area
message_frame = ttk.LabelFrame(root, text="Messages")
message_frame.grid(row=5, columnspan=6)

message_scrollbar = ttk.Scrollbar(message_frame)
message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

message_list = tk.Listbox(message_frame, width=1, height=10, yscrollcommand=message_scrollbar.set)
message_scrollbar.config(command=message_list.yview)
message_list.pack(side=tk.LEFT, fill=tk.BOTH, ipadx=200)

# plot
f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().grid(row=0, column=6, rowspan=50)

root.mainloop()
