import sql_query_task3 as sq3
from db import DB

db = DB()

db.query_execute(sq3.query_view)
print("Create or Replace View master.v_analytic_property")

db.query_execute(sq3.insert_query)
print("Insert to Table master.analytic_property")

db.query_execute(sq3.update_query)
print("Updated Table master.analytic_property")


db.close_conn()