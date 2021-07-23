import argparse
import os
import wget
import copy
import pandas as pd
from xml.etree.ElementTree import parse

def parse_args():
    parser = argparse.ArgumentParser(description='Download, parse and save KEGG kgml')
    
    parser.add_argument('-p', '--pathway_list', required=True, help='pathway list file (one line, one pathway entry)')
    parser.add_argument('-o', '--output_dir', required=True, help='output directory to save results')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbosity')
    
    return parser.parse_args()

def mkdir(dir_name):
    os.system(f'mkdir -p {dir_name}')
    
def rmfile(filename):
    if os.path.exists(filename):
        os.system(f'rm -rf {filename}')
        
def load_pathway_list(pathway_list_file):
    return pd.read_table(pathway_list_file, names=['pathway'])['pathway'].to_list()

def download_kgml(pathway_list, kgml_dir, verbose):
    print('Download KEGG kgml files...')
    if verbose:
        from tqdm import tqdm
        for pathway_id in tqdm(pathway_list):
            wget.download(url=f'http://rest.kegg.jp/get/{pathway_id}/kgml', out=f'{kgml_dir}/{pathway_id}.xml', bar=False)
    else:
        for pathway_id in pathway_list:
            wget.download(url=f'http://rest.kegg.jp/get/{pathway_id}/kgml', out=f'{kgml_dir}/{pathway_id}.xml', bar=False)        
        
def parse_kgml(pathway_id, output_dir):
    tree = parse(f'{output_dir}/kgml/{pathway_id}.xml')
    root = tree.getroot()

    entries = tree.findall('entry')
    relations = tree.findall('relation')

    # entry
    entries_df = pd.DataFrame([entry.attrib for entry in entries])
    entries_graphics_df = pd.DataFrame([entries[idx].findall('graphics')[0].attrib for idx in entries_df.index])

    entries_df_merged = pd.merge(entries_df, entries_graphics_df, left_index=True, right_index=True)
    entries_df_merged.columns = ['id', 'entry', 'type', 'link', 'name', 'fgcolor', 'bgcolor', 'graphic_type', 'x', 'y', 'width', 'height']

    entries_df_merged.to_csv(f'{output_dir}/entry/{pathway_id}', index=False, sep='\t')
    
    # entry type group
    type_group_idx = entries_df[entries_df['type'] == 'group'].index
    entries_df_type_group = entries_df.loc[type_group_idx]

    output_file = open(f'{output_dir}/entry_group/{pathway_id}', 'w')
    for idx in entries_df_type_group.index:
        group_id = entries_df_type_group.loc[idx]['id']
        components = entries[idx].findall('component')
        components = ','.join([component.attrib['id'] for component in components])
        output_file.write(f'{group_id}\t{components}\n')
    output_file.close()
    
    # relation
    relation_list = []
    for relation in relations:
        for subtype in relation.findall('subtype'):
            relation_attrib = copy.deepcopy(relation.attrib)
            relation_attrib.update(subtype.attrib)
            relation_list.append(relation_attrib)

    relation_df = pd.DataFrame(relation_list)
    relation_df.to_csv(f'{output_dir}/relation/{pathway_id}', sep='\t', index=False)

def main():
    args = parse_args()
    
    # output directory
    rmfile(args.output_dir)
    mkdir(args.output_dir)
    
    # load pathway list
    pathway_list = load_pathway_list(args.pathway_list)
    
    # download kgml
    kgml_dir = args.output_dir + '/kgml'
    mkdir(kgml_dir)
    download_kgml(pathway_list, kgml_dir, args.verbose)
    
    # parse kgml and save
    mkdir(f'{args.output_dir}/entry')
    mkdir(f'{args.output_dir}/entry_group')
    mkdir(f'{args.output_dir}/relation')
    print('Parse kgml and save results...')
    for pathway_id in pathway_list:
        parse_kgml(pathway_id, args.output_dir)
        
    print('Done.')
    
if __name__ == '__main__':
    main()