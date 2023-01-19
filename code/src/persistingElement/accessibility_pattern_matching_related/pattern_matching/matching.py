import spacy
from spacy.matcher import Matcher
import json

import pattern_matching.patterns as patterns

import pprint
pp = pprint.PrettyPrinter()

# NLP and Matcher object
nlp = spacy.load("en_core_web_trf")
matcher = Matcher(nlp.vocab)

# Define pattern class with corresponding patterns
matcher.add("pattern1", [patterns.pattern1])
matcher.add("pattern2", [patterns.pattern2])

# on match event handler
def on_match(doc, match_id, start, end, text_segment, match_result):
    pattern = nlp.vocab.strings[match_id]  # pattern match ID
    span = doc[start:end]  # matched span
    # print(pattern)
    # print(doc.text)
    # print(span.text)
    match_result["match_status"] = "yes"
    match_item = {}
    match_item["pattern"] = pattern
    match_item["content"] = doc.text
    match_item["mathced_text"] = span.text
    match_item["bbox"] = {
        "column_min": text_segment["column_min"]
        , "column_max": text_segment["column_max"]
        , "row_min": text_segment["row_min"]
        , "row_max": text_segment["row_max"]
        , "width": text_segment["width"]
        , "height": text_segment["height"]
        }
    match_result["match_info"].append(match_item)


# match patterns
def match_patterns(file):
    doc = None
    f = open(file)
    data = json.load(f)
    match_result = {"filename": file, "match_status": "no", "match_info": []}
    for text_segment in data["texts"]:
        doc = nlp(text_segment["content"])
        matches = matcher(doc)
        for match_id, start, end in matches:
            on_match(doc, match_id, start, end, text_segment, match_result)
    return match_result
