import spacy, srsly
from spacy.lang.en import English
from spacy.symbols import ORTH, NORM
from collections import Counter
from spacy import displacy
from spacy.matcher import Matcher
from pathlib import Path 


# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

special_cases = []

from spacy.util import compile_infix_regex

units_num = ['mg', 'mcg', 'g', 'units', 'u', 'mgs', 'mcgs', 'gram', 'grams', 'mG', 'mL', 'mol', 'dl', 'min', 'hr']
units_denom = ['mg', 'mgc', 'g', 'kg', 'ml', 'l', 'm2', 'm^2', 'hr', 'liter', 'gram', 'L', 'mL', 'KG', 'ml',
               'mG', 'kG', 'kilogram', 'lb', 'pounds', 'lbs', 'kilos', 'Kg', 'dl', 'min', 'hr', '1.73']

unit_suffix = []

for a in units_num:
    nlp.tokenizer.add_special_case(f'{a}', [{ORTH: a, NORM: 'unit'}])
    for b in units_denom:
        nlp.tokenizer.add_special_case(f'{b}', [{ORTH: b, NORM: 'unit'}])
        if a != b:
            nlp.tokenizer.add_special_case(f'{a}/{b}', [{ORTH: a, NORM: 'unit_num'}, {ORTH: '/'}, {ORTH: b, NORM: 'unit_denom'}])
            unit_suffix.append(f'{a}/{b}')

units_regex = '|'.join([f'{u}' for u in units_denom])
units_regex = f'^(\d+)?({units_regex})$'


custom_infixes = (unit_suffix + list(English.Defaults.infixes)  + ['&', '@', '<', '>', ';', r'\(', r'\)', r'\|', '=', ':', ',', r'\/', '~',r'\+\+\+', r'\+\+', r'\+', r'\d+', r'\?'] + spacy.lang.char_classes.LIST_HYPHENS)
infix_re = compile_infix_regex(custom_infixes)
nlp.tokenizer.infix_finditer = infix_re.finditer

def get_widest_match(start, end, matches):
    for _, s, e in matches:
        if s<start<e or s<end<e:
            if e-s > end-start:
                return False
    return True

def get_token_spans(matcher, doc):
    spans, filtered_matches = [], []
    matches = matcher(doc) 
    for m in matches:
        if get_widest_match(m[1], m[2], matches):
            filtered_matches.append(m)
            spans.append(doc[m[1]:m[2]])
    return spans, filtered_matches

def match_entities(matcher, doc, token_label, merge=False):
    spans, matches = get_token_spans(matcher, doc)
    with doc.retokenize() as retokenizer:
        for span in spacy.util.filter_spans(spans):
            for tok in span:
                tok._.set(token_label, True) 
            if merge:
                retokenizer.merge(span)
    return doc

def get_modifier_child(doc):
    return [t.head for t in doc if t._.FACT_MODIFIER]

def get_nouns(doc):
    nn = [t.text for t in doc if t.pos_=='NOUN' and not t._.AGE and not t._.STAGE and not t._.UNITS and not t._.LAB and not t._.SIZE and not t._.FACT and not t._.FACT_MODIFIER]
    if len(nn):
        return nn

matchers = {}
rules = srsly.read_json(Path(__file__).parent / 'spacy_patterns.jsonl')

for label, config in rules.items():
    spacy.tokens.Token.set_extension(label, default=False, force=True)
    matchers[label] = Matcher(nlp.vocab)
    matchers[label].add(label, config['PATTERNS'])