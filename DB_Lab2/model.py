import psycopg2
import random, string
import datetime 
                
        
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

    
def insert(table, fields = "", values = ""):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    if type(values) is list:
        values = ["'{0}'".format(x) for x in values]
        values = ', '.join(values)
    if type(fields) is list:
        fields = ', '.join(fields)
    try:
        cursor.execute("INSERT INTO " + table + '(' + fields + ')' +
                             " VALUES " + '(' + values + ')')
        res = True
    except (Exception, psycopg2.Error) as error:
        res = False
        print(error)
    conn.commit()
    cursor.close()
    conn.close()
    return res
    
    
def delete(table, where = ""):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM " + table + ' ' +  where)
        res = True
    except (Exception, psycopg2.Error) as error:
        res = False
        print(error)
    conn.commit()
    cursor.close()
    conn.close()
    return res
    
    
def update(table, set = "", where = ""):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE " + table + ' ' + set + ' ' +  where)
        res = True
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

