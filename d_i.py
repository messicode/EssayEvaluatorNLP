import spacy
import numpy as np
nlp=spacy.load("en_core_web_sm")


def get_essay_emb(essay):
    doc=nlp(essay)
    # print (essay)
    sent_embeddings=[]
    for sent in doc.sents:
        # print(sent)
        words=nlp(sent.text)
        word_embeddings=[token.vector for token in words if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV'] and token.is_stop == False]
        if word_embeddings:
            sent_embeddings.append(np.mean(word_embeddings,axis=0))
        else:
            sent_embeddings.append(np.zeros_like(words[0].vector))
    return sent_embeddings

def get_semantic_analyses(prompt,essay):

    # print(prompt)
    # get the emb
    prompt_embedding=get_essay_emb(prompt)
    sent_embedding=np.mean(get_essay_emb(essay),axis=0)
    # Calculate the cosine similarity
    cos_sim=np.dot(prompt_embedding,sent_embedding) / (np.linalg.norm(prompt_embedding) * np.linalg.norm(sent_embedding))
    return cos_sim.item()

# essay= """Early in the morning, Dr. Smith went to the hospital. Upon arrival, he remarked, 'It's going to be a long day.' The E.R. was busy, patients were waiting, and the staff was overwhelmed. Despite this, Dr. Smith, along with Nurse Amy, managed the situation well. They treated a man who had fallen off a ladder, a young girl with a high fever, and Mrs. Johnson, who complained about a severe headache. 'Thank you, Doctor,' said Mrs. Johnson, 'I feel much better now.' By noon, the chaos had subsided, and Dr. Smith finally took a break."""
#
# prompt="""Morning doctor."""
#
# print(get_semantic_analyses(prompt,essay))