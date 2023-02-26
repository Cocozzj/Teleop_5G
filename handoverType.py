from utils.context import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

filename='CHICAGOAIRPORT-M1-1S-HO.csv'

path = path.join(DATA_DIR,"HandOver\\"+filename)
data = pd.read_csv(path)

# =====================================================================================
signalInfo = data[['LTE KPI PCell Serving PCI','LTE KPI PCell Serving Band','5G KPI PCell RF Serving PCI','5G KPI PCell RF Band']]
signalInfo.columns=['4GPCI','4GBand','5GPCI','5GBand']
signalInfo=signalInfo.dropna(axis=0,how='all')

durationInfo = data[['HO Statistics Intra-LTE HO Duration [sec]','5G-NR RRC NR SCG Mobility Statistics Duration [sec]','Random Access Procedure Latency KPI Handover Latency(ms) (Chipset-Based)','Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[LTE to NR] [sec]','Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[NR to NR] [sec]']]
durationInfo.columns=['P','T','Q','U','V']
durationInfo=durationInfo.dropna(axis=0,how='all')
pd.set_option('display.max_rows', None)

# =====================================================================================
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
        durationTime.append([radio_time,lte_time,nr_time])

raw_time=pd.DataFrame(raw_time)
raw_time.to_csv('./duration.csv', index=True)
durationTime=pd.DataFrame(durationTime,columns=['Radio Duration','4G Configuration Duration','5G Configuration Duration'])
print(len(durationTime))

# =====================================================================================
def techIndentify(row):
    if ~np.isnan(row['4GPCI']):
        if np.isnan(row['5GPCI']):
            type = '4G'
        else:
            type = '5GNSA'
    elif np.isnan(row['4GPCI']) and not (np.isnan(row['5GPCI']) ):
        type ='5GSA'

    return type

handover_list=[]
for index in range(len(signalInfo)-1):
    row = signalInfo.iloc[index]
    next = signalInfo.iloc[index+1]
    print(row)
    handoverType=''
    if techIndentify(row) =='4G':
        if techIndentify(next) == '4G' and row['4GPCI']!=next['4GPCI'] :
            handoverType="4G_4G"
        elif techIndentify(next) == '5GNSA':
            handoverType="4G_5GNSA"
    elif techIndentify(row) =='5GSA':
        if techIndentify(next) == '5GSA' and row['5GPCI']!=next['5GPCI']:
            handoverType="5GSA_5GSA"
    elif techIndentify(row) =='5GNSA':
        if techIndentify(next) == '4G':
            handoverType="5GNSA_4G"
        elif techIndentify(next) == '5GNSA':
            if row['4GPCI']==next['4GPCI'] and row['5GPCI']!=next['5GPCI'] :
                handoverType = "5GNSA_5Gchange"
            elif row['5GPCI']==next['5GPCI'] and row['4GPCI']!=next['4GPCI'] :
                handoverType = "5GNSA_4Gchange"
            elif row['5GPCI']!=next['5GPCI'] and row['4GPCI']!=next['4GPCI']:
                handoverType = "5GNSA_4G5Gchange"
    if handoverType!="":
        handover_list.append((row.name,handoverType))

handover_list=pd.DataFrame(handover_list)
print(handover_list)
print(len(handover_list))
handover_list.to_csv('./handover_list.csv', index=True)

# def techIndentify(row):
#     if ~np.isnan(row['4GPCI']) and isinstance(row['4GBand'], str):
#         if np.isnan(row['5GPCI']) and isinstance(row['5GBand'], float):
#             type = '4G'
#         else:
#             type = '5GNSA'
#     elif np.isnan(row['4GPCI']) and isinstance(row['4GBand'], float) and not (np.isnan(row['5GPCI']) or isinstance(row['5GBand'], float)):
#         type ='5GSA'
#
#     return type

# handover_list=[]
# for index in range(len(signalInfo)-1):
#     row = signalInfo.iloc[index]
#     next = signalInfo.iloc[index+1]
#     handoverType=''
#     if techIndentify(row) =='4G':
#         if techIndentify(next) == '4G' and (row['4GPCI']!=next['4GPCI'] or row['4GBand']!=next['4GBand']):
#             handoverType="4G_4G"
#         elif techIndentify(next) == '5GNSA':
#             handoverType="4G_5GNSA"
#     elif techIndentify(row) =='5GSA':
#         if techIndentify(next) == '5GSA' and (row['5GPCI']!=next['5GPCI'] or row['5GBand']!=next['5GBand']):
#             handoverType="5GSA_5GSA"
#     elif techIndentify(row) =='5GNSA':
#         if techIndentify(next) == '4G':
#             handoverType="5GNSA_4G"
#         elif techIndentify(next) == '5GNSA':
#             if row['4GPCI']==next['4GPCI'] and row['4GBand']==next['4GBand'] and (row['5GPCI']!=next['5GPCI'] or row['5GBand']!=next['5GBand']):
#                 handoverType = "5GNSA_5Gchange"
#             elif row['5GPCI']==next['5GPCI'] and row['5GBand']==next['5GBand'] and (row['4GPCI']!=next['4GPCI'] or row['4GBand']!=next['4GBand']):
#                 handoverType = "5GNSA_4Gchange"
#             elif (row['5GPCI']!=next['5GPCI'] or row['5GBand']!=next['5GBand']) and (row['4GPCI']!=next['4GPCI'] or row['4GBand']!=next['4GBand']):
#                 handoverType = "5GNSA_4G5Gchange"
#     if handoverType!="":
#         handover_list.append(handoverType)