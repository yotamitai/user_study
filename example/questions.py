answer_dict = {
    "M2Q q1": '1',
    "M2Q q2": '3',
    "T2Q q1": '4',
    "T2Q q2": '2',
    "Q2T q1": '2',
    "Q2T q2": '4',
}

effectiveness_questions = {
    "effectiveness_1": 1,
    "effectiveness_2": 1,
    "effectiveness_3": 1,
    "effectiveness_4": 1
}
effectiveness_labels = [
    "Worked\nwell",
    "videos from\nSpecification",
    "Videos\nhelpful",
    "Easy to\nspecify\nbehavior",
]

efficiency_questions = {
    "efficiency_1": 1,
    "efficiency_2": 0,
    "efficiency_3": 0,
    "efficiency_4": 1,
    "efficiency_5": 0
}
efficiency_labels = [
    "Ease\nof use",
    "Unnecessarily\ncomplex",
    "Requires\ntechnical skill",
    "Fast to\nlearn",
    "Much\noverhead",
]

satisfaction_questions = {
    "satisfaction_1": 0,
    "satisfaction_2": 1
}
satisfaction_labels = [
    "Inconvenient",
    "Confidence\nusing",
]

questions_dict = {
    "effectiveness": effectiveness_questions,
    "efficiency": efficiency_questions,
    "satisfaction": satisfaction_questions,
}

labels_dict = {
    "effectiveness": effectiveness_labels,
    "efficiency": efficiency_labels,
    "satisfaction": satisfaction_labels,
}

textual_questions = ["convenient system", "clear movies", "Q253", "feedback expressive",
                     "add dropdowns", "Q252", "feedback improvment", "comments"]