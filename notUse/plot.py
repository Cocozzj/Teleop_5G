from notUse.utils import *
from utils.context import *
############### Config ####################
SHOW_PLOT_FLAG = False
print('Data: {}'.format(DATA_DIR))
print('Plot: {}'.format(PLOT_DIR))

plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

candidates = ['Habitus-ad', 'Habitus-Simple', 'Habitus-Full']

#### Plot graph
if True:  # to avoid execution of certain plots (helps a lot)
    plot_id = '005a'  # id should be script # + plot # e.g. 00a, 00b, ....
    plot_name = 'user-study'  # use descriptive names for plots
    plt.close('all')
    fig, ax = plt.subplots(figsize=(4.5, 3))
    fig.tight_layout()

    # load data
    df = pd.read_csv(os.path.join(SAVE_DIR, '005-user-study.csv'))

    data = []
    positions = []
    for c in candidates:
        data.append(list(df[c]))
        positions.append(1 * len(positions))

    width_box = 0.6
    whis = 1.5

    box1 = ax.boxplot([data[0]], positions=[positions[0]], showmeans=True, autorange=True, whis=whis,
                      showfliers=False, widths=width_box, patch_artist=True, zorder=4,
                      meanprops={"marker": "^", "markerfacecolor": colorlist20[6], "markeredgecolor": colorlist20[6],
                                 "markersize": 12})

    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box1[item], color=colorlist20[0], linewidth=2)
    plt.setp(box1['whiskers'], color=colorlist20[0], linewidth=2, linestyle='--')
    plt.setp(box1["boxes"], facecolor=colorlist20[1], linewidth=2)
    plt.setp(box1["medians"], color=colorlist20[10], linewidth=2)

    box2 = ax.boxplot([data[1]], positions=[positions[1]], showmeans=True, autorange=True, whis=whis,
                      showfliers=False, widths=width_box, patch_artist=True, zorder=4,
                      meanprops={"marker": "^", "markerfacecolor": colorlist20[6], "markeredgecolor": colorlist20[6],
                                 "markersize": 12})

    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box2[item], color=colorlist20[2], linewidth=2)
    plt.setp(box2['whiskers'], color=colorlist20[2], linewidth=2, linestyle='--')
    plt.setp(box2["boxes"], facecolor=colorlist20[3], linewidth=2)
    plt.setp(box2["medians"], color=colorlist20[10], linewidth=2)

    box3 = ax.boxplot([data[2]], positions=[positions[2]], showmeans=True, autorange=True, whis=whis,
                      showfliers=False, widths=width_box, patch_artist=True, zorder=4,
                      meanprops={"marker": "^", "markerfacecolor": colorlist20[6], "markeredgecolor": colorlist20[6],
                                 "markersize": 12})

    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box3[item], color=colorlist20[4], linewidth=2)
    plt.setp(box3['whiskers'], color=colorlist20[4], linewidth=2, linestyle='--')
    plt.setp(box3["boxes"], facecolor=colorlist20[5], linewidth=2)
    plt.setp(box3["medians"], color=colorlist20[10], linewidth=2)

    ax.set_ylabel('Subjective Rating', fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.set_xticks(positions)
    ax.set_xticklabels(['Habitus\n-ad', 'Habitus\n-Simple', 'Habitus\n-Full'], fontsize=25)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.grid(linestyle='--', axis='y')
    ax.legend([box1['medians'][0], box1['means'][0]],
              [r'Median', r'Mean'],
              loc='upper center', ncol=2, facecolor='#dddddd',
              columnspacing=0.75, handlelength=1.5, framealpha=.7, fontsize=25,
              borderpad=0.1, labelspacing=.25, handletextpad=.25, bbox_to_anchor=(0.5, 1.24))

    # always use this function to save the figures
    plot_handler(plt, plot_name, plot_id, PLOT_DIR, show_flag=SHOW_PLOT_FLAG, png_only=False, pad_inches=0.07)