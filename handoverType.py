from utils.context import *
import numpy as np
import pandas as pd

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

SIGNAL_COLUMN=[LTE_PCI,LTE_BAND,NR_PCI,NR_BAND]
EVENT_COLUMN=[LTE_EVENT,LTE_OLD_PCI,LTE_NEW_PCI,NR_EVENT,NR_CHANGE_TYPE,NR_4GPCELL_CHANGE_TYPE]
DURATION_COLUMN=[LTE_RADIO_TIME,LTE_CONFIGURATION_TIME,NR_RADIO_TIME,NR_NSA_CONFIGURATION_TIME_LTE2NR,NR_NSA_CONFIGURATION_TIME_NR2NR,NR_SA_TIME_NR2NR]
ALL_COLUMN=SIGNAL_COLUMN+EVENT_COLUMN+DURATION_COLUMN

TABLE_COLUMN=['HandoverType','Radio Time','4G Configuration Duration','5G Configuration Duration']
EVENT_LEN=len(EVENT_COLUMN)
DURATION_LEN=len(DURATION_COLUMN)

def dataloader(data):
    # =====================================================================================
    # Identify the event techologies
    connection_type = []
    EventTech_summary = data['Event Technology'].dropna(axis=0, how='all').unique()
    for type in EventTech_summary:
        if 'LTE' in type:
            connection_type.append("LTE")
        elif '5G-NR_NSA' in type:
            connection_type.append("5G-NR_NSA")
        elif '5G-NR_SA' in type:
            connection_type.append("5G-NR_SA")
    connection_type = pd.Series(connection_type).unique()
    connection_type.sort()

    # =====================================================================================
    # Loading data
    for name in ALL_COLUMN:
        if not name in data.columns.values.tolist():
            data[name] = np.nan

    signalInfo = data[SIGNAL_COLUMN]
    signalInfo = signalInfo.dropna(axis=0, how='all')
    signalInfo.fillna(value='None', inplace=True)

    eventInfo = data[EVENT_COLUMN]
    eventInfo = eventInfo.dropna(axis=0, how='all')
    eventInfo = eventInfo[(eventInfo[NR_EVENT] == SA_ATTEMPT) | (eventInfo[NR_EVENT] == NSA_ATTEMPT) | (
                eventInfo[LTE_EVENT] == LTE_SUCCESS) | (eventInfo[LTE_EVENT] == LTE_ATTEMPT) | (
                                      eventInfo[NR_EVENT] == NSA_SUCCESS) | (eventInfo[NR_EVENT] == SA_SUCCESS)]
    eventInfo.fillna(value='None', inplace=True)
    eventInfo_pro = pd.DataFrame()
    index = 0
    while index < len(eventInfo) - 2:
        if eventInfo.iloc[index][NR_EVENT] == SA_ATTEMPT and eventInfo.iloc[index + 1][NR_EVENT] == SA_SUCCESS:
            eventInfo_pro = pd.concat([eventInfo_pro, eventInfo.iloc[[index]], eventInfo.iloc[[index + 1]]])
            index = index + 2
        elif eventInfo.iloc[index][NR_EVENT] == NSA_ATTEMPT and eventInfo.iloc[index + 1][NR_EVENT] == NSA_SUCCESS:
            if eventInfo.iloc[index][LTE_EVENT] == 'None' or (
                    eventInfo.iloc[index][LTE_EVENT] == LTE_ATTEMPT and eventInfo.iloc[index + 1][
                LTE_EVENT] == LTE_SUCCESS):
                eventInfo_pro = pd.concat([eventInfo_pro, eventInfo.iloc[[index]], eventInfo.iloc[[index + 1]]])
                index = index + 2
            else:
                index = index + 1
        elif eventInfo.iloc[index][LTE_EVENT] == LTE_ATTEMPT and eventInfo.iloc[index + 1][LTE_EVENT] == LTE_SUCCESS:
            eventInfo_pro = pd.concat([eventInfo_pro, eventInfo.iloc[[index]], eventInfo.iloc[[index + 1]]])
            index = index + 2
        else:
            index = index + 1
    eventInfo = eventInfo_pro
    # eventInfo.to_csv('./eventInfo.csv')

    durationInfo = data[DURATION_COLUMN]
    durationInfo = durationInfo.dropna(axis=0, how='all')
    if LTE_CONFIGURATION_TIME in durationInfo.columns.values.tolist():
        durationInfo[LTE_CONFIGURATION_TIME] = durationInfo[LTE_CONFIGURATION_TIME] / 1000
    # durationInfo.to_csv('./duration.csv')

    return connection_type, signalInfo, eventInfo, durationInfo

def event_dur_each(dataframe, tag):
    df_event_duration = pd.DataFrame(
        columns=['index', 'Type', 'Radio Time', '4G Configuration Duration', '5G Configuration Duration', 'oldPCI',
                 'newPCI'], index=[tag])

    duration = dataframe.iloc[1:, -DURATION_LEN:]
    for col_index in range(DURATION_LEN):
        dataframe_notnan = duration[~np.isnan(duration.iloc[:, col_index])].iloc[:, col_index].values
        if dataframe_notnan.size > 0:
            duration.iloc[:, col_index].fillna(dataframe_notnan[0], inplace=True)
    duration = duration.iloc[0]
    event = dataframe.iloc[0]

    if event[NR_EVENT] == SA_ATTEMPT:
        df_event_duration['Type'] = '5GSA_5GSA'
        df_event_duration['5G Configuration Duration'] = duration[NR_SA_TIME_NR2NR]
    elif event[LTE_EVENT] != 'None' and event[NR_EVENT] == 'None' and event[NR_CHANGE_TYPE] == 'None' and event[
        NR_4GPCELL_CHANGE_TYPE] == 'None':
        if event[LTE_OLD_PCI] != event[LTE_NEW_PCI]:
            df_event_duration['Type'] = '4G_4G'
            df_event_duration['5G Configuration Duration'] = duration[NR_NSA_CONFIGURATION_TIME_LTE2NR] if ~np.isnan(
                duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) else duration[NR_NSA_CONFIGURATION_TIME_NR2NR]
        else:
            df_event_duration['Type'] = '5GNSA_4G'
            df_event_duration['5G Configuration Duration'] = duration[NR_NSA_CONFIGURATION_TIME_LTE2NR] if ~np.isnan(
                duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) else duration[NR_NSA_CONFIGURATION_TIME_NR2NR]
    elif event[LTE_EVENT] == 'None' and event[NR_EVENT] != 'None' and ~np.isnan(
            duration[NR_NSA_CONFIGURATION_TIME_NR2NR]) and np.isnan(duration[LTE_CONFIGURATION_TIME]):
        df_event_duration['Type'] = '5GNSA_5GChange'
        df_event_duration['5G Configuration Duration'] = duration[NR_NSA_CONFIGURATION_TIME_LTE2NR] if ~np.isnan(
            duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) else duration[NR_NSA_CONFIGURATION_TIME_NR2NR]
    elif event[LTE_EVENT] != 'None' and event[NR_EVENT] != 'None':
        if ~np.isnan(duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) and np.isnan(
                duration[NR_NSA_CONFIGURATION_TIME_NR2NR]):
            df_event_duration['Type'] = '4G_5GNSA'
            df_event_duration['5G Configuration Duration'] = duration[NR_NSA_CONFIGURATION_TIME_LTE2NR] if ~np.isnan(
                duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) else duration[NR_NSA_CONFIGURATION_TIME_NR2NR]
        elif np.isnan(duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) and ~np.isnan(
                duration[NR_NSA_CONFIGURATION_TIME_NR2NR]) and event[LTE_OLD_PCI] != event[LTE_NEW_PCI]:
            if event[LTE_OLD_PCI] != event[LTE_NEW_PCI]:
                df_event_duration['Type'] = '5GNSA_4G/4G5GChange'
                df_event_duration['5G Configuration Duration'] = duration[
                    NR_NSA_CONFIGURATION_TIME_LTE2NR] if ~np.isnan(duration[NR_NSA_CONFIGURATION_TIME_LTE2NR]) else \
                duration[NR_NSA_CONFIGURATION_TIME_NR2NR]

    df_event_duration['index'] = event['index']
    df_event_duration['Radio Time'] = duration[LTE_RADIO_TIME] if ~np.isnan(duration[LTE_RADIO_TIME]) else duration[
        NR_RADIO_TIME]
    df_event_duration['4G Configuration Duration'] = duration[LTE_CONFIGURATION_TIME]
    df_event_duration['newPCI'] = event[LTE_NEW_PCI]
    df_event_duration['oldPCI'] = event[LTE_OLD_PCI]

    return df_event_duration
def event_duration_filter(eventInfo, durationInfo):
    # =====================================================================================
    # process event-duration data
    event_duration_info = pd.concat([eventInfo, durationInfo], axis=1).sort_index(ascending=True)
    event_duration_info.reset_index(inplace=True)
    # event_duration_info.to_csv('./event_duration.csv')

    df_event_duration = pd.DataFrame()

    for idk in range(2, len(eventInfo), 2):
        pre = eventInfo.iloc[idk - 2].name
        next = eventInfo.iloc[idk].name

        index_pre = event_duration_info[event_duration_info['index'] == pre].index.values[0]
        index_next = event_duration_info[event_duration_info['index'] == next].index.values[0]
        cut_pd = event_duration_info.iloc[index_pre:index_next]
        df = event_dur_each(cut_pd, int(idk / 2 - 1))
        df_event_duration = pd.concat([df_event_duration, df], axis=0)

    df_event_duration.sort_values("index", inplace=True)
    # df_event_duration.to_csv('./df_event_duration.csv')
    return df_event_duration

def techIndentify(row):
    if row[LTE_PCI] != "None" or row[LTE_BAND] != 'None':
        if row[NR_PCI] == "None" and row[NR_BAND] == 'None':
            type = '4G'
        else:
            type = '5GNSA'
    elif row[LTE_PCI] == "None" and row[LTE_BAND] == 'None' and (row[NR_PCI] != "None" or row[NR_BAND] != 'None'):
        type = '5GSA'
    return type
def handoverList_filter(signalInfo):
    handover_list = []
    for index in range(len(signalInfo)):
        row = signalInfo.iloc[index - 1]
        next = signalInfo.iloc[index]
        handoverType = ''
        if techIndentify(row) == '4G':
            if techIndentify(next) == '4G' and (row[LTE_PCI] != next[LTE_PCI] or row[LTE_BAND] != next[LTE_BAND]):
                handoverType = "4G_4G"
            elif techIndentify(next) == '5GNSA':
                handoverType = "4G_5GNSA"
        elif techIndentify(row) == '5GSA':
            if techIndentify(next) == '5GSA' and (row[NR_PCI] != next[NR_PCI] or row[NR_BAND] != next[NR_BAND]):
                handoverType = "5GSA_5GSA"
        elif techIndentify(row) == '5GNSA':
            if techIndentify(next) == '4G':
                handoverType = "5GNSA_4G"
            elif techIndentify(next) == '5GNSA':
                if row[LTE_PCI] == next[LTE_PCI] and (row[NR_PCI] != next[NR_PCI] or row[NR_BAND] != next[NR_BAND]):
                    handoverType = "5GNSA_5GChange"
                elif row[NR_PCI] == next[NR_PCI] and (row[LTE_PCI] != next[LTE_PCI] or row[LTE_BAND] != next[LTE_BAND]):
                    handoverType = "5GNSA_4GChange"
                elif (row[NR_PCI] != next[NR_PCI] or row[NR_BAND] != next[NR_BAND]) and (
                        row[LTE_PCI] != next[LTE_PCI] or row[LTE_BAND] != next[LTE_BAND]):
                    handoverType = "5GNSA_4G5GChange"
        if handoverType != "":
            handover_list.append((row.name + 2, handoverType, row[LTE_PCI], next[LTE_PCI]))

    handover_list = pd.DataFrame(handover_list)
    handover_list.columns = ['index', 'handoverType', 'lte_OldPCI', 'lte_NewPCI']
    handover_list.sort_values("index", inplace=True)
    # handover_list.to_csv('./handover_list.csv')
    return handover_list
def compare2pd(event_duration, handover):
    if np.abs(event_duration['index'] - handover['index']) < 10:
        if event_duration['Type'] == handover['handoverType']:
            return True
        elif event_duration['Type'] == '5GNSA_4G/4G5GChange' and (
                handover['handoverType'] == '5GNSA_4GChange' or handover['handoverType'] == '5GNSA_4G5GChange') and (
                event_duration['newPCI'] == handover['lte_NewPCI']) and (
                event_duration['oldPCI'] == handover['lte_OldPCI']):
            return True
    return False
def mergeList(df_event_duration,handover_list):
    videoType_Table = []
    i = 0
    j = 0
    while i < len(handover_list) and j < len(df_event_duration):
        event_duration = df_event_duration.iloc[j]
        handover = handover_list.iloc[i]
        if compare2pd(event_duration, handover):
            handover_type = handover['handoverType']
            radio_time = event_duration['Radio Time']
            lte_time = event_duration['4G Configuration Duration']
            nr_time = event_duration['5G Configuration Duration']
            videoType_Table.append([handover_type, radio_time, lte_time, nr_time])
            i = i + 1
            j = j + 1
        elif event_duration['index'] > handover['index']:
            while event_duration['index'] > handover['index']:
                i = i + 1
                event_duration = df_event_duration.iloc[j]
                handover = handover_list.iloc[i]
                if compare2pd(event_duration, handover):
                    break
        elif event_duration['index'] <= handover['index']:
            while event_duration['index'] <= handover['index']:
                j = j + 1
                event_duration = df_event_duration.iloc[j]
                handover = handover_list.iloc[i]
                if compare2pd(event_duration, handover):
                    break
        else:
            i = i + 1
            j = j + 1

    videoType_Table = pd.DataFrame(videoType_Table, columns=TABLE_COLUMN)

    return videoType_Table
def generateTable(datapath,tablepath):
    data = pd.read_csv(datapath,low_memory=False)

    connection_type, signalInfo, eventInfo, durationInfo=dataloader(data)
    print("Event Technology:", connection_type)
    event_duration_list=event_duration_filter(eventInfo, durationInfo)
    handover_list=handoverList_filter(signalInfo)
    videoType_Table=mergeList(event_duration_list,handover_list)
    videoType_Table.to_csv(tablepath)


if __name__ == '__main__':
    for file in os.listdir(path.join(DATA_DIR, "HandOver\\")):
        if file.endswith('.csv'):
            filename= file.split(".")[0]

            datapath = path.join(DATA_DIR, "HandOver\\" + filename +".csv")
            tablepath = path.join(TASK3_DIR, "Table\\" + filename + "-DurationTable.csv")

            print("*******************************************")
            print("Creating Table: ", filename)
            generateTable(datapath,tablepath)
