import json
from db import DB
import pandas as pd
import func_replace as fr

with open('complex.json', 'r', encoding="utf-8") as f:
    data = f.read()

new_data = fr.str_rep(data)


# loads to dict
data_json = json.loads(f'[{new_data}]') 


# parse to dataframe
df = pd.DataFrame.from_dict(data_json)


df['last_update_at'] = pd.to_datetime(df.last_update_at, unit='s') #convert to timestamp
df['create_at'] = pd.to_datetime(df.create_at, unit='s') #convert to timestamp
df['isactive'] = ((df['status']==0.0) | (df['status']==0)) #with use 0 is active (True) because from the data i not see status = 1, so i decide use 0 as active status

df['facilities'] = list(map(lambda x: json.dumps(x), df['facilities']))
df['images'] = list(map(lambda x: json.dumps(x), df['images']))
df['branches'] = list(map(lambda x: json.dumps(x), df['branches']))
df['surrounding_area'] = list(map(lambda x: json.dumps(x), df['surrounding_area']))
df['address_area'] = list(map(lambda x: json.dumps(x), df['address_area']))
df['service_types'] = list(map(lambda x: json.dumps(x), df['service_types']))


db = DB()
db.insert_dataframe(df, 'public', 'complex')

db.close_conn()