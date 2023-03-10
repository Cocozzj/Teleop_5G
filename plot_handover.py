from utils.context import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

NUM_BINS=100
TABLE_COLUMN=['Radio Time','4G Configuration Duration','5G Configuration Duration']
def distribution_plot(datapath,plotFolder):
    data = pd.read_csv(datapath)
    for index in TABLE_COLUMN:
        histplot=data.plot.hist(column=[index],bins=NUM_BINS)
        histplot.set_ylabel(index)
        plt.tight_layout()
        plt.savefig(plotFolder+index+'-plot.png')
        plt.close()


if __name__ == '__main__':
    for file in os.listdir(path.join(TASK3_DIR, "Table\\")):
        if file.endswith('.csv'):
            filename= file.split(".")[0]
            datapath = path.join(TASK3_DIR, "Table\\" + filename + ".csv")
            plotFolder= path.join(TASK3_DIR, "Plot\\" + filename + "\\")
            if not os.path.exists(plotFolder):
                os.makedirs(plotFolder)
            print("Creating Histogram for: " + filename)
            distribution_plot(datapath,plotFolder)

