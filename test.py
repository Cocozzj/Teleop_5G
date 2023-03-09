from utils.context import *
import numpy as np
import pandas as pd

filename='CHICAGOAIRPORT-M1-1S-HO'

datapath = path.join(DATA_DIR,"HandOver\\"+filename+".csv")
tablepath = path.join(DATA_DIR,"HandOver\\"+filename+"-DurationTable.csv")
data = pd.read_csv(datapath,dtype = 'str')

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
NR_SA_TIME_NR2NR='5G-NR RRC NR MCG Mobility Statistics Intra-NR HandoverDuration [sec]'

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
print(connection_type)
signalInfo_index=[]
eventInfo_index=[]
durationInfo_index=[]
for type in connection_type:
    if type=='LTE':
        signalInfo_index.extend((LTE_PCI,LTE_BAND))
        eventInfo_index.extend((LTE_EVENT,LTE_OLD_PCI,LTE_NEW_PCI))
        durationInfo_index.extend((LTE_RADIO_TIME,LTE_CONFIGURATION_TIME))
    elif type == '5G-NR_NSA':
        signalInfo_index.extend((NR_PCI,NR_BAND))
        eventInfo_index.extend((NR_EVENT,NR_CHANGE_TYPE,NR_4GPCELL_CHANGE_TYPE))
        durationInfo_index.extend((NR_RADIO_TIME,NR_NSA_CONFIGURATION_TIME_LTE2NR,NR_NSA_CONFIGURATION_TIME_NR2NR))
    elif type == '5G-NR_SA':
        signalInfo_index.extend((NR_PCI,NR_BAND))
        eventInfo_index.extend((NR_EVENT))
        durationInfo_index.extend((NR_SA_TIME_NR2NR))

sorted(set(signalInfo_index), key = signalInfo_index.index)
sorted(set(eventInfo_index), key = eventInfo_index.index)
sorted(set(durationInfo_index), key = durationInfo_index.index)

# =====================================================================================
# Loading data
signalInfo = data[signalInfo_index]
signalInfo=signalInfo.dropna(axis=0,how='all')
signalInfo.fillna(value='None',inplace=True)

eventInfo = data[eventInfo_index]
eventInfo=eventInfo.dropna(axis=0,how='all')
for type in connection_type:
    if type=='LTE':
        eventInfo=eventInfo[(eventInfo[LTE_EVENT]=='Handover Attempt') | (eventInfo[LTE_EVENT]=='Handover Success')]
    elif type == '5G-NR_NSA':
        eventInfo=eventInfo[(eventInfo[NR_EVENT]=='NR SCG Modification Attempt')|(eventInfo[NR_EVENT]=='NR SCG Modification Success')]
    elif type == '5G-NR_SA':
        eventInfo=eventInfo[(eventInfo[NR_EVENT]=='NR MCG Handover Attempt')|(eventInfo[NR_EVENT]=='NR MCG Handover Success')]
eventInfo.fillna(value='None',inplace=True)
# eventInfo_len=len(eventInfo.columns.values.tolist())

durationInfo = data[durationInfo_index]
durationInfo=durationInfo.dropna(axis=0,how='all')
durationInfo=durationInfo.astype('float')
if LTE_CONFIGURATION_TIME in durationInfo.columns.values.tolist():
    durationInfo[LTE_CONFIGURATION_TIME]=durationInfo[LTE_CONFIGURATION_TIME] / 1000
durationInfo_len=len(durationInfo.columns.values.tolist())

event_duration_info=pd.concat([eventInfo, durationInfo], axis=1).sort_index(ascending=True)
event_duration_info.reset_index(inplace=True)
event_duration_info.to_csv('./event_duration.csv')
# =====================================================================================
# process event-duration data
def event_dur_each(dataframe,connection_type,durationInfo_len,eventInfo_len):
    df_event_duration = pd.DataFrame(columns=['Type','Radio Time', '4G Configuration Duration', '5G Configuration Duration'])
    duration=dataframe.iloc[:,-durationInfo_len:]
    for col_index in range(durationInfo_len):
        dataframe_notnan = duration[~duration.iloc[:,col_index].isna()].iloc[:,col_index].values
        if dataframe_notnan.size>0:
            duration.iloc[:,col_index].fillna(dataframe_notnan[0],inplace=True)
        # process_data['U'].fillna(U_notnan[0],inplace=True)a
    duration=duration.iloc[[0]]

    event=dataframe.iloc[0,0:eventInfo_len]
    if len(connection_type)==1:
        if connection_type[0]=='LTE':
            df_event_duration['Radio Time']=duration[LTE_RADIO_TIME]
            df_event_duration['Type']='4G_4G'
            df_event_duration['4G Configuration Duration']=duration[LTE_CONFIGURATION_TIME]
        elif connection_type[0]=='5G-NR_SA':
            df_event_duration['Radio Time']=duration[NR_SA_TIME_NR2NR]
            df_event_duration['Type']='5GSA_5GSA'
        elif connection_type[0]=='5G-NR_NSA':
            df_event_duration['Radio Time']=duration[NR_RADIO_TIME]
            df_event_duration['5G Configuration Duration']=duration[LTE_CONFIGURATION_TIME]
            if event['']
            if event['NR_CHANGE_TYPE']!=None:
                if event[NR_4GPCELL_CHANGE_TYPE]=='None':
                    df_event_duration['Type']='5GNSA_5GChange'    


    
    # if dataframe[[LTE_EVENT]].iloc[1].values[0]!='NR MCG Handover Success' and dataframe[[NR_EVENT]].iloc[1].values[0]!='Handover Success':
    #     P=dataframe[~dataframe[LTE_RADIO_TIME].isna()][LTE_RADIO_TIME].values[0]
    #     T=dataframe[~dataframe[NR_RADIO_TIME].isna()][NR_RADIO_TIME].values[0]
    #     if P==T:
    #         radio_time= P
    #     else:
    #         print("ERROR: P!=T")
    #     lte_time=dataframe[~dataframe[LTE_CONFIGURATION_TIME].isna()][LTE_CONFIGURATION_TIME].values[0]

for idk in range(2,len(eventInfo),2):
    pre=eventInfo.iloc[idk-2].name
    next=eventInfo.iloc[idk].name
    
    index_pre=event_duration_info[event_duration_info['index']==pre].index.values[0]
    index_next=event_duration_info[event_duration_info['index']==next].index.values[0]
    cut_pd=event_duration_info.iloc[index_pre:index_next]
    event_dur_each(cut_pd,connection_type,durationInfo_len,eventInfo_len)

# Integrate duration time
# durationTime=[]
# raw_time=[]
# for index in range(len(durationInfo)-1):
#     row=durationInfo.iloc[index]
#     if not (np.isnan(row['P']) and np.isnan(row['T'])):

#         if not (np.isnan(row['P']) or np.isnan(row['T'])):
#             process_data=durationInfo.iloc[index:index+3]
#         elif np.isnan(row['P']) or np.isnan(row['T']):
#             process_data = durationInfo[index:index + 2]

#         Q_notnan = process_data[~process_data['Q'].isna()]['Q'].values
#         U_notnan = process_data[~process_data['U'].isna()]['U'].values
#         V_notnan = process_data[~process_data['V'].isna()]['V'].values
#         W_notnan = process_data[~process_data['W'].isna()]['W'].values

#         if Q_notnan.size>0:
#             process_data['Q'].fillna(Q_notnan[0], inplace=True)
#         if U_notnan.size>0:
#             process_data['U'].fillna(U_notnan[0],inplace=True)
#         if V_notnan.size>0:
#             process_data['V'].fillna(V_notnan[0],inplace=True)
#         if W_notnan.size>0:
#             process_data['W'].fillna(W_notnan[0],inplace=True)    

#         radio_time = process_data.iloc[0, 0] if np.isnan(process_data.iloc[0, 1]) else process_data.iloc[0, 1]
#         lte_time = process_data.iloc[0, 2]
#         if ~np.isnan(process_data.iloc[0, 3]):
#             nr_time = process_data.iloc[0, 3]
#         elif  ~np.isnan(process_data.iloc[0, 4]):
#             nr_time = process_data.iloc[0, 4]
#         elif  ~np.isnan(process_data.iloc[0, 5]):
#             nr_time = process_data.iloc[0, 5]
      
#         raw_time.append(process_data.iloc[0])
#         durationTime.append([process_data.iloc[0].name,radio_time,lte_time,nr_time])

# raw_time=pd.DataFrame(raw_time)
# durationTime=pd.DataFrame(durationTime,columns=['index','Radio Duration','4G Configuration Duration','5G Configuration Duration'])
# durationTime.to_csv('./duration.csv',index=False)

# # =====================================================================================

# eventInfo.to_csv('./eventInfo.csv',index=False)
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

=======
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
# >>>>>>> f5ef09a (Updated)
