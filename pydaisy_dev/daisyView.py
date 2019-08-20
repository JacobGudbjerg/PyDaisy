# -*- coding: utf-8 -*-
import sys
sys.path.append(r'../')
import numpy as np
import matplotlib.pyplot as plt
from pydaisy.Daisy import DaisyDlf, DaisyModel
from scipy.interpolate import griddata
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, Frame, Listbox
import os

class heatmap(object):
    """
    A class that draws a heat map from a daisy dlf file if it has x- and y-coordinates 
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
    
    def plot(self, timestep=1):
        grid_z0 = griddata(self.points, self.daisy_dlf.Data.values[timestep,:], (self.grid_x, self.grid_y), method='nearest')
        plt.clf()
        plt.imshow(grid_z0.T, self.extent, origin='lower') 
        plt.show()




class dai_view(object):
    def __init__(self, filename, frame):

        self.tree = ttk.Treeview(frame, selectmode='browse')
        self.tree.pack(side='left')
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree["columns"]=('Word')
        self.tree.column("Word", width=100 )
        self.tree.heading("Word", text="Word")
        self.tree.bind("<<TreeviewSelect>>", self.selectItem, "+")

        self.listbox = Listbox(frame)
        self.listbox.pack(side='right', fill='y',  padx=5)
        vsb.pack(side='right', fill='y')

        dm = DaisyModel(filename)
        self.recursiveadd("", dm.Input)


    def selectItem(self, a):
        curItem = self.tree.focus()
        self.listbox.delete(0, tk.END)
        item = self.tree.item(curItem)
        for item in self.tree.item(curItem)['values']:
            self.listbox.insert(tk.END, item)

    def recursiveadd(self, parent_item_id, DaisyEntry):
        for cc in DaisyEntry.Children:
            child_item_id=self.tree.insert(parent_item_id, 3, text=cc.Keyword, values=cc.Words )
            self.recursiveadd(child_item_id, cc)
