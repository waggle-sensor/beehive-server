import pandas as pd
from glob import glob

df = pd.concat(pd.read_csv(f, dtype={'node_id': str})
               for f in glob('*/nodes.csv'))
df.start_timestamp = pd.to_datetime(df.start_timestamp)
df.end_timestamp = pd.to_datetime(df.end_timestamp)

errors = pd.DataFrame({'errors': df.groupby('node_id').node_id.count() > 1})

merged = df.join(errors, how='left', on='node_id')

merged.loc[merged.errors == True, 'node_id'] = '>>> ' + \
    merged[merged.errors].node_id

merged.sort_values(['errors', 'node_id']).drop(
    'errors', axis='columns').to_csv('master.csv', index=False)
