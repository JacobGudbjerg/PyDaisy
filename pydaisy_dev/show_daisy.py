import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from daisyView import *


def load_file():
    fname = askopenfilename(filetypes=(("Daisy files", "*.dai;*.dlf;*.dwf"), ("All files", "*.*") ))
    e1.insert(1, fname)
    if fname:
        name, ext = os.path.splitext(fname)
        if ext.lower()=='.dai':
            d=dai_view(fname, root)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ShowDaisy")
    Label(root, text="Daisy file").grid(row=1)
    e1 = Entry(root)
    e1.grid(row=1, column=1)
    Button(root, text="Browse", command=load_file, width=10).grid(row=1, column=2, sticky=W)
    root.mainloop()
