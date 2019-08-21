# -*- coding: utf-8 -*-
import sys
sys.path.append(r'../')
import numpy as np
import matplotlib.pyplot as plt
from pydaisy.Daisy import DaisyDlf, DaisyModel
from scipy.interpolate import griddata
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, Frame, Listbox, Label
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





class daisy_entry_view(Frame):
    def __init__(self, daisy_entry):
        super().__init__(padx=5)

        Label(self, text = daisy_entry.Keyword).pack(side='top', anchor="w")
        listbox = Listbox(self)
        listbox.pack(side='top', fill='y')
        for item in daisy_entry.Words:
            listbox.insert(tk.END, item)



class dai_view(Frame):
    def __init__(self, filename):
        super().__init__()

        self.tree = ttk.Treeview(self, selectmode='browse')
        self.tree.pack(side='left', fill='y', padx=5)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree["columns"]=('Word')
        self.tree.column("Word", width=100 )
        self.tree.heading("Word", text="Word")
        self.tree.bind("<<TreeviewSelect>>", self.selectItem, "+")

        self.item_dictionary={}

        dm = DaisyModel(filename)
        self.recursiveadd("", dm.Input)

    def selectItem(self, a):
        curItem = self.tree.focus()
        selected_item = self.item_dictionary[curItem]
        if hasattr(self, 'dev'):
            del self.dev
        self.dev = daisy_entry_view(selected_item)
        self.dev.pack(side='right')


    def recursiveadd(self, parent_item_id, DaisyEntry):
        for cc in DaisyEntry.Children:
            child_item_id=self.tree.insert(parent_item_id, 3, text=cc.Keyword, values=cc.Words )
            self.item_dictionary[child_item_id]=cc
            self.recursiveadd(child_item_id, cc)
