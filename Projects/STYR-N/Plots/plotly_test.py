# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 12:55:04 2018

@author: tqc268
"""

import plotly.plotly as py
import plotly.tools as tls
import matplotlib.pyplot as plt
import numpy as np

mpl_fig = plt.figure()
ax = mpl_fig.add_subplot(111)

N = len(df2)
#menMeans = (20, 35, 30, 35, 27)
#womenMeans = (25, 32, 34, 20, 25)
#menStd = (2, 3, 4, 1, 2)
#womenStd = (3, 5, 2, 3, 3)
ind = np.arange(N)    # the x locations for the groups
#width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = ax.bar(df2.index, df2.Ryegrass)
p2 = ax.bar(ind, womenMeans, width, color=(1.0,0.5,0.62),
             bottom=menMeans)
ax.set_ylabel('Scores')
ax.set_xlabel('Groups')
ax.set_title('Scores by group and gender')

ax.set_xticks(ind + width/2.)
ax.set_yticks(np.arange(0, 81, 10))
ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

plotly_fig = tls.mpl_to_plotly( mpl_fig )

# For Legend
plotly_fig["layout"]["showlegend"] = True
plotly_fig["data"][0]["name"] = "Men"
plotly_fig["data"][1]["name"] = "Women"
py.iplot(plotly_fig, filename='stacked-bar-chart')