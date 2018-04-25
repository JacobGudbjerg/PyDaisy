import numpy as np
import matplotlib.pyplot as plt
from Daisy import DaisyDlf
from scipy.interpolate import griddata


result = DaisyDlf('C:/Projects/DaisyProjects/Pestpore/2d/soil_water_content.dlf')
ydata = result.getYCoordinates()
xdata = result.getXCoordinates();

points =[]
for i in range(0, len(xdata)):
    for j in range(0,len(ydata)):
        points.append([xdata[i],ydata[j]])
grid_x, grid_y = np.mgrid[min(xdata):max(xdata):101j, min(ydata):max(ydata):101j]
 
k=300
grid_z0 = griddata(points, result.Data.values[k,:], (grid_x, grid_y), method='nearest')

plt.clf()
plt.imshow(grid_z0.T, extent=[min(xdata),max(xdata),min(ydata), max(ydata)], origin='lower') 
plt.show()


# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:02:09 2018

@author: jpq949
"""

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
tree.column("Count", width=300)
tree.heading("Words", text="Words")
tree.heading("Count", text="Count")


for c in dm.Input.Children:
    id3= tree.insert("", 3, text=c.Keyword, values=(' '.join(c.Words), len(c.Words) ))
    for cc in c.Children:
        tree.insert(id3, 3, text=cc.Keyword, values=(' '.join(cc.Words),len(cc.Words) ))

tree.pack()
root.mainloop()
