import tkinter as tk
from tkinter import ttk

def read_report():
    # Read the report file
    report_file = open("./predictions2.txt", "r")
    report_text = report_file.read()
    report_file.close()
    return report_text

def popup_report(root):
    # Create a popup window that displays ./predictions2.txt
    report_window = tk.Toplevel(root)
    report_window.title("Model Report")
    report_window.geometry("600x400")

    # Read the report file
    report_text = read_report()

    # Display the report in a text box
    report_textbox = tk.Text(report_window, wrap="word")
    report_textbox.insert(tk.END, report_text)
    report_textbox.pack(fill="both", expand=True)

    # Close button
    close_button = ttk.Button(report_window, text="Close", command=report_window.destroy)
    close_button.pack(pady=10)