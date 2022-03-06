from os.path import join
from statistics import mean, stdev

import pandas as pd
import scipy
import seaborn as sns
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

from common.logger import log


def filter_attention_and_duration(df, logger, duration_limit=None, attention_questions=[],
                                  attention_values=[]):
    count = df.shape[0]
    df['Duration'] = df['Duration (in seconds)'].astype(int)
    # df = df[df['Duration'] >= (mean(df['Duration']) - 1 * stdev(df['Duration']))]
    # df = df[df['Duration'] <= (mean(df['Duration']) + 1 * stdev(df['Duration']))]
    if duration_limit: df = df[df['Duration'] >= duration_limit]
    log(logger, f'# Samples filtered by duration: {count - df.shape[0]}')

    """attention filter"""
    if attention_questions:
        assert len(attention_questions) == len(attention_values), \
            'All attention questions must have answers.'

        count, new_df = df.shape[0], pd.DataFrame()
        for q, a in zip(attention_questions, attention_values):
            temp_df = df.dropna(subset=[q])
            temp_df_filtered = temp_df[temp_df[q] == a]
            new_df = pd.concat([new_df, temp_df_filtered])
        log(logger, f'# Samples filtered by attention: {count - new_df.shape[0]}')
    return df


def get_bonus(df, bonus, answers, logger, questions=(), addons=()):
    df['Bonus'] = 0
    if questions:
        for q in questions:
            for add in addons:
                question = ' '.join([q, add])
                df.loc[df[question] == answers[question], 'Bonus'] += bonus
    else:
        for q in answers:
            df.loc[df[q] == answers[q], 'Bonus'] += bonus
    log(logger, f'Bonus assigned to participants')


def get_bonus_csv(df, path, fields, logger, skip=False):
    bonus_df = df[fields]
    # bonus_df['Bonus'].replace(0, np.nan, inplace=True)
    # bonus_df.dropna(subset=['Bonus'], inplace=True)
    if skip:  # skip certain ids that already got bonus
        bonus_df = bonus_df[~bonus_df['prolific_id'].isin(skip)]
    bonus_df.to_csv(path, index=False)
    log(logger, f'Bonus CSV generated at: {path}')


def bootstrap_mean(x, B=100000, alpha=0.05, plot=False):
    """Bootstrap standard error and (1-alpha)*100% c.i. for the population mean

    Returns bootstrapped standard error and different types of confidence intervals"""

    # Deterministic things
    n = len(x)  # sample size

    # Generate boostrap distribution of sample mean
    xboot = boot_matrix(x, B=B)
    sampling_distribution = xboot.mean(axis=1)

    quantile_boot = np.percentile(sampling_distribution,
                                  q=(100 * alpha / 2, 100 * (1 - alpha / 2)))

    if plot:
        plt.hist(sampling_distribution, bins="fd")
    return quantile_boot


def boot_matrix(z, B):
    """Bootstrap sample

    Returns all bootstrap samples in a matrix"""

    n = len(z)  # sample size
    idz = np.random.randint(0, n, size=(B, n))  # indices to pick for all boostrap samples
    return z[idz]


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n - 1)
    return h


def get_confidence_intervals(arrays, confidence=0.95, rounding=None, percentage=False):
    results = []
    for a in arrays:
        x = mean_confidence_interval(a, confidence)
        if percentage: x = x * 100
        if rounding: x = round(x, rounding)
        results.append(x)
    return results


def get_textual_responses(df, column, question):
    path = join('text_responses', column + '.txt')
    with open(path, 'w') as f:
        f.write("QUESTION:\n")
        f.write(question)
        f.write("\nRESPONSES:\n")
        for name, response in zip(df['prolific_id'].tolist(), df[column].tolist()):
            f.write(f"({name}) {response}\n")


def get_demographics(df, columns, types, questions):
    path = 'demographics.txt'
    with open(path, 'w') as f:
        f.write("DEMOGRAPHICS:\n")
        for i in range(len(columns)):
            f.write(f"{questions[i]}\n\t")
            if isinstance(types[i], int):
                f.write(f"AVG: {df[columns[i]].astype(int).mean()}, "
                        f"STD: {df[columns[i]].astype(int).std()}\n")
            elif isinstance(types[i], list):
                counts = df[columns[i]].value_counts()
                indxes = df[columns[i]].value_counts().axes[0].astype(int).tolist()
                for j in range(len(counts)):
                    f.write(f"{types[i][indxes[j]]}: {counts[j]}\n\t")
            f.write("\n")
