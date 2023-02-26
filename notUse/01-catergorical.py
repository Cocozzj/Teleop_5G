import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fullDataset = pd.read_csv('../Data/full-dataset.csv')

# =====================================================================================
smallCell1PCILabel = '5G KPI SCell[1] RF Serving PCI'
smallCell2PCILabel = '5G KPI SCell[2] RF Serving PCI'
mcsULLabel = '5G KPI PCell Layer1 UL MCS (Avg)'
mcsDLLabel = '5G KPI PCell Layer1 DL MCS (Avg)'
rbDLLabel = '5G KPI PCell Layer1 DL RB Num (Including 0)'
rbULLabel = '5G KPI PCell Layer1 UL RB Num (Including 0)'
radioRelationshipULLabel = '5G KPI PCell Layer1 UL MIMO'
radioRelationshipDLLabel = '5G KPI PCell Layer1 DL MIMO'
carrierLabel = 'Smart Phone Android System Info Operator'
bandLabel = '5G KPI PCell RF Band'
technologyLabel = 'Event Technology'
abstractTechLabel = 'Abstract-Tech-Label'
tputUpLabel = 'Total UL Tput (Mbps)'
tputDlLabel = 'Total DL Tput (Mbps)'
signalLabels = ['5G KPI PCell RF Serving SS-RSRP [dBm]', '5G KPI PCell RF Serving SS-RSRQ [dB]', '5G KPI PCell RF Serving SS-SINR [dB]','5G KPI PCell RF CQI']
#fullDataset = fullDataset[fullDataset['5G Estimate'] == True]
print('Dataset Size {}'.format(len(fullDataset)))
bandsSeen = fullDataset[bandLabel].unique()
carriersSeen = fullDataset[carrierLabel].unique()
environmentsSeen = fullDataset['Environment'].unique()
radioRelationshipsSeen = list(fullDataset[radioRelationshipULLabel].unique())
radioRelationshipsSeen.extend(list(fullDataset[radioRelationshipDLLabel].unique()))
#technologiesSeen = fullDataset[technologyLabel].unique()[:-1]
technologiesSeen = fullDataset[fullDataset[abstractTechLabel].notna()]
technologiesSeen = technologiesSeen[abstractTechLabel].unique()
uploadDataSet = fullDataset[fullDataset['Direction'] == 'UP']
uploadDataSet = uploadDataSet[uploadDataSet[abstractTechLabel] != 'NO SERVICE']
downloadDataSet = fullDataset[fullDataset['Direction'] == 'DL']
# ======================================================================================

# Graph tpu, direction
boxplot = uploadDataSet.boxplot(column=[tputUpLabel], by=[abstractTechLabel], showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Deployment Type')
plt.suptitle('')
plt.title('Upload Speeds')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-UL-general.png')
plt.close()

boxplot = downloadDataSet.boxplot(column=[tputDlLabel], by=[abstractTechLabel], showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Deployment Type')
plt.suptitle('')
plt.title('Download Speeds')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-DL-general.png')
plt.close()


# ======================================================================================

# Graph Tput, Direction, Band
boxplot = uploadDataSet.boxplot(column=[tputUpLabel],by=[bandLabel], showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band')
plt.suptitle('')
plt.title('Upload Speed By Band')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-UL-band.png')
plt.close()

boxplot = downloadDataSet.boxplot(column=[tputDlLabel],by=[bandLabel], showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band')
plt.suptitle('')
plt.title('Download Speed By Band')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-DL-band.png')
plt.close()

# ======================================================================================

# Graph MCS by direction
boxplot = uploadDataSet.boxplot(column=[mcsULLabel],by=[bandLabel], showfliers=False)
boxplot.set_ylabel('MCS')
boxplot.set_xlabel('Band')
plt.suptitle('')
plt.title('MCS By Band')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-UL-band-MCS.png')
plt.close()

boxplot = downloadDataSet.boxplot(column=[mcsDLLabel],by=[bandLabel], showfliers=False)
boxplot.set_ylabel('MCS')
boxplot.set_xlabel('Band')
plt.suptitle('')
plt.title('MCS By Band')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-DL-band-MCS.png')
plt.close()

# ======================================================================================

# Graph Secondary Cells by direction and band
boxplot = uploadDataSet.boxplot(column=[rbULLabel],by=[bandLabel], showfliers=False)
boxplot.set_ylabel('RB')
boxplot.set_xlabel('Band')
plt.suptitle('')
plt.title('RB By Band')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-UL-band-rb.png')
plt.close()

boxplot = downloadDataSet.boxplot(column=[rbDLLabel],by=[bandLabel], showfliers=False)
boxplot.set_ylabel('RB')
boxplot.set_xlabel('Band')
plt.suptitle('')
plt.title('RB By Band')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-DL-band-rb.png')
plt.close()

# =======================================================================================

# Graph Tput, Direction, Carrier, Band
boxplot = uploadDataSet.boxplot(column=[tputUpLabel],by=[bandLabel,carrierLabel], figsize=(12,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Carrier')
plt.suptitle('')
plt.title('Upload Speed By Band & Carrier')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-UL-band-carrier.png')
plt.close()

boxplot = downloadDataSet.boxplot(column=[tputDlLabel],by=[bandLabel,carrierLabel], figsize=(12,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Carrier')
plt.suptitle('')
plt.title('Download Speed By Band & Carrier')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-DL-band-carrier.png')
plt.close()

# =======================================================================================

# Graph Tput, Direction, Carrier, Band, technology
boxplot = uploadDataSet.boxplot(column=[tputUpLabel],by=[bandLabel,carrierLabel,technologyLabel], figsize=(90,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Carrier')
plt.suptitle('')
plt.title('Upload Speed By Band & Carrier & Technology')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-UL-band-carrier-tech.png')
plt.close()

boxplot = downloadDataSet.boxplot(column=[tputDlLabel],by=[bandLabel,carrierLabel,technologyLabel], figsize=(90,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Carrier')
plt.suptitle('')
plt.title('Download Speed By Band & Carrier & Technology')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-DL-band-carrier-tech.png')
plt.close()

# ========================================================================================

# Graph Tput, Direction, Carrier, Band, Environment
boxplot = uploadDataSet.boxplot(column=[tputUpLabel],by=[bandLabel,'Environment',carrierLabel], figsize=(60,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Carrier')
plt.suptitle('')
plt.title('Upload Speed By Band, Carrier, Environment')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-UL-band-carrier-env.png')
plt.close()

boxplot = downloadDataSet.boxplot(column=[tputDlLabel],by=[bandLabel,'Environment',carrierLabel], figsize=(60,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Carrier')
plt.suptitle('')
plt.title('Download Speed By Band, Carrier, Environment')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-DL-band-carrier-env.png')
plt.close()

# =========================================================================================

# Graph Tput, Direction, Band, Environment
boxplot = uploadDataSet.boxplot(column=[tputUpLabel],by=[bandLabel,'Environment'], figsize=(26,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Carrier')
plt.suptitle('')
plt.title('Upload Speed By Band, Environment')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-UL-band-env.png')
plt.close()

boxplot = downloadDataSet.boxplot(column=[tputDlLabel],by=[bandLabel,'Environment'], figsize=(26,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Carrier')
plt.suptitle('')
plt.title('Download Speed By Band, Environment')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-DL-band-env.png')
plt.close()

# =======================================================================================

# Graph Tput, Direction, Carrier, Band
boxplot = uploadDataSet.boxplot(column=[tputUpLabel],by=[bandLabel,radioRelationshipULLabel], figsize=(28,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Antenna Technology')
plt.suptitle('')
plt.title('Upload Speed By Band & Antenna Technology')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-UL-band-ant-tech.png')
plt.close()

boxplot = downloadDataSet.boxplot(column=[tputDlLabel],by=[bandLabel,radioRelationshipDLLabel], figsize=(28,6), showfliers=False)
boxplot.set_ylabel('Speed (Mbps)')
boxplot.set_xlabel('Band & Antenna Technology')
plt.suptitle('')
plt.title('Download Speed By Band & Antenna Technology')
plt.tight_layout()
plt.savefig('../Data/data-analysis/boxplot-DL-band-ant-tech.png')
plt.close()



# ========================================================================================

for signal in signalLabels:
    # Graph Signal, Direction, Band

    boxplot = uploadDataSet.boxplot(column=[signal], by=[bandLabel], figsize=(16, 6),
                                  showfliers=False)
    boxplot.set_ylabel('{}'.format(signal))
    boxplot.set_xlabel('Band')
    plt.suptitle('')
    plt.title('{} By Band'.format(signal))
    plt.tight_layout()
    plt.savefig('./data-analysis/boxplot-UL-band-{}.png'.format(signal))
    plt.close()

    boxplot = downloadDataSet.boxplot(column=[signal], by=[bandLabel], figsize=(16, 6),
                                  showfliers=False)
    boxplot.set_ylabel('{}'.format(signal))
    boxplot.set_xlabel('Band')
    plt.suptitle('')
    plt.title('{} By Band'.format(signal))
    plt.tight_layout()
    plt.savefig('./data-analysis/boxplot-DL-band-{}.png'.format(signal))
    plt.close()

    # =====================================================================================

    # Graph Signal, Direction, Band, Carrier
    boxplot = uploadDataSet.boxplot(column=[signal], by=[bandLabel,carrierLabel], figsize=(16, 6),
                                  showfliers=False)
    boxplot.set_ylabel('{}'.format(signal))
    boxplot.set_xlabel('Band & Carrier')
    plt.suptitle('')
    plt.title('{} By Band & Carrier'.format(signal))
    plt.tight_layout()
    plt.savefig('./data-analysis/boxplot-UL-band-carrier-{}.png'.format(signal))
    plt.close()

    boxplot = downloadDataSet.boxplot(column=[signal], by=[bandLabel, carrierLabel], figsize=(16, 6),
                                  showfliers=False)
    boxplot.set_ylabel('{}'.format(signal))
    boxplot.set_xlabel('Band & Carrier')
    plt.suptitle('')
    plt.title('{} By Band & Carrier'.format(signal))
    plt.tight_layout()
    plt.savefig('./data-analysis/boxplot-DL-band-carrier-{}.png'.format(signal))
    plt.close()



    # ======================================================================================

    # Graph Signal, Direction, Band, Enivronment
    boxplot = uploadDataSet.boxplot(column=[signal], by=[bandLabel,'Environment'], figsize=(22, 6),
                                  showfliers=False)
    boxplot.set_ylabel('{}'.format(signal))
    boxplot.set_xlabel('Band & Environment')
    plt.suptitle('')
    plt.title('{} By Band & Environment'.format(signal))
    plt.tight_layout()
    plt.savefig('./data-analysis/boxplot-UL-band-env-{}.png'.format(signal))
    plt.close()

    boxplot = downloadDataSet.boxplot(column=[signal], by=[bandLabel,'Environment'], figsize=(22, 6),
                                  showfliers=False)
    boxplot.set_ylabel('{}'.format(signal))
    boxplot.set_xlabel('Band & Environment')
    plt.suptitle('')
    plt.title('{} By Band & Environment'.format(signal))
    plt.tight_layout()
    plt.savefig('./data-analysis/boxplot-DL-band-env-{}.png'.format(signal))
    plt.close()

# ================================================================================

# Graph the pie chart for band occurrences overall
topLevelBandDF = pd.DataFrame()

for band in bandsSeen:

    bandDF = fullDataset[fullDataset[bandLabel] == band]
    bandUlDF = bandDF[bandDF['Direction'] == 'UP']
    bandDlDF = bandDF[bandDF['Direction'] == 'DL']

    topLevelRow = pd.DataFrame()

    topLevelRow['Band'] = [band]
    topLevelRow['UL Count'] = [len(bandUlDF)]
    topLevelRow['DL Count'] = [len(bandDlDF)]

    topLevelBandDF = topLevelBandDF.append(topLevelRow)

topLevelBandDF = topLevelBandDF.set_index('Band')
plotAx = topLevelBandDF.plot.pie(y='UL Count', autopct='%1.1f%%', figsize=(5, 5),
                                 title='Band Occurrence (Upload)')
plt.savefig('./data-analysis/band-occurrence-UL-pie-chart.jpg')
plt.close()
print('UL Band Count Total {}'.format(topLevelBandDF['UL Count'].sum()))

plotAx = topLevelBandDF.plot.pie(y='DL Count', autopct='%1.1f%%', figsize=(5, 5),
                                 title='Band Occurrence (Download)')
plt.savefig('./data-analysis/band-occurrence-DL-pie-chart.jpg')
plt.close()
print('DL Band Count Total {}'.format(topLevelBandDF['DL Count'].sum()))

# ===============================================================================

# Graph the carrier breakdowns
for carrier in carriersSeen:

    carrierLevelDF = pd.DataFrame()

    for band in bandsSeen:
        bandDF = fullDataset[(fullDataset[bandLabel] == band) & (fullDataset[carrierLabel] == carrier)]
        bandUlDF = bandDF[bandDF['Direction'] == 'UP']
        bandDlDF = bandDF[bandDF['Direction'] == 'DL']

        carrierLevelRow = pd.DataFrame()

        carrierLevelRow['Band'] = [band]
        carrierLevelRow['UL Count'] = [len(bandUlDF)]
        carrierLevelRow['DL Count'] = [len(bandDlDF)]

        carrierLevelDF = carrierLevelDF.append(carrierLevelRow)

    carrierLevelDF = carrierLevelDF.set_index('Band')

    if carrierLevelDF['UL Count'].sum() > 0:

        plotAx = carrierLevelDF.plot.pie(y='UL Count', autopct='%1.1f%%', figsize=(5, 5),
                                         title='{} Band Occurrence (Upload)'.format(carrier))
        plt.savefig('./data-analysis/band-occurrence-{}-UL-pie-chart.jpg'.format(carrier))
        plt.close()
        print('{} UL Band Count Total {}'.format(carrier,carrierLevelDF['UL Count'].sum()))
    else:
        print('{} UL Band Count Total {}'.format(carrier, carrierLevelDF['UL Count'].sum()))

    if carrierLevelDF['DL Count'].sum() > 0:
        plotAx = carrierLevelDF.plot.pie(y='DL Count', autopct='%1.1f%%', figsize=(5, 5),
                                         title='{} Band Occurrence (Download)'.format(carrier))
        plt.savefig('./data-analysis/band-occurrence-{}-DL-pie-chart.jpg'.format(carrier))
        plt.close()
        print('{} DL Band Count Total {}'.format(carrier, carrierLevelDF['DL Count'].sum()))
    else:
        print('{} DL Band Count Total {}'.format(carrier, carrierLevelDF['DL Count'].sum()))

# ===============================================================================

# Graph Carrier by environment

for carrier in carriersSeen:

    for env in environmentsSeen:

        envLevelDF = pd.DataFrame()

        for band in bandsSeen:
            bandDF = fullDataset[(fullDataset[bandLabel] == band) & (fullDataset[carrierLabel] == carrier) & (fullDataset['Environment'] == env)]
            bandUlDF = bandDF[bandDF['Direction'] == 'UP']
            bandDlDF = bandDF[bandDF['Direction'] == 'DL']

            carrierLevelRow = pd.DataFrame()

            carrierLevelRow['Band'] = [band]
            carrierLevelRow['UL Count'] = [len(bandUlDF)]
            carrierLevelRow['DL Count'] = [len(bandDlDF)]

            envLevelDF = envLevelDF.append(carrierLevelRow)

        envLevelDF = envLevelDF.set_index('Band')
        if envLevelDF['UL Count'].sum() > 0:
            plotAx = envLevelDF.plot.pie(y='UL Count', autopct='%1.1f%%', figsize=(5, 5),
                                         title='{} {} Band Occurrence (Upload)'.format(env, carrier))
            plt.savefig('./data-analysis/band-occurrence-{}-{}-UL-pie-chart.jpg'.format(env, carrier))
            plt.close()
            print('{} {} UL Band Count Total {}'.format(env, carrier, envLevelDF['UL Count'].sum()))
        else:
            print('{} {} UL Band Count Total {}'.format(env, carrier, envLevelDF['UL Count'].sum()))

        if envLevelDF['DL Count'].sum() > 0:
            plotAx = envLevelDF.plot.pie(y='DL Count', autopct='%1.1f%%', figsize=(5, 5),
                                             title='{} {} Band Occurrence (Download)'.format(env, carrier))
            plt.savefig('./data-analysis/band-occurrence-{}-{}-DL-pie-chart.jpg'.format(env, carrier))
            plt.close()
            print('{} {} DL Band Count Total {}'.format(env, carrier, envLevelDF['DL Count'].sum()))
        else:
            print('{} {} DL Band Count Total {}'.format(env, carrier, envLevelDF['DL Count'].sum()))

# ================================================================================

# Graph pie plot for technology for carrier

for carrier in carriersSeen:

    carrierLevelDF = pd.DataFrame()

    for technology in technologiesSeen:
        bandDF = fullDataset[(fullDataset[abstractTechLabel] == technology) & (fullDataset[carrierLabel] == carrier)]
        bandUlDF = bandDF[bandDF['Direction'] == 'UP']
        bandDlDF = bandDF[bandDF['Direction'] == 'DL']

        carrierLevelRow = pd.DataFrame()

        carrierLevelRow['Tech'] = [technology]
        carrierLevelRow['UL Count'] = [len(bandUlDF)]
        carrierLevelRow['DL Count'] = [len(bandDlDF)]

        carrierLevelDF = carrierLevelDF.append(carrierLevelRow)

    carrierLevelDF = carrierLevelDF.set_index('Tech')

    if carrierLevelDF['UL Count'].sum() > 0:

        plotAx = carrierLevelDF.plot.pie(y='UL Count', autopct='%1.1f%%', figsize=(5, 5),
                                         title='{} Technology Occurrence (Upload)'.format(carrier))
        plt.savefig('./data-analysis/tech-occurrence-{}-UL-pie-chart.jpg'.format(carrier))
        plt.close()
        print('{} UL Tech Count Total {}'.format(carrier,carrierLevelDF['UL Count'].sum()))
    else:
        print('{} UL Tech Count Total {}'.format(carrier, carrierLevelDF['UL Count'].sum()))

    if carrierLevelDF['DL Count'].sum() > 0:
        plotAx = carrierLevelDF.plot.pie(y='DL Count', autopct='%1.1f%%', figsize=(5, 5),
                                         title='{} Tech Occurrence (Download)'.format(carrier))
        plt.savefig('./data-analysis/Tech-occurrence-{}-DL-pie-chart.jpg'.format(carrier))
        plt.close()
        print('{} DL Tech Count Total {}'.format(carrier, carrierLevelDF['DL Count'].sum()))
    else:
        print('{} DL Tech Count Total {}'.format(carrier, carrierLevelDF['DL Count'].sum()))

# ================================================================================

# Graph pie plot for technology by environment

for carrier in carriersSeen:

    for env in environmentsSeen:

        envLevelDF = pd.DataFrame()

        for technology in technologiesSeen:
            bandDF = fullDataset[(fullDataset[abstractTechLabel] == technology) & (fullDataset[carrierLabel] == carrier) & (fullDataset['Environment'] == env)]
            bandUlDF = bandDF[bandDF['Direction'] == 'UP']
            bandDlDF = bandDF[bandDF['Direction'] == 'DL']

            carrierLevelRow = pd.DataFrame()

            carrierLevelRow['Tech'] = [technology]
            carrierLevelRow['UL Count'] = [len(bandUlDF)]
            carrierLevelRow['DL Count'] = [len(bandDlDF)]

            envLevelDF = envLevelDF.append(carrierLevelRow)

        envLevelDF = envLevelDF.set_index('Tech')
        if envLevelDF['UL Count'].sum() > 0:
            plotAx = envLevelDF.plot.pie(y='UL Count', autopct='%1.1f%%', figsize=(5, 5),
                                         title='{} {} Tech Occurrence (Upload)'.format(env, carrier))
            plt.savefig('./data-analysis/tech-occurrence-{}-{}-UL-pie-chart.jpg'.format(env, carrier))
            plt.close()
            print('{} {} UL Tech Count Total {}'.format(env, carrier, envLevelDF['UL Count'].sum()))
        else:
            print('{} {} UL Tech Count Total {}'.format(env, carrier, envLevelDF['UL Count'].sum()))

        if envLevelDF['DL Count'].sum() > 0:
            plotAx = envLevelDF.plot.pie(y='DL Count', autopct='%1.1f%%', figsize=(5, 5),
                                             title='{} {} Tech Occurrence (Download)'.format(env, carrier))
            plt.savefig('./data-analysis/tech-occurrence-{}-{}-DL-pie-chart.jpg'.format(env, carrier))
            plt.close()
            print('{} {} DL Tech Count Total {}'.format(env, carrier, envLevelDF['DL Count'].sum()))
        else:
            print('{} {} DL Tech Count Total {}'.format(env, carrier, envLevelDF['DL Count'].sum()))

# ================================================================================

# Graph pie plot for antenna by environment

for carrier in carriersSeen:

    for env in environmentsSeen:

        envLevelDF = pd.DataFrame()

        for antTech in radioRelationshipsSeen:

            subDF = fullDataset[(fullDataset[radioRelationshipULLabel] == antTech) & (fullDataset[carrierLabel] == carrier) & (fullDataset['Environment'] == env)]

            bandULDF = subDF[subDF['Direction'] == 'UP']
            bandDLDF = subDF[subDF['Direction'] == 'DL']

            carrierLevelRow = pd.DataFrame()

            carrierLevelRow['Tech'] = [antTech]
            carrierLevelRow['UL Count'] = [len(bandUlDF)]
            carrierLevelRow['DL Count'] = [len(bandDlDF)]

            envLevelDF = envLevelDF.append(carrierLevelRow)

        envLevelDF = envLevelDF.set_index('Tech')
        if envLevelDF['UL Count'].sum() > 0:
            plotAx = envLevelDF.plot.pie(y='UL Count', autopct='%1.1f%%', figsize=(5, 5),
                                         title='{} {} Ant Tech Occurrence (Upload)'.format(env, carrier))
            plt.savefig('./data-analysis/ant-tech-occurrence-{}-{}-UL-pie-chart.jpg'.format(env, carrier))
            plt.close()
            print('{} {} UL Tech Count Total {}'.format(env, carrier, envLevelDF['UL Count'].sum()))
        else:
            print('{} {} UL Tech Count Total {}'.format(env, carrier, envLevelDF['UL Count'].sum()))

        if envLevelDF['DL Count'].sum() > 0:
            plotAx = envLevelDF.plot.pie(y='DL Count', autopct='%1.1f%%', figsize=(5, 5),
                                             title='{} {} Ant Tech Occurrence (Download)'.format(env, carrier))
            plt.savefig('./data-analysis/ant-tech-occurrence-{}-{}-DL-pie-chart.jpg'.format(env, carrier))
            plt.close()
            print('{} {} DL Ant Tech Count Total {}'.format(env, carrier, envLevelDF['DL Count'].sum()))
        else:
            print('{} {} DL Ant Tech Count Total {}'.format(env, carrier, envLevelDF['DL Count'].sum()))

