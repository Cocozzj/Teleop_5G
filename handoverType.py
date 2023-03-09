from utils.context import *
import numpy as np
import pandas as pd

filename='CHICAGOAIRPORT-M3-1S-HO'

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
LTE_ATTEMPT='Handover Attempt'
LTE_SUCCESS='Handover Success'

NR_4GPCELL_CHANGE_TYPE='5G-NR RRC ENDC MeNB PCell Change MeNB Pcell Change Type'
NR_PCI='5G KPI PCell RF Serving PCI'
NR_BAND='5G KPI PCell RF Band'
NR_EVENT="Event 5G-NR Events"
NR_CHANGE_TYPE='5G-NR RRC NR SCG Mobility Statistics NR SCG Mobility Type'
NR_RADIO_TIME='5G-NR RRC NR SCG Mobility Statistics Duration [sec]'
NR_NSA_CONFIGURATION_TIME_LTE2NR='Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[LTE to NR] [sec]'
NR_NSA_CONFIGURATION_TIME_NR2NR='Qualcomm 5G-NR MAC RACH Info Latency KPI Handover Latency[NR to NR] [sec]'
NR_SA_TIME_NR2NR='5G-NR RRC NR MCG Mobility Statistics Intra-NR HandoverDuration [sec]'
NSA_SUCCESS='NR SCG Modification Success'
NSA_ATTEMPT='NR SCG Modification Attempt'
SA_SUCCESS='NR MCG Handover Success	 '
SA_ATTEMPT='NR MCG Handover Attempt	 '

EVENT_COLUMN=[LTE_EVENT,LTE_OLD_PCI,LTE_NEW_PCI,NR_EVENT,NR_CHANGE_TYPE,NR_4GPCELL_CHANGE_TYPE]
DURATION_COLUMN=[LTE_RADIO_TIME,LTE_CONFIGURATION_TIME,NR_RADIO_TIME,NR_NSA_CONFIGURATION_TIME_LTE2NR,NR_NSA_CONFIGURATION_TIME_NR2NR,NR_SA_TIME_NR2NR]

EVENT_LEN=len(EVENT_COLUMN)
DURATION_LEN=len(DURATION_COLUMN)

# =====================================================================================
# Identify the event techologies
connection_type=[]
EventTech_summary=data['Event Technology'].dropna(axis=0,how='all').unique()
for type in EventTech_summary:
    if 'LTE' in type:
        connection_type.append("LTE")
    elif '5G-NR_NSA' in type:
        connection_type.append("5G-NR_NSA")
    elif '5G-NR_SA' in type:
        connection_type.append("5G-NR_SA")
connection_type=pd.Series(connection_type).unique()
connection_type.sort()
print("Connection Type:",connection_type)
signalInfo_index=[]
eventInfo_index=[]
durationInfo_index=[]
for type in connection_type:
    if type=='LTE':
        signalInfo_index.extend([LTE_PCI,LTE_BAND])
        eventInfo_index.extend([LTE_EVENT,LTE_OLD_PCI,LTE_NEW_PCI])
        durationInfo_index.extend([LTE_RADIO_TIME,LTE_CONFIGURATION_TIME])
    elif type == '5G-NR_NSA':
        signalInfo_index.extend([LTE_PCI,LTE_BAND,NR_PCI,NR_BAND])
        eventInfo_index.extend([LTE_EVENT,LTE_OLD_PCI,LTE_NEW_PCI,NR_EVENT,NR_CHANGE_TYPE,NR_4GPCELL_CHANGE_TYPE])
        durationInfo_index.extend([LTE_RADIO_TIME,LTE_CONFIGURATION_TIME,NR_RADIO_TIME,NR_NSA_CONFIGURATION_TIME_LTE2NR,NR_NSA_CONFIGURATION_TIME_NR2NR])
    elif type == '5G-NR_SA':
        signalInfo_index.extend([NR_PCI,NR_BAND])
        eventInfo_index.extend([NR_EVENT])
        durationInfo_index.extend([NR_SA_TIME_NR2NR])
signalInfo_index=sorted(set(signalInfo_index))
eventInfo_index=sorted(set(eventInfo_index))
durationInfo_index=sorted(set(durationInfo_index))

# =====================================================================================
# Loading data
signalInfo = data[signalInfo_index]
signalInfo=signalInfo.dropna(axis=0,how='all')
signalInfo.fillna(value='None',inplace=True)

eventInfo = data[eventInfo_index]
eventInfo=eventInfo.dropna(axis=0,how='all')
for name in EVENT_COLUMN:
    if not name in eventInfo.columns.values.tolist():
        eventInfo[name]=np.nan

eventInfo=eventInfo[(eventInfo[NR_EVENT]==SA_ATTEMPT) | (eventInfo[NR_EVENT]==NSA_ATTEMPT) | (eventInfo[LTE_EVENT]==LTE_SUCCESS) | (eventInfo[LTE_EVENT]==LTE_ATTEMPT) | (eventInfo[NR_EVENT]==NSA_SUCCESS) | (eventInfo[NR_EVENT]==SA_SUCCESS)]
eventInfo_pro=pd.DataFrame()
index=0
while index < len(eventInfo)-1:
    if eventInfo.iloc[index][NR_EVENT]==SA_ATTEMPT and eventInfo.iloc[index+1][NR_EVENT]!=SA_SUCCESS :
        index = index +2
        eventInfo_pro = pd.concat([eventInfo_pro, eventInfo.iloc[index], eventInfo.iloc[index+1]])
    elif eventInfo.iloc[index][NR_EVENT]==NSA_ATTEMPT and eventInfo.iloc[index+1][NR_EVENT]==NSA_SUCCESS :
        if eventInfo.iloc[index][LTE_EVENT]=='None' | (eventInfo.iloc[index][LTE_EVENT]==LTE_ATTEMPT and eventInfo.iloc[index+1][LTE_EVENT]==LTE_SUCCESS):
            index = index +2
            eventInfo_pro = pd.concat([eventInfo_pro, eventInfo.iloc[index], eventInfo.iloc[index+1]])
        else: 
            index = index +1
    elif eventInfo.iloc[index][LTE_EVENT]==LTE_ATTEMPT and eventInfo.iloc[index+1][LTE_EVENT]==LTE_SUCCESS :
        index = index +2
        eventInfo_pro = pd.concat([eventInfo_pro, eventInfo.iloc[index], eventInfo.iloc[index+1]])
    else:
        index = index + 1
            
eventInfo=eventInfo_pro
eventInfo.fillna(value='None',inplace=True)

#eventInfo.to_csv('./eventInfo.csv')

durationInfo = data[durationInfo_index]
durationInfo=durationInfo.dropna(axis=0,how='all')
if LTE_CONFIGURATION_TIME in durationInfo.columns.values.tolist():
    durationInfo[LTE_CONFIGURATION_TIME]=durationInfo[LTE_CONFIGURATION_TIME] / 1000
for name in DURATION_COLUMN:
    if not name in durationInfo.columns.values.tolist():
        durationInfo[name]=np.nan


event_duration_info=pd.concat([eventInfo, durationInfo], axis=1).sort_index(ascending=True)
event_duration_info.reset_index(inplace=True)
#durationInfo.to_csv('./duration.csv')

event_duration_info.to_csv('./event_duration.csv')
# =====================================================================================
# process event-duration data
def event_dur_each(dataframe):

    df_event_duration = pd.DataFrame(columns=['index','Type','Radio Time', '4G Configuration Duration', '5G Configuration Duration','oldPCI','newPCI'],index=[0])

    duration=dataframe.iloc[1:,-DURATION_LEN:]
    for col_index in range(DURATION_LEN):
        dataframe_notnan = duration[~np.isnan(duration.iloc[:,col_index])].iloc[:,col_index].values   
        if dataframe_notnan.size>0:
            duration.iloc[:,col_index].fillna(dataframe_notnan[0],inplace=True)
    duration=duration.iloc[0]
    event=dataframe.iloc[0]
   
    if event[NR_EVENT]==SA_ATTEMPT:

        df_event_duration['Type']='5GSA_5GSA'
        df_event_duration['Radio Time']=duration[NR_SA_TIME_NR2NR]
    elif event[LTE_EVENT]!='None' and event[NR_EVENT]=='None' and event[NR_CHANGE_TYPE]=='None' and event[NR_4GPCELL_CHANGE_TYPE]=='None':
        if event[LTE_OLD_PCI]!=event[LTE_NEW_PCI]:
            df_event_duration['Type']='4G_4G'
            df_event_duration['Radio Time']=duration[LTE_RADIO_TIME] if ~np.isnan(duration[LTE_RADIO_TIME]) else duration[NR_RADIO_TIME]
        else:
            df_event_duration['Type']='5GNSA_4G'
            df_event_duration['Radio Time']=duration[LTE_RADIO_TIME] if ~np.isnan(duration[LTE_RADIO_TIME]) else duration[NR_RADIO_TIME]
    elif event[LTE_EVENT]=='None' and event[NR_EVENT]!='None' and ~np.isnan(duration[NR_NSA_CONFIGURATION_TIME_NR2NR]) and np.isnan(duration[LTE_CONFIGURATION_TIME]):
            df_event_duration['Type']='5GNSA_5GChange'
            df_event_duration['Radio Time']=duration[LTE_RADIO_TIME] if ~np.isnan(duration[LTE_RADIO_TIME]) else duration[NR_RADIO_TIME]
    elif event[LTE_EVENT]!='None' and event[NR_EVENT]!='None':    
        if ~np.isnan(duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) and np.isnan(duration[NR_NSA_CONFIGURATION_TIME_NR2NR]):
            df_event_duration['Type']='4G_5GNSA'
            df_event_duration['Radio Time']=duration[LTE_RADIO_TIME] if ~np.isnan(duration[LTE_RADIO_TIME]) else duration[NR_RADIO_TIME]
        elif np.isnan(duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) and ~np.isnan(duration[NR_NSA_CONFIGURATION_TIME_NR2NR]) and event[LTE_OLD_PCI]!=event[LTE_NEW_PCI]: 
            df_event_duration['Type']='5GNSA_4GChange'
            df_event_duration['Radio Time']=duration[LTE_RADIO_TIME] if ~np.isnan(duration[LTE_RADIO_TIME]) else duration[NR_RADIO_TIME]
    
    df_event_duration['index']=event['index']
    df_event_duration['4G Configuration Duration']=duration[LTE_CONFIGURATION_TIME]
    df_event_duration['5G Configuration Duration']=duration[NR_NSA_CONFIGURATION_TIME_LTE2NR] if ~np.isnan(duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) else duration[NR_NSA_CONFIGURATION_TIME_NR2NR]
    df_event_duration['newPCI']=event[LTE_NEW_PCI]
    df_event_duration['oldPCI']=event[LTE_OLD_PCI]

    return df_event_duration

df_event_duration=pd.DataFrame()
for idk in range(2,len(eventInfo),2):
    pre=eventInfo.iloc[idk-2].name
    next=eventInfo.iloc[idk].name
    print(pre,next)
    index_pre=event_duration_info[event_duration_info['index']==pre].index.values[0]
    index_next=event_duration_info[event_duration_info['index']==next].index.values[0]
    cut_pd=event_duration_info.iloc[index_pre:index_next]
    df=event_dur_each(cut_pd)
   
    df_event_duration=pd.concat([df_event_duration,df])
df_event_duration.to_csv('./df_event_duration.csv')


