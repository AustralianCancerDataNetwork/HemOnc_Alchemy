# HemOnc Alchemy

Purpose: to provide an interface to the HemOnc data model that is compatible with [OMOP Alchemy interface](https://github.com/AustralianCancerDataNetwork/OMOP_Alchemy)

### Notes

To create your own sqlite version of the data model, you will need to access the source hemonc tables and run the import steps available in the [import source notebook](notebooks/01_import_hemonc_source.ipynb) 

Else, to request a demo version of the sqlite reference database, please reach out to the authors.

### Quickstart

Copy the file `.env_sample` (as `.env`) to set the environment variable for the directory where your db connection config file will live. 

Copy the file `oa_system_config_sample.yaml` in the same way, updating the absolute path for your reference database.

### ERD

An overview ERD can be found [here](notebooks/db_fig.pdf) for reference and ease of use

### Examples

Some key example queries can be found [here](notebooks/03_example_usage.ipynb) - see reference [here](notebooks/OHDSI_2024.pdf) for 
descriptions.
