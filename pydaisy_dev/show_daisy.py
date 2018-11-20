import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from daisyView import *

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("ShowDaisy")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        Label(self.master, text="Daisy file").grid(row=1)
        self.e1 = Entry(self.master)
        self.e1.grid(row=1, column=1)

        self.button = Button(self.master, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=1, column=2, sticky=W)

    def load_file(self):
        fname = askopenfilename(filetypes=(("Daisy files", "*.dai;*.dlf;*.dwf"), ("All files", "*.*") ))
        self.e1.insert(1, fname)
        if fname:
            name, ext = os.path.splitext(fname)
            if ext.lower()=='.dai':
                d=dai_view(fname, self.master)


if __name__ == "__main__":
    import dfgui
    from Daisy import *
    df = DaisyDlf(r'C:\GitHub\RainProof\Flak_SB\MultiDaisy\0\daily_Hussar OD SB.dlf')
    dfgui.show(df.Data)
#    MyFrame().mainloop()