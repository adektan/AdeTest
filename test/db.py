from sqlalchemy import create_engine
import psycopg2
import pandas as pd
# from dotenv import load_dotenv
# import os

# load_dotenv()


class DB:
    def __init__(self):
        """Connection to Postgresql DB Local"""
        db = 'postgres'
        db_user = 'postgres'
        db_pwd = 'password'
        db_url = 'localhost'
        db_port = '5432'
        db_connection = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (db_user, db_pwd, db_url, db_port, db)
       
        con = create_engine(db_connection)
        self.conn = con.connect()
#         self.cur = self.conn.cursor()
#         self.cur = self.conn.cursor()
#         self.con = create_engine(dwh_connection)
#         self.conn = self.con.connect()
    
    def select_data(self, query):
        results = []
        datas = self.conn.execute(query)
        for data in datas:
            results.append(data)
#         results = self.cur.fetchall()
        return results

    def query_execute(self, upsert_query):
        self.conn.execute(upsert_query)
        
    def select_dataframe(self, queries):
        self.df = pd.read_sql_query(queries, self.conn)
        return self.df
    
    def insert_dataframe(self, df_insert, schema_name, table_name):
        df_insert.to_sql(table_name, self.conn, schema = schema_name, if_exists='append',index=False, chunksize = 10000, method = 'multi')
    
    def close_conn(self):
#         self.cur.close()
        self.conn.close()
        """Close connection to Postgresql DB Local"""
