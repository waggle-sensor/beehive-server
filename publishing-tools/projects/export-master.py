import pandas as pd
from glob import glob

df = pd.read_csv('master.csv')

for project_id, rows in df.groupby('project_id'):
    print(project_id)
