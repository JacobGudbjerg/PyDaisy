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
#            frame = Frame(root, height=400, width=400)
            d=dai_view(fname)
            d.pack(side='top', anchor="w", fill='y')

if __name__ == "__main__":
    root = tk.Tk()
#    root.state('zoomed')
    root.minsize(500, 500)
    root.title("ShowDaisy")

    topframe = Frame(root)
    Label(topframe, text="Daisy file").pack(side='left')
    e1 = Entry(topframe)
    e1.pack(side='left',fill='y')
    Button(topframe, text="Browse", command=load_file, width=10).pack(side='right')
    topframe.pack(side='top', anchor="w")
    root.mainloop()
