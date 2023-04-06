import os
import warnings
from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText

from openfabric_pysdk.context import OpenfabricExecutionRay
from openfabric_pysdk.loader import ConfigClass
from time import time

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span

# Load pre-trained spaCy model
nlp = spacy.load('en_core_web_sm')

# Define custom matcher for scientific questions
matcher = Matcher(nlp.vocab)
pattern = [{'LOWER': {'IN': ['what', 'how', 'why', 'who', 'when']}}, {'LOWER': 'is'}, {'ENT_TYPE': 'NORP', 'OP': '+'}]
matcher.add('SCIENCE_QUESTION', None, pattern)


from googlesearch import search

def search_for_answer(query):
    results = list(search(query, num_results=3))
    
    if results:
        return results[0]
    else:
        return "I'm sorry, I couldn't find an answer to your question."

############################################################
# Callback function called on update config
############################################################
def config(configuration: ConfigClass):
    pass


############################################################
# Callback function called on each execution pass
############################################################
def execute(request: SimpleText, ray: OpenfabricExecutionRay) -> SimpleText:
    output = []
    for text in request.text:        
        doc = nlp(text)
        matches = matcher(doc)
        if matches:
            entities = [doc[start:end] for _, start, end in matches]
            entity_str = ', '.join([str(e) for e in entities])
            
            answer = search_for_answer(entity_str)
            output.append(answer)
        else:
            output.append("I'm sorry, I don't understand the question.")
    return SimpleText(dict(text=output))
