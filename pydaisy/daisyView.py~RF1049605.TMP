# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from Daisy import DaisyDlf
from scipy.interpolate import griddata


class heatmap(object):
    """
    A class that helps splitting and daisy input files and joining resultfiles.
    """
    def __init__(self, dlf_file, timestep=1):
        points =[]
        xdata = dlf_file.get_x_coordinates()
        ydata = dlf_file.get_y_coordinates()
        for i in range(0, len(xdata)):
            for j in range(0,len(ydata)):
                points.append([xdata[i],ydata[j]])
        grid_x, grid_y = np.mgrid[min(xdata):max(xdata):101j, min(ydata):max(ydata):101j]
 
        grid_z0 = griddata(points, dlf_file.Data.values[timestep,:], (grid_x, grid_y), method='nearest')

        plt.clf()
        plt.imshow(grid_z0.T, extent=[min(xdata),max(xdata),min(ydata), max(ydata)], origin='lower') 
        plt.show()




def daisy_browse():
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
    from Daisy import DaisyModel

    #dm = DaisyModel(r'C:\Roerrendegaard\DaisyModel.dai')

    root = tk.Tk()
    #root.withdraw()

    dm = DaisyModel(filedialog.askopenfilename())

    root.title = dm.DaisyInputfile
    tree = ttk.Treeview(root)

    tree["columns"]=("Words", 'Count')
    tree.column("Words", width=300 )
    tree.column("Count", width=100)
    tree.heading("Words", text="Words")
    tree.heading("Count", text="Count")


    recursiveadd(tree, "", dm.Input)

    tree.pack()
    root.mainloop()

def recursiveadd(tree, parent_item_id, DaisyEntry):
    for cc in DaisyEntry.Children:
        child_item_id=tree.insert(parent_item_id, 3, text=cc.Keyword, values=(' '.join(cc.Words),len(cc.Words) ))
        recursiveadd(tree, child_item_id, cc)