import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.context import *

if __name__ == '__main__':
    fullDataset = pd.read_csv(path.join(DATA_DIR, 'full-dataset.csv'))

    # =====================================================================================
    abstractTechLabel = 'Abstract-Tech-Label'
    tputUpLabel = 'Total UL Tput (Mbps)'
    tputDlLabel = 'Total DL Tput (Mbps)'
    # technologiesSeen = fullDataset[technologyLabel].unique()[:-1]
    technologiesSeen = fullDataset[fullDataset[abstractTechLabel].notna()]
    technologiesSeen = technologiesSeen[abstractTechLabel].unique()
    uploadDataSet = fullDataset[fullDataset['Direction'] == 'UP']
    uploadDataSet = uploadDataSet[uploadDataSet[abstractTechLabel] != 'NO SERVICE']
    downloadDataSet = fullDataset[fullDataset['Direction'] == 'DL']

    # =====================================================================================
    data = uploadDataSet.groupby(abstractTechLabel)[tputUpLabel].agg(lambda x: list(x))
    labels = data.index
    fig, ax = plt.figure(figsize=(10, 7))

    ax.violinplot(data, showmeans=True, showmedians=True)
    ax.set_ylabel('Speed (Mbps)',fontsize=25)
    ax.set_xlabel('Deployment Type',fontsize=25)
    ax.set_xticks(np.arange(len(labels) + 1), labels=labels,fontsize=25)
    plt.title('Upload Speeds',fontsize=25)
    plt.grid(linestyle='--', axis='y')
    plt.tight_layout()
    plt.savefig(path.join(PLOT_DIR, 'violin-UL-general.png'))
    plt.close()

    # # =====================================================================================
    data = downloadDataSet.groupby(abstractTechLabel)[tputDlLabel].agg(lambda x: list(x))
    labels = data.index
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.violinplot(data, showmeans=True, showmedians=True)
    ax.set_ylabel('Speed (Mbps)',fontsize=25)
    ax.set_xlabel('Deployment Type',fontsize=25)
    ax.set_xticks(np.arange(1, len(labels) + 1), labels=labels,fontsize=25)
    ax.grid(linestyle='--', axis='y')
    plt.title('Download Speeds',fontsize=25)
    plt.tight_layout()

    plt.savefig(path.join(PLOT_DIR, 'violin-DL-general.png'))
    plt.close()
    # =====================================================================================
