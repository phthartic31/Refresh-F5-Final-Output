"""
Simple GUI Calculator
----------------------
Built with tkinter (comes built-in with Python, no extra install needed).

Broken into functions, following the same idea from your worksheet:
- build_gui()      -> sets up the window and buttons
- on_button_click() -> handles what happens when a number/operator is pressed
- calculate_result() -> does the actual math
- clear_display()   -> resets the screen
"""

import tkinter as tk


def build_gui():
    """Creates the calculator window, display, and buttons."""
    window = tk.Tk()
    window.title("Simple Calculator")
    window.geometry("300x450")
    window.resizable(False, False)

    # Display screen at the top
    display_var = tk.StringVar()
    display = tk.Entry(
        window, textvariable=display_var, font=("Arial", 24),
        justify="right", bd=10, relief="ridge"
    )
    display.grid(row=0, column=0, columnspan=4, sticky="nsew")

    # Button layout: (label, row, column)
    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ('C', 5, 0)
    ]

    for (label, row, col) in buttons:
        if label == '=':
            action = lambda: calculate_result(display_var)
        elif label == 'C':
            action = lambda: clear_display(display_var)
        else:
            action = lambda label=label: on_button_click(display_var, label)

        btn = tk.Button(
            window, text=label, font=("Arial", 18),
            command=action
        )
        btn.grid(row=row, column=col, sticky="nsew")

    # Make rows/columns resize evenly
    for i in range(6):
        window.grid_rowconfigure(i, weight=1)
    for i in range(4):
        window.grid_columnconfigure(i, weight=1)

    return window


def on_button_click(display_var, label):
    """Appends the clicked number/operator to the display."""
    current = display_var.get()
    display_var.set(current + label)


def calculate_result(display_var):
    """Evaluates the expression currently shown on the display."""
    try:
        expression = display_var.get()
        result = eval(expression)  # safe here since input is only from our own buttons
        display_var.set(str(result))
    except (SyntaxError, ZeroDivisionError):
        display_var.set("Error")


def clear_display(display_var):
    """Clears the display screen."""
    display_var.set("")


def main():
    window = build_gui()
    window.mainloop()


if __name__ == "__main__":
    main()