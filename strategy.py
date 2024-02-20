import pandas as pd
import matplotlib.pyplot as plt
import scenario

strategies_description = scenario.strategies_description
archetypes = scenario.archetypes
archetype_descriptions = scenario.archetype_descriptions

def get_strategy(results, chat_id, poll_number):
    ###########################################################################
    strategies = []
    df = pd.DataFrame(results, columns=['chat_id', 'user_id', 'poll_number', 'question_id', 'response', 'timestamp'])
    df = df[df['poll_number'] == poll_number]
    df = df[df['chat_id'] == (chat_id)]
    icon = df[df['question_id'] == 25][['response']].iloc[0,0]
    df = df[df['question_id'] != 25]
    strategies.append(df[df['question_id'].isin([1,4])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([2,5])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([3,6])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([7,10])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([8,11])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([9,12])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([13,16])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([14,17])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([15,18])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([19,22])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([20,23])][['response']].sum(axis=0)['response'])
    strategies.append(df[df['question_id'].isin([21,24])][['response']].sum(axis=0)['response'])

    if icon == 0:
        strategies[0] = strategies[0] + 4
    elif icon == 1:
        strategies[11] = strategies[11] + 4
    elif icon == 2:
        strategies[9] = strategies[9] + 4
    elif icon == 3:
        strategies[7] = strategies[7] + 4
    elif icon == 4:
        strategies[5] = strategies[5] + 4
    elif icon == 5:
        strategies[10] = strategies[10] + 4
    elif icon == 6:
        strategies[1] = strategies[1] + 4
    elif icon == 7:
        strategies[2] = strategies[2] + 4
    elif icon == 8:
        strategies[6] = strategies[6] + 4
    elif icon == 9:
        strategies[8] = strategies[8] + 4
    elif icon == 10:
        strategies[4] = strategies[4] + 4
    elif icon == 11:
        strategies[3] = strategies[3] + 4

    result = [strategies[0]+strategies[4]+strategies[10],
              strategies[2]+strategies[6]+strategies[9],
              strategies[1]+strategies[5]+strategies[11],
              strategies[3]+strategies[7]+strategies[8]
              ]
    max_str = 0
    for i in range(4):
        if max_str < result[i]:
            max_str = result[i]
    for i in range(4):
        if result[i] == max_str:
            return strategies_description[i], strategies

def get_archetype(strategies):
    # Вот здесь сделаем датафрейм для визуализации:
    archetypes_df = pd.DataFrame(data={'archetypes':archetypes, 'values':strategies})
    archetypes_df = archetypes_df.sort_values(by='values', ascending=False)#[:3]
    fig, ax = plt.subplots()
    ax.pie(archetypes_df['values'], labels=archetypes_df['archetypes'], autopct='%1.1f%%')
    return ax