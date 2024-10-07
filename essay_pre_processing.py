#To take all the essays and calculate base parameters a, b ,c etc

import csv
import os
import numpy as np
import a_length
import c_3
import c_syntax_grammar
import classifiers
import d_i
import scoring
import spacy

nlp=spacy.load("en_core_web_sm")

# Get dictionary with file_number and a tuple{prompt,grade}
def get_essay_details(path):
    essay_details = {}
    # print("dets----------------------")
    with open(path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        next(csvreader, None)
        for row in csvreader:
            file_number, prompt, grade = row
            #Extracting topical prompt
            top_prompt=list(nlp(prompt).sents)[1].text
            file_number = file_number.rstrip('.txt')
            # print(file_number)
            essay_details[file_number] = {'prompt':top_prompt,'grade': grade}
            # print(f"File num: {file_number}, prompt: {prompt}, Grade:{grade}")
    return essay_details


# Get dictionary containing file_number and its essay
def get_essays(path):
    # print("ess-----------------")
    essay_files = [file for file in os.listdir(path) if file.endswith('.txt')]
    essays = {}
    for essay in essay_files:
        file_num = essay.rstrip('.txt')
        file_path = os.path.join(path, essay)
        with open(file_path, 'r', encoding='utf-8') as file:
            essays[file_num] = file.read()
    return essays

# This finds and scales(1to5) the error, high lengths,low lengths, and their means
# Creates training set for classifiers

def pre_process(essays, essay_details):
    syn_error = np.array([])
    high_lengths = np.array([])
    low_lengths = np.array([])
    max_length = float('-inf')
    max_error = float('-inf')
    min_length = float('inf')
    min_error = float('inf')
    # Find values of corpora essays individually
    for file_num, essay in essays.items():
        l_essay = a_length.count_sentences(essay)
        c1,c2 = c_syntax_grammar.evaluate_syntax_grammar(essay)
        # Adjusting for c3 errors
        c3=c_3.evaluate_syn_well_form(essay)
        err=c1+c2+(2*c3)

        max_length = max(l_essay, max_length)
        max_error = max(err, max_error)
        min_error = min(err, min_error)
        min_length = min(l_essay, min_length)
        essay_details[file_num].update({'l':l_essay, 'e':err})
    # Score each essay on 1 to 5 on both criteria

    # Adjusting for range and creating arrays to find mean
    for details in essay_details.values():
        grade=details['grade']
        err=details['e']
        l=details['l']
        syn_error = np.append(syn_error, scoring.scoring(err, min_error, max_error, True))
        if grade == 'high':
            high_lengths = np.append(high_lengths, scoring.scoring(l, min_length, max_length, False))
        else:
            low_lengths = np.append(low_lengths, scoring.scoring(l, min_length, max_length, False))
    high_mean_length = np.round(np.mean(high_lengths),2)
    low_mean_length = np.round(np.mean(low_lengths),2)
    mean_error = np.round(np.mean(syn_error),2)
    # print(high_lengths)
    # print(low_lengths)
    # print(essay_details)
    return max_length,max_error,min_length,min_error,high_mean_length, low_mean_length, mean_error

# Computes prompts and essay similarity to have thresholds for mapping individual essays
def pre_process_prompts(essays,essay_details):
    prompts=set()
    cs_high_same = []
    cs_low_same = []
    cs_high_diff = []
    cs_low_diff = []
    # Gather all prompts
    for details in essay_details.values():
        prompts.add(details['prompt'])
        # print(details['prompt'])

    for prompt in prompts:
        #Pick another prompt with least cos_sim to current prompt
        sims={value: d_i.get_semantic_analyses(prompt, value) for value in prompts}
        diff_prompt=min(sims, key=sims.get)
        #Find cosine sim with given and unrelated prompt
        for file_num,details in essay_details.items():
            if prompt==details['prompt']:
                cs=d_i.get_semantic_analyses(prompt,essays[file_num])
                essay_details[file_num].update({'csim':cs})
                cs_diff=d_i.get_semantic_analyses(diff_prompt,essays[file_num])
                if(details['grade']=='high'):
                    cs_high_same.append(cs)
                    cs_high_diff.append(cs_diff)
                else:
                    cs_low_same.append(cs)
                    cs_low_diff.append(cs)

    csim_high_same=np.mean(cs_high_same) # max for high essays
    csim_low_same = np.mean(cs_low_same) # max for low essays
    csim_high_diff = np.mean(cs_high_diff) # min for high essays
    csim_low_diff = np.mean(cs_low_diff) # min for low essays
    # print(csim_low_diff,csim_low_same,csim_high_diff,csim_high_same)
    csim_high=(csim_high_same+csim_high_diff)/2
    csim_low=(csim_low_same+csim_low_diff)/2


    return scoring.scoring(csim_high,csim_high_diff,csim_high_same,False),scoring.scoring(csim_low,csim_low_diff,csim_low_same,False)


def essay_pre_processing(essay_details_path, essay_folder_path):
    essay_details = get_essay_details(essay_details_path)
    essays = get_essays(essay_folder_path)
    max_length,max_error,min_length,min_error,high_mean_length, low_mean_length, mean_error = pre_process(essays, essay_details)
    csim_high,csim_low=pre_process_prompts(essays,essay_details)
    #call classfiers here
    mlp_accuracy,log_reg_accuracy=classifiers.classify(essay_details)

    return essays,essay_details,max_length,max_error,min_length,min_error,high_mean_length, low_mean_length, mean_error, csim_high,csim_low,mlp_accuracy,log_reg_accuracy

# essays_dict = {
#     1: "This are the first essay. It has two sentences.",
#     2: "This are the second essay. It also is two sentences, but it's longer.",
# }
# es_dets = {
#     1:{"prompt":"jh", "grade":"low"},
#     2:{"prompt":"hj", "grade":"high"},
# }
# a,b,c=pre_process(essays_dict,es_dets)
# print(a,b,c)