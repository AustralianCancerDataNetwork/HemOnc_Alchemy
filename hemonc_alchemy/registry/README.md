# Registry Contract

The registry module is a schema-driven compiler for the HemOnc data model.

It takes the authoritative HemOnc data dictionary and up to date CSV extracts, reconciles them into a single canonical registry, and generates:

* SQLAlchemy ORM entities
* Enum classes
* Lookup and normalisation tables
* Relationship mappings for denormalised source fields

The goal is to keep the ORM structurally aligned with curren HemOnc updates.

### Phases

1. Schema intent (authoritative)

The Excel HemOnc data dictionary defines:

* Tables
* Keys
* Descriptions
* Declared data types
* Intended semantics

This is treated as the source of truth.

-----

2. Observed reality (heuristics)

The actual CSV files are inspected to infer database-schema-friendly specification of what is described in the data dictionary.

* Appropriate Python data types
* Create enums with limited cardinality
* Boolean and datetime encodings
* Denormalised multi-value columns
* Candidate identity keys

-----

3. Registry (canonical model)

The result is a registry JSON that fully describes the resolved HemOnc schema:

* Columns and types
* Primary and identity keys
* Enums
* Normalisation groups
* Derived vs imported fields

This registry is:

* Deterministic
* Versionable
* Diff-able
* The only input to code generation

-----

4. Code generation

From the registry, HemOnc-Alchemy generates:

* `entities.py` – core ORM tables
* `enums.py` – Python enums
* `lookups.py` – lookup and association tables

No inference happens at this stage.

### Environment configuration

Create an `.env` file at the project root

```
data_dictionary_path=./data.dictionary.xlsx
table_path=./data
generation_path=./final_model
doc_path=./docs
```

### Prepare input

#### Data dictionary

An Excel file with:

* Content sheet
* Lookup sheet
* Optional per-table sheets for field-level metadata

#### Data files

* One CSV per table
* Filenames should match table names in the dictionary

### Build the registry and generate models

Run the main entrypoint:

This will:

* Read the Excel dictionary
* Load CSV data
* Enrich the registry with inferred metadata
* Write registry.json
* Generate SQLAlchemy models into final_model/

You should treat `registry.json` as the primary artefact for review and version control.

#### Relationship & normalisation handling

Columns that encode multiple values (e.g. A|B|C) are:

* Detected heuristically
* Grouped into normalisation sets
* Expanded into lookup and association tables
* Exposed via SQLAlchemy relationships

This allows:

* Lossless ingestion
* Relational querying
* Clean downstream analytics