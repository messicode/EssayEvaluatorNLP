import a_length
import c_3
import d_i
import essay_pre_processing
import c_syntax_grammar
import scoring

import threading
import itertools
import sys
import time
def get_grade(input_essay,high_mean_length,low_mean_length,mean_error,min_length,max_length,min_error,max_error,prompt,csim_high,csim_low):
    a = a_length.count_sentences(input_essay)
    c1, c2 = c_syntax_grammar.evaluate_syntax_grammar(input_essay)
    c3=c_3.evaluate_syn_well_form(input_essay)
    d_1=d_i.get_semantic_analyses(prompt,input_essay)

    print(f"\rRaw scores:\nNumber of sentences: {a},\nC1 errors (SV agreement errors): {c1},\nC2 errors (Verb form errors): {c2}")
    print(f"C3 errors(Syntax not well formed errors):{c3}\nSemantic similarity with prompt:{d_1}")
    # print(d_1, csim_low, csim_high)
    # print(high_mean_length,low_mean_length,mean_error)

    # Everything is given weight according to formula, except errors are given weightage implicitly
    means = 2*(high_mean_length + low_mean_length)/2 + mean_error + 3* (csim_low+csim_high)/2
    score = (2 * scoring.scoring(a, min_length, max_length, False) + scoring.scoring(c1 + c2 + 2*c3, min_error, max_error, True)
             + 3 * scoring.scoring(d_1,-1,1,False))
    if score<=means or a<11 or prompt==input_essay: return "LOW"
    else: return "HIGH"

def show_processing_animation(stop_event):

    for char in itertools.cycle('|/-\\'):
        sys.stdout.write('\r' + char)
        sys.stdout.flush()
        time.sleep(0.1)
        if stop_event.is_set():
            break
    sys.stdout.write('\r')  # Overwrite the character with spaces and return to start
    sys.stdout.flush()



def main():
    # Get the essay details and start pre-processing to get mean thresholds for low and high values
    essay_details_path = "index.csv"
    essay_folder_path = "essays"
    # Input from .txt file placed with main file
    with open("input_essay.txt", 'r', encoding='utf-8') as file:
        input_essay = file.read()
    with open("prompt.txt", 'r', encoding='utf-8') as file:
        prompt = file.read()

    # print(prompt)
    # Input from cmd
    # if len(sys.argv)!=2:
    #     print("Please give the essay text in inverted commas like so: \"text\" ")
    #     sys.exit(1)
    # input_essay=sys.argv[1]
    # Code to test each essay of corpora and see pred ratio which turns out to be 85%
    # essays=essay_pre_processing.get_essays(essay_folder_path)
    # essay_details=essay_pre_processing.get_essay_details(essay_details_path)
    # tot=0
    # rl=0
    # rr=0
    # for file_num,essay in essays.items():
    #     tot+=1
    #     grade_pred=get_grade(essay,high_mean_length,low_mean_length,mean_error,min_length,max_length,min_error,max_error)
    #     grade_actual=essay_details[file_num]['grade']
    #     if grade_pred==grade_actual :
    #         if grade_pred=="low": rl+=1
    #         else: rr+=1
    # print(rl,rr,tot)


    #SHow progress
    stop_event = threading.Event()
    animation_thread = threading.Thread(target=show_processing_animation, args=(stop_event,))
    animation_thread.start()

    # Pre-processing of essays corpora
    (essays,essay_details,max_length, max_error, min_length, min_error, high_mean_length, low_mean_length, mean_error,
     csim_high,csim_low,mlp_accuracy,log_reg_accuracy) = essay_pre_processing.essay_pre_processing(essay_details_path, essay_folder_path)

    # Fetch grade
    g = get_grade(input_essay, high_mean_length, low_mean_length, mean_error, min_length, max_length, min_error,
                  max_error, prompt, csim_high, csim_low)


    # Used for testing the whole corpora
    #
    # score=0
    # count=0
    # for file_num, details in essay_details.items():
    #     count+=1
    #     input_essay=essays[file_num]
    #     prompt=details['prompt']
    #     g = get_grade(input_essay, high_mean_length, low_mean_length, mean_error, min_length, max_length, min_error,
    #                   max_error,prompt,csim_high,csim_low)
    #
    #     if g.lower()==details['grade']:
    #         score+=1
    #
    # print(f"Score:{score/count}")
    #Stop animation
    stop_event.set()
    time.sleep(.2)
    animation_thread.join()


    print(f"\rGrade: {g}")
    print("\nF1 Accuracy using different classifiers:")
    print(f"Multilayer Perceptron accuracy:{mlp_accuracy}\nLogistic Regression accuracy:{log_reg_accuracy}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    exit(main())
