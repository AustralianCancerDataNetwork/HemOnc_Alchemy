"""Cross-entity enrichment layer — mirrors omop_alchemy's cdm/handlers/.

Tiers 2 and 3 of the split described in ../model/relationships.py's
docstring: fuzzy cross-reference resolution (linking.py) and clinical
classification (classification.py). Both consume the model but are not
themselves declarative ORM relationships — that distinction is the whole
point of splitting them out (US-16, US-17).
"""
