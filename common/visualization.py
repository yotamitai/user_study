from os.path import join, isdir

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

COLORS = {
    "Blue": '#2CBDFE',
    "Yellow": '#FFCC00',
    "Pink": '#F3A0F2',
    "Orange": '#FF8040',
    "Violet": '#661D98',
    "Amber": '#F5B14C',
    "Red": "#B90E0A",
    "Green": "#74B72E",
    "Gray": "#BEBEBE"
}
font = {'family': 'serif',
        'color': 'darkred',
        'weight': 'normal',
        'size': 16,
        }


def visualize_bar(labels, values, y_label, color='b', y_ticks=None, ci=None,
                  title=None, file_name=None, rotation=0, horizontal_line=False):
    x = np.arange(len(labels))
    plt.bar(x, values, edgecolor='black', yerr=ci, color=color)
    plt.ylabel(y_label, fontdict=font)
    plt.xticks(x, labels, rotation=rotation)
    if y_ticks: plt.yticks(y_ticks)
    if title: plt.title(title)
    plt.tick_params(axis='both', which='major', labelsize=14)
    if horizontal_line: plt.axhline(y=horizontal_line, color='b', linestyle='--')

    if file_name:
        plt.savefig(join('figures', file_name))
    plt.tight_layout()
    plt.show()


def visualize_and_save_bar(labels, lst1, lst2, y_label, colors, y_ticks, ci=[0, 0],
                           legend=None, title=None, file_name=None, width=0.35, rotation=0,
                           horizontal_line=False):
    x = np.arange(len(labels))
    p1 = plt.bar(x - width / 2, lst1, width, yerr=ci[0], color=COLORS[colors[0]])
    p2 = plt.bar(x + width / 2, lst2, width, yerr=ci[1], color=COLORS[colors[1]])
    plt.ylabel(y_label, fontdict=font)
    plt.xticks(x, labels, rotation=rotation)
    plt.yticks(y_ticks)
    if legend: plt.legend((p1[0], p2[0]), legend, fontsize=14)
    if title: plt.title(title)
    plt.tick_params(axis='both', which='major', labelsize=14)
    if horizontal_line: plt.axhline(y=horizontal_line, color='b', linestyle='--')

    if file_name:
        file_name = join('figures', file_name)
        if not (isdir(file_name)):
            os.makedirs(file_name)
            os.rmdir(file_name)
        plt.savefig(file_name)
    plt.tight_layout()
    plt.show()


def visualize_and_save_3bar(labels, lst1, lst2, lst3, y_label, title, colors, y_ticks,
                            ci=[0, 0, 0],
                            legend=None, file_name=None, width=0.35, rotation=0):
    x = np.arange(len(labels))
    p1 = plt.bar(x - width, lst1, width, yerr=ci[0], color=COLORS[colors[0]])
    p2 = plt.bar(x + width, lst2, width, yerr=ci[1], color=COLORS[colors[1]])
    p3 = plt.bar(x, lst3, width, yerr=ci[2], color=COLORS[colors[2]])
    plt.ylabel(y_label, fontdict=font)
    # plt.legend((p1, p2), ("chose left agent", "chose right agent"), title=title)
    plt.xticks(x, labels, rotation=rotation)
    plt.yticks(y_ticks)
    if legend: plt.legend((p1[0], p2[0], p3[0]), legend, fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)

    if file_name:
        file_name = join('figures', file_name)
        if not (isdir(file_name)):
            os.makedirs(file_name)
            os.rmdir(file_name)
        plt.savefig(file_name)
    plt.tight_layout()
    plt.show()


def visualize_and_save_confidence(labels, lst1, y_label, colors, y_ticks,
                                  legend=None, title=None, file_name=None, width=0.35):
    black_diamond = dict(markerfacecolor='k', marker='D')
    x = np.arange(1, len(labels) + 1)
    p1 = plt.boxplot(lst1, flierprops=black_diamond, patch_artist=True, widths=0.35, )
    plt.ylabel(y_label, fontdict=font)
    plt.xticks(x, labels)
    plt.yticks(np.arange(7))
    for i in range(len(labels)):
        p1['boxes'][i].set_facecolor(COLORS[colors[i % 2]])
    for i in range(1, (len(labels) // 2)):
        plt.axvline(x=0.5 + 2 * i, color='k', linestyle='--')
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.grid()
    if title: plt.title(title)

    if file_name:
        file_name = join('figures', file_name)
        if not (isdir(file_name)):
            os.makedirs(file_name)
            os.rmdir(file_name)
        plt.savefig(file_name)
    plt.tight_layout()
    plt.show()


def visualize_confidence(labels, lst, y_label, colors):
    black_diamond = dict(markerfacecolor='k', marker='D')
    p1 = plt.boxplot(lst, flierprops=black_diamond, patch_artist=True, widths=0.35)
    plt.ylabel(y_label, fontdict=font)
    plt.xticks([1, 2, 3, 4, 5, 6], labels)
    plt.yticks(np.arange(8))
    for i in range(len(labels)):
        p1['boxes'][i].set_facecolor(COLORS[colors[i % 2]])
    for i in range(1, (len(labels) // 2)):
        plt.axvline(x=0.5 + 2 * i, color='k', linestyle='--')
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.grid()

    plt.show()


def visualize_and_save_satisfaction(labels, lst1, y_label, colors, y_ticks,
                                    legend=None, title=None, file_name=None, width=0.35):
    black_diamond = dict(markerfacecolor='k', marker='D')
    x = np.arange(1, len(labels) + 1)
    p1 = plt.boxplot(lst1, flierprops=black_diamond, patch_artist=True, widths=0.35, )
    plt.ylabel(y_label, fontdict=font)
    plt.xticks(x, labels)
    plt.yticks(np.arange(7))
    for i in range(len(labels)):
        p1['boxes'][i].set_facecolor(COLORS[colors[i % 2]])
    for i in range(1, (len(labels) // 2)):
        plt.axvline(x=0.5 + 2 * i, color='k', linestyle='--')
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.grid()
    if title: plt.title(title)

    if file_name:
        file_name = join('figures', file_name)
        if not (isdir(file_name)):
            os.makedirs(file_name)
            os.rmdir(file_name)
        plt.savefig(file_name)
    plt.tight_layout()
    plt.show()
