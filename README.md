# KEGG pathway kgml parser
Python code to download and parse KEGG pathway kgml file

This code saves two information for each pathway.

1. Entry information including graphics and group information

2. Relation information

## Usage
```
python kgml_parser.py -p [pathway list file] -o [path to output directory] [-v]

python kgml_parser.py --pathway_list [pathway list file] --output_dir [path to output directory] [--verbose]
```

pathway_list: pathway list file (one line, one pathway entry) (Refer example file: pathway_list.txt)

output_dir: output directory for saving results

verbose: print progress bar (python package "tqdm" is required)
