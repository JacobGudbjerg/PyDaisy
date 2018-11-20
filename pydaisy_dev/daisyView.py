# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from pydaisy.Daisy import DaisyDlf, DaisyModel
from scipy.interpolate import griddata
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import os

class heatmap(object):
    """
    A class that draw a heat map from a daisy dlf file if it has x- and y-coordinates 
    """
    def __init__(self, daisy_dlf, grid_nx=101j, grid_ny=101j):
        self.daisy_dlf=daisy_dlf
        self.points =[]
        x_coordinates = daisy_dlf.get_x_coordinates()
        y_coordinates = daisy_dlf.get_y_coordinates()
        for i in range(0, len(x_coordinates)):
            for j in range(0,len(y_coordinates)):
                self.points.append([x_coordinates[i],y_coordinates[j]])
        self.grid_x, self.grid_y = np.mgrid[min(x_coordinates):max(x_coordinates):grid_nx, min(y_coordinates):max(y_coordinates):grid_ny]
        self.extent=[min(x_coordinates), max(x_coordinates), min(y_coordinates), max(y_coordinates)]
    
    def plot(timestep=1):
        grid_z0 = griddata(self.points, self.daisy_dlf.Data.values[timestep,:], (self.grid_x, self.grid_y), method='nearest')
        plt.clf()
        plt.imshow(grid_z0.T, self.extent, origin='lower') 
        plt.show()




class dai_view(object):
    def __init__(self, filename, master):
        root = tk.Tk(master)
        self.tree = ttk.Treeview(root)


        dm = DaisyModel(filename)
        root.title = dm.DaisyInputfile

        self.tree["columns"]=('Par1', 'Par2')
        self.tree.column("Par1", width=100 )
        self.tree.column("Par2", width=100)
        self.tree.heading("Par1", text="Par1")
        self.tree.heading("Par2", text="Par2")
        self.recursiveadd("", dm.Input)
        self.tree.pack()
        self.tree.bind('<ButtonRelease-1>', self.selectItem)
        root.mainloop()

        Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
        Button(master, text='Show', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)


    def selectItem(self, a):
        curItem = self.tree.focus()
        print (self.tree.item(curItem))

    def recursiveadd(self, parent_item_id, DaisyEntry):
        for cc in DaisyEntry.Children:
            child_item_id=self.tree.insert(parent_item_id, 3, text=cc.Keyword, values=cc.Words )
            self.recursiveadd(child_item_id, cc)
