# Get c1(Subject-verb agreement) and c2(Verb form errors) type errors
import spacy

nlp = spacy.load("en_core_web_sm")


def expl_check(sent):
    errors = 0
    expletive_used = False
    subject_detected = False

    for token in sent:
        # Detect expletives (e.g.,"There is/are")
        if token.dep_ == "expl":
            expletive_used = True
            continue  # When expletive found than check following verbs so skip this tokn check

        # Checks the first noun/pronouns plurality that comes after an expletive
        if expletive_used and not subject_detected and token.pos_ in ["NOUN", "PRON"]:
            subject_detected = True  # Mark that we've found the subject
            # Subject plurality check
            is_plural = token.tag_ in ["NNS", "NNPS"] or token.text.lower() in ["we", "they"]
            # Verb and expletive plurality agreement
            for child in token.head.children:
                if child.dep_ == "expl":
                    if (is_plural and child.head.tag_ == "VBZ") or (not is_plural and child.head.tag_ == "VBP"):
                        errors += 1  # Incorrect verb and epletive plurality
                    break

            expletive_used = False
            subject_detected = False

    return errors

# C1 errors
def sv_agreement_errors(sent):
    errors = 0
    subject_plural = False
    found_subject = False
    found_verb = False

    for token in sent:
        if token.dep_ in ["nsubj", "nsubjpass"]:
            found_subject = True #subject found
            # find subject plurality
            if token.tag_ in ["NNS", "NNPS"] or token.lower_ in ["we", "they", "you"]:
                subject_plural = True

        # 'And' points to compound subjects
        if found_subject and token.lower_ == "and":
            subject_plural = True
        # print(token, token.pos_, token.dep_, token.tag_,found_subject, subject_plural)

        # When subject is found and verb is not found yet but found now check plurality of subject and verb
        if found_subject and not found_verb and token.pos_ in ["VERB","AUX"]:
            found_verb = True
            if (subject_plural and token.tag_ == "VBZ") or (
                    not subject_plural and token.tag_ == "VBP"):
                errors += 1
            # print(found_verb)
            found_subject = False
            subject_plural = False
    return errors


# C2 errors
def verb_form_errors(sent):
    errors = 0
    last_aux = None
    for token in sent:
        # print(token,token.pos_,token.tag_)
        # Whenever an aux/MD is found, check the following verbs plurality agreement
        if token.pos_=="AUX" or token.tag_=="MD":
            last_aux = token
        elif token.pos_ == "VERB":
            if last_aux and ((last_aux.tag_ == "MD" and token.tag_ != "VB") or
                             (last_aux.lemma_ in ["have","be"] and token.tag_ != "VBN")): # [have, be] cant have following VBN
                errors += 1
            last_aux = None
    return errors


def evaluate_syntax_grammar(essay):
    doc = nlp(essay)
    c1 = 0  # Subject-Verb Agreement Errors
    c2 = 0  # Verb Form Errors

    for sent in doc.sents:
        # Aggregate scores
        a= sv_agreement_errors(sent)
        b= verb_form_errors(sent)
        c1+=a
        c2+=b
        # print(sent,a,b)
    return c1, c2

# Test sentences

# Example usage
# essay = """Jessica have 8 years old. He can eats a lot of food. The cats is hungry. John and Mary goes to school every day. They enjoys playing tennis. He do not like to read."""
# essay="""They enjoys playing tennis"""
# essay="""The cats is hungry."""
# essay="""John and Mary goes to school."""
# essay="""Does it looks clean?"""
# essay="""Successful people has the ambition to do new things to get what ever thy are looking not only to do that but also to get out of the darckness."""
# Same error detected has have in this sent as c1 checks for verb following aux/mod and c2 verb and sbj plurality
# essay="""He can eats a lot of food.""" # c2 test
# essay="""She can sings beautifully.""" # Issue in spacy as sings is reduced to base form sing which is correct
# errors = evaluate_syntax_grammar(essay)

#
# c1, c2 = evaluate_syntax_grammar(essay)
# print(f"Subject-Verb Agreement Errors Detected (c1): {c1}")
# print(f"Verb Form Errors Detected (c2): {c2}")

# # Expl check
# essay="""There is many books on the table."""
# doc = nlp(essay)
# err = expl_check(doc)
# print(f"Expl error:{err}")

# print(f"Errors detected: {errors}")
