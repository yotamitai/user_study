import argparse
from copy import deepcopy
from os.path import join

import numpy as np
import pandas as pd

from Agent_Interview.questions import answer_dict, questions_dict, labels_dict, textual_questions
from common.logger import setup_applevel_logger
from common.utils import filter_attention_and_duration, get_bonus_csv, get_bonus, \
    get_confidence_intervals, get_textual_responses, get_demographics
from common.visualization import visualize_bar


def success(df, questions, color, logger):
    success_rates, responses = [], []
    for q in questions:
        answers = np.where(df[q] == questions[q], 1, 0)
        responses.append(answers)
        success_rates.append((sum(answers) / df.shape[0]) * 100)

    ci = get_confidence_intervals(responses, confidence=0.95, rounding=True, percentage=True)

    visualize_bar(questions.keys(), success_rates, "Success Rate", color=color, ci=ci,
                  file_name="success rate", horizontal_line=50)


def usability(df, questions, labels, name, logger, color):
    responses, overall = [], []
    for q in questions:
        answers = np.array(df[q].astype(int)) if questions[q] else 7 - np.array(df[q].astype(int))
        responses.append(answers - 1)
        overall.append((sum(answers) / df.shape[0]))

    ci = get_confidence_intervals(responses, confidence=0.95, rounding=2)

    visualize_bar(labels, overall, f"{name} Rate", color=color, ci=ci,
                  file_name=name, rotation=295, y_ticks=(0, 1, 2, 3, 4, 5, 6))


def main(args):
    """Process Data"""
    """Qualtrics"""
    qualtrics_df = pd.read_csv(args.csv)
    df = deepcopy(qualtrics_df)
    df.drop(index=[0, 1], inplace=True)

    """Filter"""
    # df = filter_attention_and_duration(df, args.logger,
    #                                    attention_questions=args.attention_questions,
    #                                    attention_values=args.attention_values)
    # """bonus"""
    # get_bonus(df, args.bonus, args.correct_answers, args.logger)
    # get_bonus_csv(df, 'bonus.csv', args.bonus_fields, args.logger, skip=args.skip_bonus)
    #
    # """success"""
    # success(df, args.correct_answers, 'g', args.logger)
    #
    # """usability"""
    # for test, color in [["effectiveness", 'b'], ["efficiency", 'c'], ["satisfaction", 'r']]:
    #     usability(df, questions_dict[test], labels_dict[test], test, args.logger, color)
    #
    # """Textual Responses"""
    # for column in textual_questions:
    #     survey_question = qualtrics_df[column][0]
    #     get_textual_responses(df, column, survey_question)

    """demographics"""
    questions = [qualtrics_df[x[0]][0] for x in args.demographics]
    columns = [x[0] for x in args.demographics]
    types = [x[1] for x in args.demographics]
    get_demographics(df, columns, types, questions)


if __name__ == '__main__':
    args = argparse.ArgumentParser().parse_args()
    args.logger = setup_applevel_logger(file_name='logging.log')
    args.exp_name = 'Agent Interview'
    args.attention_questions = []
    args.attention_values = []
    args.bonus_fields = ['prolific_id', 'Bonus']
    # args.bonus_msg = f'Bonus for {args.exp_name} experiment, thank you for participating!'
    args.csv = 'data/prolific_pilot.csv'
    args.bonus = 0.1
    args.correct_answers = answer_dict
    args.skip_bonus = [
        "5e5b7d7b1977823677ebc5ae",
        "5f24348aaf4d9b0144933300",
        "5f07267fa81c732d460fc24e",
        "5d174a5cf0b3c1001a263bab",
        "5eac671f0658ac0ea6c730d2",
        "5bfd2d6b8acfed00011a5c89",
        "5dee32d84378274d09c2ed2d",
        "5f3ebe53b9a7b3150f539bde",
        "6147c5874b61952e42e9b2bd",
        "6102c8df44596782a4b121df",
    ]
    args.demographics = [
        ("Duration (in seconds)", 1),
        ("age", 1),
        ("gender", ["M", "F", "Prefer not to say", "Other"]),
        ("country", ["","US", "UK", "Other"]),
        ("education", ["","<8", "8-12", "BSc", "MSc", "Phd/MD", "Other"]),
        ("english", ["","Not", "2", "3", "so-so", "5", "6", "Superbly"]),
        ("tech-savvy", ["","Not", "2", "3", "so-so", "5", "6", "Superbly"]),
        ("ai", ["","never heard", "heard", "interested", "course", "work", "research"]),
    ]
    main(args)
