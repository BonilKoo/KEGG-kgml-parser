# KEGG-kgml-parser
Python code to download and parse KEGG kgml file

## Usage
```
python kgml_parser.py -p pathway_list.txt -o result [-v]

python kgml_parser.py --pathway_list pathway_list.txt --output_dir result [--verbose]
```

pathway_list: pathway list file (one line, one pathway entry) (Refer example file: pathway_list.txt)

output_dir: output directory for saving results

verbose: print progress bar
