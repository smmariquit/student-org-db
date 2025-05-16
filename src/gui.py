import tkinter as tk
from tkinter import ttk
import mariadb
from typing import Optional

class StudentOrgApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Organization Database")
        self.root.geometry("800x600")

def main():
    root = tk.Tk()
    app = StudentOrgApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 