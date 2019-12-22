import psycopg2
import random, string
import datetime 
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

import tables
               

class Database():
    engine = None
    Base = tables.Base

    def __init__(self):
        try:
            url = "postgresql://postgres:password@localhost:5432/postgres"
            self.engine = db.create_engine(url)
            self.connection = self.engine.connect()
            #self.table_names = self.Base.metadata.tables.keys()
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            print(error)
            exit()
    
    
    def connect_db(self):
        try:
            Session = sessionmaker(bind=self.engine) 
            session = Session()  
            res = session
        except (Exception, psycopg2.Error) as error:
            res = False
            print(error)
        return res 
            
    
    def select(self, table):
        session = self.connect_db()
        if not session: return False
        my_table = getattr(tables, table)
        try:
            res = session.query(my_table).all()
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            res = False
            print(error)
        session.commit()
        return res
    
    
    def insert(self, table, table_columns, values):
        session = self.connect_db()
        if not session: return False
        my_table = getattr(tables, table)
        new_row = my_table(*values)
        try:
            session.add(new_row)
            res = True
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            res = False
            print(error)
        session.commit()
        return res
        
        
    def delete(self, table, where = ""):
        session = self.connect_db()
        if not session: return False
        my_table = getattr(tables, table)
        filter = {f"{where[0]}" : f"{where[1]}"}
        try:
            session.query(my_table).filter_by(**filter).delete()
            res = True
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            res = False
            print(error)
        session.commit()
        return res
    
    
    def update(self, table, set = "", where = ""):
        session = self.connect_db()
        if not session: return False
        my_table = getattr(tables, table)
        filter = {f"{where[0]}" : f"{where[1]}"}
        values = {f"{set[0]}" : f"{set[1]}"}
        print(filter)
        print(values)
        try:
            session.query(my_table).filter_by(**filter).update(values)
            res = True
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            res = False
            print(error)
        session.commit()
        return res
                
def connect_db():
    try:
        res = psycopg2.connect(host="localhost", port="5432", 
                                database="postgres", user="postgres", 
                                password='password')
    except (Exception, psycopg2.Error) as error:
        res = False
        print(error)
    return res 

    
def select(table, id = "", fields = "*", where = ""):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT " + fields + " FROM " + table + ' ' + where + "ORDER BY " + id +" ASC")
        res = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        res = False
        print(error)
    conn.commit()
    cursor.close()
    conn.close()
    return res
    
def select1(table, where = "", fields = "*"):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT " + fields + " FROM " + table + ' ' + where)
        res = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        res = False
        print(error)
    conn.commit()
    cursor.close()
    conn.close()
    return res    

    
def random_author(num):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("insert into player (nickname) select * FROM rand_player({})".format(num))
        res = True
    except (Exception, psycopg2.Error) as error:
        res = False
        print(error)
    conn.commit()
    cursor.close()
    conn.close()
    return res

    
def full_text_search(table, where, mode):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        if mode == '1':
            cursor.execute("select * from {} where {}".format(table, where))
            res = cursor.fetchall()
        elif mode == '2':
            cursor.execute("select * from {} where {}".format(table, where))
            res = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        res = None
        print(error)
    conn.commit()
    cursor.close()
    conn.close()
    return res

