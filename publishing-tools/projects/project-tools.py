import argparse
import pandas as pd
from glob import glob


def read_nodes_file(path):
    df = pd.read_csv(path, dtype={'node_id': str, 'vsn': str})
    df.start_timestamp = pd.to_datetime(df.start_timestamp)
    df.end_timestamp = pd.to_datetime(df.end_timestamp)
    return df


def import_nodes_files():
    df = pd.concat(read_nodes_file(f) for f in glob('*/nodes.csv'))

    errors = pd.DataFrame(
        {'errors': df.groupby('node_id').node_id.count() > 1})

    merged = df.join(errors, how='left', on='node_id')

    merged.loc[merged.errors == True, 'node_id'] = '>>> ' + \
        merged[merged.errors].node_id

    merged.sort_values(['errors', 'node_id']).drop(
        'errors', axis='columns').to_csv('master.csv', index=False)


def export_nodes_files():
    df = read_nodes_file('master.csv')

    for project_id, rows in df.groupby('project_id'):
        rows.sort_values(['vsn']).to_csv(
            f'tmp/{project_id}.csv', index=False, date_format='%Y/%m/%d %H:%M:%S')


commands = {
    'import': import_nodes_files,
    'export': export_nodes_files,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=list(commands.keys()))
    args = parser.parse_args()
    commands[args.command]()
