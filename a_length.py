# To count number of sentences considering complex sentences as 2 sentences
# Can be improved to check for more than 2 sentences

import spacy
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def count_sentences(essay):
    doc = nlp(essay)
    sentence_count = 0
    for sent in doc.sents:
        additional_sentence=1
        finite_verb = 0
        cap_check = False
        conjunction = False
        # Check for mid-sentence capitalization and finite verbs
        tokens = list(sent)
        # print(sent)
        for i, token in enumerate(tokens):
            # print(token,token.pos_)
            # Skip the first token and capital words(nouns but ignores fully capital words except 'I')
            # for capitalization check
            if i > 0 and token.text[0].isupper() and token.pos_!="PROPN" and not(len(token.text)>1 and token.text.isupper()):
                    cap_check =True
            if token.pos_=="CCONJ": #Found conjunction
                conjunction=True
            # Counts verbs/aux found
            if token.pos_ == "VERB" or token.pos_=="AUX":
                finite_verb += 1
        # If only 1 finite verb then 1 sentence possible otherwise check for complex/multiple sentences
        if finite_verb>1 and (conjunction or cap_check):
            additional_sentence+=min(finite_verb - 1, int(conjunction) + int(cap_check))
        sentence_count+=additional_sentence
        # print(sent)
        # print("count",sentence_count)
    return sentence_count

#
# Example essay text
# essay= """Early in the morning, Dr. Smith went to the hospital. Upon arrival, he remarked, 'It's going to be a long day.' The E.R. was busy, patients were waiting, and the staff was overwhelmed. Despite this, Dr. Smith, along with Nurse Amy, managed the situation well. They treated a man who had fallen off a ladder, a young girl with a high fever, and Mrs. Johnson, who complained about a severe headache. 'Thank you, Doctor,' said Mrs. Johnson, 'I feel much better now.' By noon, the chaos had subsided, and Dr. Smith finally took a break."""
#essay="""I am writing this code."""
# essay="""The E.R. was busy, patients were waiting, and the staff was overwhelmed."""
# essay="""I would really prefer to travel on my own with plenty on time, but who wouldn’t? Unfortunately that is not always possible. It is always nicer to walk looking around at the same time, steping by little shops and cafes, talking to people, asking for directions, going to the places you choose to go to and discovering everything on your own. I think that is the travel ideal for many of us, but we usually have a hard time on finding the time to do it that way, and instead make plans with too many destinations all at once in a small schedule."""
# print(essay)
# print("Number of sentences:", count_sentences(essay))
