from utils.context import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

filename='CHICAGOAIRPORT-M1-1S-HO'

datapath = path.join(DATA_DIR,"HandOver\\"+filename+".csv")
tablepath = path.join(DATA_DIR,"HandOver\\"+filename+"-DurationTable.csv")
data = pd.read_csv(datapath)

# =====================================================================================
# Loading data
signalInfo = data[['LTE KPI PCell Serving PCI','LTE KPI PCell Serving Band','5G KPI PCell RF Serving PCI','5G KPI PCell RF Band']]
signalInfo.columns=['4GPCI','4GBand','5GPCI','5GBand']
signalInfo=signalInfo.dropna(axis=0,how='all')
values = {'4GPCI': '-1', '4GBand': 'None', '5GPCI': -1, '5GBand': 'None'}
signalInfo.fillna(value=values,inplace=True)


durationInfo = data[['HO Statistics Intra-LTE HO Duration [sec]','5G-NR RRC NR SCG Mobility Statistics Duration [sec]','Random Access Procedure Latency KPI Handover Latency(ms) (Chipset-Based)','Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[LTE to NR] [sec]','Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[NR to NR] [sec]']]
durationInfo.columns=['P','T','Q','U','V']
durationInfo=durationInfo.dropna(axis=0,how='all')

# =====================================================================================
# Integrate duration time
durationTime=[]
raw_time=[]
for index in range(len(durationInfo)-1):
    row=durationInfo.iloc[index]
    if not (np.isnan(row['P']) and np.isnan(row['T'])):

        if not (np.isnan(row['P']) or np.isnan(row['T'])):
            process_data=durationInfo.iloc[index:index+3]
        elif np.isnan(row['P']) or np.isnan(row['T']):
            process_data = durationInfo[index:index + 2]

        Q_notnan = process_data[~process_data['Q'].isna()]['Q'].values
        U_notnan = process_data[~process_data['U'].isna()]['U'].values
        V_notnan = process_data[~process_data['V'].isna()]['V'].values

        if Q_notnan.size>0:
            process_data['Q'].fillna(Q_notnan[0], inplace=True)
        if U_notnan.size>0:
            process_data['U'].fillna(U_notnan[0],inplace=True)
        if V_notnan.size>0:
            process_data['V'].fillna(V_notnan[0],inplace=True)

        radio_time = process_data.iloc[0, 0] if np.isnan(process_data.iloc[0, 1]) else process_data.iloc[0, 1]
        lte_time = process_data.iloc[0, 2]
        nr_time = process_data.iloc[0, 4] if np.isnan(process_data.iloc[0, 3]) else process_data.iloc[0, 3]

        raw_time.append(process_data.iloc[0])
        durationTime.append([process_data.iloc[0].name,radio_time,lte_time,nr_time])

raw_time=pd.DataFrame(raw_time)
durationTime=pd.DataFrame(durationTime,columns=['index','Radio Duration','4G Configuration Duration','5G Configuration Duration'])
durationTime.to_csv('./duration.csv',index=False)
# =====================================================================================
# Integrate band info
def techIndentify(row):
    if row['4GPCI']!=-1 or row['4GBand']!='None':
        if row['5GPCI']==-1 and row['5GBand']=='None':
            type = '4G'
        else:
            type = '5GNSA'
    elif row['4GPCI']==-1 and row['4GBand']=='None' and (row['5GPCI']!=-1 or row['5GBand']!='None'):
        type ='5GSA'

    return type

handover_list=[]
for index in range(len(signalInfo)-1):
    row = signalInfo.iloc[index]
    next = signalInfo.iloc[index+1]
    handoverType=''
    if techIndentify(row) =='4G':
        if techIndentify(next) == '4G' and (row['4GPCI']!=next['4GPCI'] or row['4GBand']!=next['4GBand']):
            handoverType="4G_4G"
        elif techIndentify(next) == '5GNSA':
            handoverType="4G_5GNSA"
    elif techIndentify(row) =='5GSA':
        if techIndentify(next) == '5GSA' and (row['5GPCI']!=next['5GPCI'] or row['5GBand']!=next['5GBand']):
            handoverType="5GSA_5GSA"
    elif techIndentify(row) =='5GNSA':
        if techIndentify(next) == '4G':
            handoverType="5GNSA_4G"
        elif techIndentify(next) == '5GNSA':
            if row['4GPCI']==next['4GPCI'] and row['4GBand']==next['4GBand'] and (row['5GPCI']!=next['5GPCI'] or row['5GBand']!=next['5GBand']):
                handoverType = "5GNSA_5Gchange"
            elif row['5GPCI']==next['5GPCI'] and row['5GBand']==next['5GBand'] and (row['4GPCI']!=next['4GPCI'] or row['4GBand']!=next['4GBand']):
                handoverType = "5GNSA_4Gchange"
            elif (row['5GPCI']!=next['5GPCI'] or row['5GBand']!=next['5GBand']) and (row['4GPCI']!=next['4GPCI'] or row['4GBand']!=next['4GBand']):
                handoverType = "5GNSA_4G5Gchange"
    if handoverType!="":
        handover_list.append((row.name,handoverType))

handover_list=pd.DataFrame(handover_list)
handover_list.columns=['index','handoverType']
handover_list.to_csv('./handover_list.csv',index=False)


# =====================================================================================
# Integrate two table
if (len(handover_list)==len(durationTime)):
    tablepd = pd.concat([handover_list['handoverType'], durationTime],axis=1)
    tablepd.to_csv(tablepath, index=False)
    print(tablepath+": Table is completed")
else:
    print("#haveoverType:" + str(len(handover_list))+ ";    #duration:" +str(len(durationTime)))
