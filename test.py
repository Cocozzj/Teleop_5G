from utils.context import *
import numpy as np
import pandas as pd

filename='CHICAGOAIRPORT-M1-1S-HO'

datapath = path.join(DATA_DIR,"HandOver\\"+filename+".csv")
tablepath = path.join(DATA_DIR,"HandOver\\"+filename+"-DurationTable.csv")
data = pd.read_csv(datapath)

# =====================================================================================
# Const Variable
LTE_PCI='LTE KPI PCell Serving PCI'
LTE_BAND='LTE KPI PCell Serving Band'
LTE_EVENT='Event LTE Events'
LTE_OLD_PCI='HO Statistics Intra-LTE HO Source PCI'
LTE_NEW_PCI='HO Statistics Intra-LTE HO Target PCI'
LTE_RADIO_TIME='HO Statistics Intra-LTE HO Duration [sec]'
LTE_CONFIGURATION_TIME='Random Access Procedure Latency KPI Handover Latency(ms) (Chipset-Based)'

NR_4GPCELL_CHANGE_TYPE='5G-NR RRC ENDC MeNB PCell Change MeNB Pcell Change Type'
NR_PCI='5G KPI PCell RF Serving PCI'
NR_BAND='5G KPI PCell RF Band'
NR_EVENT='Event 5G-NR Events'
NR_CHANGE_TYPE='5G-NR RRC NR SCG Mobility Statistics NR SCG Mobility Type'
NR_RADIO_TIME='5G-NR RRC NR SCG Mobility Statistics Duration [sec]'
NR_NSA_CONFIGURATION_TIME_LTE2NR='Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[LTE to NR] [sec]'
NR_NSA_CONFIGURATION_TIME_NR2NR='Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[NR to NR] [sec]'
NR_SA_CONFIGURATION_TIME_NR2NR='5G-NR RRC NR MCG Mobility Statistics Intra-NR HandoverDuration [sec]'

# =====================================================================================
# Identify the event techologies
type_total=[]
EventTech_summary=data['Event Technology'].dropna(axis=0,how='all').unique()
for type in EventTech_summary:
    if 'LTE' in type:
        type_total.append("LTE")
    if '5G-NR_NSA' in type:
        type_total.append("5G-NR_NSA")
    if '5G-NR_SA' in type:
        type_total.append("5G-NR_SA")
type_total=pd.Series(type_total).unique()

signalInfo_index=[]
eventInfo_index=[]
durationInfo_index=[]
for type in type_total:
    if type=='LTE':
        signalInfo_index.append()
        eventInfo_index.append()
        durationInfo_index.append()

# =====================================================================================
# Loading data
signalInfo = data[['LTE KPI PCell Serving PCI','LTE KPI PCell Serving Band','5G KPI PCell RF Serving PCI','5G KPI PCell RF Band']]
signalInfo.columns=['4GPCI','4GBand','5GPCI','5GBand']
signalInfo=signalInfo.dropna(axis=0,how='all')
values = {'4GPCI': '-1', '4GBand': 'None', '5GPCI': -1, '5GBand': 'None'}
signalInfo.fillna(value=values,inplace=True)

eventInfo = data [['Event LTE Events','Event 5G-NR Events','5G-NR RRC NR SCG Mobility Statistics NR SCG Mobility Type','5G-NR RRC ENDC MeNB PCell Change MeNB Pcell Change Type','HO Statistics Intra-LTE HO Source PCI','HO Statistics Intra-LTE HO Target PCI']]
eventInfo.columns=['4GEvents','5GEvents','5GType','4GPcellChange','4GOldPCI','4GNewPCI']
eventInfo=eventInfo.dropna(axis=0,how='all')
eventInfo=eventInfo[(eventInfo['4GEvents']=='Handover Attempt') | (eventInfo['4GEvents']=='Handover Success')|(eventInfo['5GEvents']=='NR SCG Modification Attempt')|(eventInfo['5GEvents']=='NR SCG Modification Success')]
values = {'4GEvents':'None','5GEvents':'None','5GType': 'None', '4GPcellChange':'None','4GOldPCI': '-1', '4GNewPCI': -1}
eventInfo.fillna(value=values,inplace=True)

durationInfo = data[['HO Statistics Intra-LTE HO Duration [sec]','5G-NR RRC NR SCG Mobility Statistics Duration [sec]','Random Access Procedure Latency KPI Handover Latency(ms) (Chipset-Based)','Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[LTE to NR] [sec]','Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[NR to NR] [sec]','5G-NR RRC NR MCG Mobility Statistics Intra-NR HandoverDuration [sec]']]
durationInfo.columns=['P','T','Q','U','V','W']
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
        W_notnan = process_data[~process_data['W'].isna()]['W'].values

        if Q_notnan.size>0:
            process_data['Q'].fillna(Q_notnan[0], inplace=True)
        if U_notnan.size>0:
            process_data['U'].fillna(U_notnan[0],inplace=True)
        if V_notnan.size>0:
            process_data['V'].fillna(V_notnan[0],inplace=True)
        if W_notnan.size>0:
            process_data['W'].fillna(W_notnan[0],inplace=True)    

        radio_time = process_data.iloc[0, 0] if np.isnan(process_data.iloc[0, 1]) else process_data.iloc[0, 1]
        lte_time = process_data.iloc[0, 2]
        if ~np.isnan(process_data.iloc[0, 3]):
            nr_time = process_data.iloc[0, 3]
        elif  ~np.isnan(process_data.iloc[0, 4]):
            nr_time = process_data.iloc[0, 4]
        elif  ~np.isnan(process_data.iloc[0, 5]):
            nr_time = process_data.iloc[0, 5]
      
        raw_time.append(process_data.iloc[0])
        durationTime.append([process_data.iloc[0].name,radio_time,lte_time,nr_time])

raw_time=pd.DataFrame(raw_time)
durationTime=pd.DataFrame(durationTime,columns=['index','Radio Duration','4G Configuration Duration','5G Configuration Duration'])
durationTime.to_csv('./duration.csv',index=False)

# =====================================================================================

eventInfo.to_csv('./eventInfo.csv',index=False)
# Integrate Event Info
# def handoverEst(row):
#     type="None"
#     if row['4GEvents']!='None':
#         if row['5GEvents']!='None':
            
        
# for index in range(len(eventInfo)-1):
#     row=eventInfo.iloc[index]




# # =====================================================================================
# # Integrate band info
# def techIndentify(row):
#     if row['4GPCI']!=-1 or row['4GBand']!='None':
#         if row['5GPCI']==-1 and row['5GBand']=='None':
#             type = '4G'
#         else:
#             type = '5GNSA'
#     elif row['4GPCI']==-1 and row['4GBand']=='None' and (row['5GPCI']!=-1 or row['5GBand']!='None'):
#         type ='5GSA'

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
#         handover_list.append((row.name,handoverType))

# handover_list=pd.DataFrame(handover_list)
# handover_list.columns=['index','handoverType']
# handover_list.to_csv('./handover_list.csv',index=False)


# # =====================================================================================
# # Integrate two table
# if (len(handover_list)==len(durationTime)):
#     tablepd = pd.concat([handover_list['handoverType'], durationTime],axis=1)
#     tablepd.to_csv(tablepath, index=False)
#     print(tablepath+": Table is completed")
# else:
#     print("#haveoverType:" + str(len(handover_list))+ ";    #duration:" +str(len(durationTime)))

