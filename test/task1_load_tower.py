import json
import re
from db import DB
import pandas as pd
import func_replace as fr

with open('tower.json', 'r', encoding="utf-8") as f:
    data = f.read()
    

new_data = fr.str_rep(data)

# loads to dict
data_json = json.loads(f'[{new_data}]') 


# parse to dataframe
df = pd.DataFrame.from_dict(data_json)
df.fillna(value=pd.np.nan, inplace=True)

df['internet'] = df.internet.fillna('{}')
df['lift'] = df.lift.fillna('{}')
df['parking'] = df.parking.fillna('{}')
df['images'] = df.images.fillna('{}')
df['branches'] = df.branches.fillna('{}')
df['fee_component'] = df.fee_component.fillna('{}')
df['building_type'] = df.building_type.fillna('{}')
df['selling_point'] = df.selling_point.fillna('{}')
df['complex'] = df.complex.fillna('{}')
df['description'] = df.description.fillna('{}')

df['last_update_at'] = pd.to_datetime(df.last_update_at, unit='s') #convert to timestamp
df['create_at'] = pd.to_datetime(df.create_at, unit='s') #convert to timestamp
df['isactive'] = ((df['status']==0.0) | (df['status']==0)) #with use 0 is active (True) because from the data i not see status = 1, so i decide use 0 as active status


df['parking'] = list(map(lambda x: json.dumps(x), df['parking']))
df['lift'] = list(map(lambda x: json.dumps(x), df['lift']))
df['internet'] = list(map(lambda x: json.dumps(x), df['internet']))
df['images'] = list(map(lambda x: json.dumps(x), df['images']))
df['branches'] = list(map(lambda x: json.dumps(x), df['branches']))
df['fee_component'] = list(map(lambda x: json.dumps(x), df['fee_component']))
df['building_type'] = list(map(lambda x: json.dumps(x), df['building_type']))
df['selling_point'] = list(map(lambda x: json.dumps(x), df['selling_point']))
df['complex'] = list(map(lambda x: json.dumps(x), df['complex']))
df['description'] = list(map(lambda x: json.dumps(x), df['description']))


db = DB()
db.insert_dataframe(df, 'public', 'tower')

db.close_conn()