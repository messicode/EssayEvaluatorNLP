# checking c3 synctactic well-formedness errors

import spacy

nlp=spacy.load("en_core_web_sm")


def evaluate_syn_well_form(essay):
    doc=nlp(essay)
    c3=0
    for sent in doc.sents:
        # print(sent)
        first_tok=sent[0]
        # For question sentence should start with wh or aux
        if sent.text.strip().endswith('?'):
            if first_tok.tag_ not in ['WDT', 'WP', 'WP$', 'WRB'] and first_tok.dep_!='aux':
                c3+=1
        # Otherwise Sentence with verb/aux in the beginning that is not aux/supporting another verb
        elif first_tok.pos_ in ['VERB', 'AUX'] and first_tok.dep_ not in ['aux', 'ROOT']:
            c3+=1
        # print(f"first:{c3}")
        prev=None
        for token in sent:
            # Singular noun check
            if token.pos_ == 'NOUN' and token.tag_ == 'NN':
                # Prev token makes det unnecessary
                if prev and (prev.dep_ != 'det' and prev.text.lower() not in ['the', 'a', 'an']):
                    # Check exceptions such as proper nouns, mass nouns, or nouns following certain prepositions
                    if prev.pos_ not in ['PROPN', 'ADP'] and token.text[0].islower():
                        c3+=1
            # print(f"{token.text}:{c3}")
            # Check for subordinating conjunction usage
            elif token.dep_ == 'mark':
                clause = [child for child in token.head.children if child.dep_ in ['csubj', 'ccomp']]
                if not clause:
                    c3 += 1
            prev = token
            # print(f"{token.text}:{c3}")
    return c3

# essay= """Early in the morning, Dr. Smith went to the hospital. Upon arrival, he remarked, 'It's going to be a long day.' The E.R. was busy, patients were waiting, and the staff was overwhelmed. Despite this, Dr. Smith, along with Nurse Amy, managed the situation well. They treated a man who had fallen off a ladder, a young girl with a high fever, and Mrs. Johnson, who complained about a severe headache. 'Thank you, Doctor,' said Mrs. Johnson, 'I feel much better now.' By noon, the chaos had subsided, and Dr. Smith finally took a break."""
#
# print(evaluate_syn_well_form(essay))