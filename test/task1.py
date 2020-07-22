import sql_query as sq
from db import DB

db = DB()

db.query_execute(sq.insert_master_complex)
print("Insert to Table master.complex")

db.query_execute(sq.update_master_complex)
print("Updated Table master.complex")

db.query_execute(sq.insert_master_tower)
print("Insert to Table master.tower")

db.query_execute(sq.update_master_tower)
print("Updated Table master.tower")

db.query_execute(sq.insert_master_unit)
print("Insert to Table master.unit")

db.query_execute(sq.update_master_unit)
print("Updated Table master.unit")

db.close_conn()