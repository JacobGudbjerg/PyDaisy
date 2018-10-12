from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("ShowDaisy")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        Label(self.master, text="Daisy file").grid(row=1)
        self.e1 = Entry(self.master, w)
        self.e1.grid(row=1, column=1)

        self.button = Button(self.master, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=1, column=2, sticky=W)

    def load_file(self):
        fname = askopenfilename(filetypes=(("Daisy files", "*.dai;*.dlf;*.dwf"), ("All files", "*.*") ))
        self.e1.insert(1, fname)
        if fname:
            try:
                print("""here it comes: self.settings["template"].set(fname)""")
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return


if __name__ == "__main__":
    MyFrame().mainloop()