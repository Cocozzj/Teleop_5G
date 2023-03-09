from utils.context import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data =np.array([[2.8 , 0 , 97.2, 7.00],
       [81.1, 14.7 , 4.2, 12.23],
       [20.8, 0 , 79.2, 13.85],
       [0 , 0 , 100, 0.98],
       [0.5, 98.5, 1.0, 7.77],
       [78.5, 0, 21.2, 0.04]])
data = pd.DataFrame(data,columns=['5G-NSA-UL','5G-SA-UL','4G-UL','Outage'],index=["VZ","TMB","ATT","VZ","TMB","ATT"],dtype='float')
data["Scenario"]=["Highway","Highway" ,"Highway", "Urban", "Urban","Urban"]
colors = ["#90d595","#aafbff","#adb0ff"]

# =====================================================================================
highwayData=data[data['Scenario']=="Highway"][['4G-UL','5G-NSA-UL','5G-SA-UL']]
labels = highwayData.index

ax = highwayData.plot.bar(rot=0,stacked=True,color=colors, figsize=(10, 7))
ax.set_ylabel('Deployment Type',fontsize=25)
ax.set_xlabel('Carrier',fontsize=25)
ax.set_xticks(np.arange(0, len(labels)), labels=labels,fontsize=25)
plt.legend(loc='upper center', fontsize=20,bbox_to_anchor=(0,1,1,0.15),ncol=len(labels))
plt.title('Highway Coverage Ratio',fontsize=25, y=1.15)
plt.grid(linestyle='--', axis='y')
plt.tight_layout()
#plt.show()
plt.savefig(path.join(RESULT_DIR, 'highway_UL_carrierRatio.png'))
plt.close()

# =====================================================================================
urbanData=data[data['Scenario']=="Urban"][['4G-UL','5G-NSA-UL','5G-SA-UL']]
labels = urbanData.index

ax = urbanData.plot.bar(rot=0,stacked=True,color=colors, figsize=(10, 7))
ax.set_ylabel('Deployment Type',fontsize=25)
ax.set_xlabel('Carrier',fontsize=25)
ax.set_xticks(np.arange(0, len(labels)), labels=labels,fontsize=25)
plt.legend(loc='upper center', fontsize=20,bbox_to_anchor=(0,1,1,0.15),ncol=len(labels))
plt.title('Urban Coverage Ratio',fontsize=25, y=1.15)
plt.grid(linestyle='--', axis='y')
plt.tight_layout()

#plt.show()
plt.savefig(path.join(RESULT_DIR, 'urban_UL_carrierRatio.png'))
plt.close()