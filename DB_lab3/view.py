import os
from controller import tables, columns
      
  
def show_main_menu():
    print('''\n+=+=+=+=+=+=+=+Main menu:=+=+=+=+=+=+=+
      1. Select
      2. Insert
      3. Update
      4. Delete
      5. Full text search
      6. Games in price range
      7. Game of developer
      8. Random player
      9. Clear screen
      0. Exit\t\n+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+''')
    
  
def fts_mode():
    print('''\n+=+=+=+=+=+=+Search mode:=+=+=+=+=+=+=+ 
    1. Required word entry
    2. Full phrase
    0. Back to menu\n+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+''')
    

def back_to_menu():
    print('''\n+=+=+=+=+=Back to main menu:+=+=+=+=+=+
    1. Yes
    0. No\n+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+''')
    

    

def table_columns_names(table):
    table_columns = columns[tables[table]]
    print('+='*20) 
    for i in range(len(table_columns)):
        print(str(i+1) + ". " + table_columns[i])
    print("0. Back to menu")
    print('+='*20) 

    
def tables_names():
    print('+='*20) 
    print("Choose table:")
    for k, v in tables.items():
        print("{}. {}".format(k, v))
    print("0. Back to menu")
    print('+='*20) 
        
    
def print_table(table, notes):
    if not notes: 
        print('+='*20) 
        print('No data')
        print('+='*20) 
        return
    print()
    table_columns = columns[tables[table]]
    print('+='*20) 
    for note in notes:
        for i in range(len(note)):
            print(table_columns[i] + ' -', note[i])           
        print('+='*20)      



def print_orm_table(notes):
    if not notes: 
        print('\nNo data')
        return
    for note in notes:
        print(note)         
        print('-'*40)          