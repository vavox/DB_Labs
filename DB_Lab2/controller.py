import os
import re

tables = {'1':'developer', 
          '2':'player', 
          '3':'videogame', 
          '4':'dev_game',
          '5':'game_player',
          }

columns = {'developer':['dev_id', 'name'],
           'player':['id', 'nickname'],
           'videogame':['game_id', 'v_name', 'genre', 'price'],
           'dev_game':['game_id', 'dev_id', 'release_date'],
           'game_player':['game_id', 'player_id', 'buy_date']
           }
           
columnins = {'developer':['name'],
           'player':['nickname'],
           'videogame':['v_name', 'genre', 'price'],
           'dev_game':['game_id','dev_id', 'release_date'],
           'game_player':['game_id','player_id', 'buy_date']
           }

fts_columns = {'developer':['name'],
               'player':['nickname'],
               'videogame':['v_name', 'genre'],
               }
              

import model as model
import view as view

              

def game_price_range():
    print("Input Range")
    print("price more than: ")
    lw= input()
    print("price less than: ")
    hg = input()
    where = ("WHERE ((price >= "+lw+")AND(price <= "+hg+")) ORDER BY game_id")
    return(model.select1("videogame",  where))
              


def game_of_developers(v_game):
    for temp in v_game:
        print("\n",temp.strip())
        try:
            yield model.select1("videogame, dev_game, developer",
                            "WHERE dev_game.dev_id = developer.dev_id \
                             AND dev_game.game_id = videogame.game_id \
                             AND (developer.name ILIKE '{}' \
                             OR developer.name ILIKE '{}')".format(temp.strip(),temp.strip()), "videogame.game_id, v_name, genre, price ")
        except (Exception, psycopg2.Error) as error:
            print(error)
            return  
            
def insert_into_table(table_num):
    table = tables[table_num]
    table_columns = columnins[table]
    values = []
    try:
        for i in range(len(table_columns)):
                answer = input(table_columns[i] + ' = ')
                values.append(answer)
    except Exception as error:
        print(error)
        return
    print("INSERT INTO " + table + " VALUES(" + ', '.join(values) + ')')
    res = model.insert(table, table_columns, values)
    return res
    
        
        
def delete_from_table(table_num):
    table = tables[table_num]
    table_columns = columns[table]
    while True:
        print("Choose column to delete by:")
        view.table_columns_names(table_num)
        chosen_column_num = input()
        if re.match(r'^[1-{}]{}$'.format(len(table_columns), "{1}"), 
                    chosen_column_num):
            chosen_column = table_columns[int(chosen_column_num)-1]
            print("Input value: ")
            print("DELETE FROM {} WHERE {} = ...".format(table, chosen_column))
            value = "'" + input() + "'"
            print("DELETE FROM {} WHERE {} = {}".format(table, 
                   chosen_column, value))
            where = " WHERE {} = {}".format(chosen_column, value)
            res = model.delete(table, where)
            return res
        elif chosen_column_num == '0':
            return
        else:
            print("No such option. Check your input")

           
def update_table(table_num):
    table = tables[table_num]
    table_columns = columns[table]
    while True:
        print("Choose column to update:")
        view.table_columns_names(table_num)
        chosen_column_num = input()
        if re.match(r'^[1-{}]{}$'.format(len(table_columns), "{1}"), 
                    chosen_column_num):
            set_column = table_columns[int(chosen_column_num)-1]
            print("Input value: ")
            print("UPDATE {} SET {} = ...".format(table, set_column))
            set_value = "'" + input() + "'"
            print("Choose column to update by:")
            view.table_columns_names(table_num)
            chosen_column_num = input()
            if re.match(r'^[1-{}]{}$'.format(len(table_columns), "{1}"), 
                    chosen_column_num):
                where_column = table_columns[int(chosen_column_num)-1]
                print("Input value: ")
                print("UPDATE {} SET {} = {} WHERE {} = ...".format(table, 
                      set_column, set_value, where_column))
                where_value = "'" + input() + "'"
                print("UPDATE {} SET {} = {} WHERE {} = {}".format(table, 
                      set_column, set_value, where_column, where_value))
                set = " SET {} = {}".format(set_column, set_value)
                where = " WHERE {} = {}".format(where_column, where_value)
                res = model.update(table, set, where)
                return res
            elif chosen_column_num == '0':
                return
            else:
                print("No such option. Check your input")       
        elif chosen_column_num == '0':
            return
        else:
            print("No such option. Check your input")       
  
  
def fts_table(text, mode, table_num):
    table = tables[table_num]
    to_tsvector = fts_columns[table]
    where = ' || '.join("to_tsvector(coalesce({}, ''))".format(w) 
                   for w in to_tsvector)
    where += " @@ plainto_tsquery('{}')".format(text)
    return(model.full_text_search(table, where, mode))
        
  
def main_menu():
    while True:
        view.show_main_menu()
        option = input()
        if re.match(r'^[1-5]{1}$', option):
            while True:
                    view.tables_names()
                    chosen_table = input()
                    if re.match(r'^[1-6]{1}$', chosen_table):
                        table = view.tables[chosen_table]
                        if option == '1':
                            table = tables[chosen_table]
                            table_columns = columns[table]
                            notes = model.select(table, table_columns[0])
                            view.print_table(chosen_table, notes)
                        elif option == '2':
                            res = insert_into_table(chosen_table)
                            if not res:
                                print("Data wasn't inserted")
                            else:
                                print("Successfully inserted")
                        elif option == '3':
                            res = update_table(chosen_table)
                            if not res:
                                print("Data wasn't updated")
                            else:
                                print("Operation successfull")
                        elif option == '4':
                            res = delete_from_table(chosen_table)
                            if not res:
                                print("Data wasn't deleted")
                            else:
                                print("Operation successfull")
                        elif option == '5':
                            text = input("Input text to search: ")
                            view.fts_mode()
                            mode = input()
                            if re.match(r'^[1,2]{1}$', mode):
                                notes = fts_table(text, mode, chosen_table)
                                view.print_table(chosen_table, notes) 
                            elif back_to_menu == '1':
                                break
                            else:
                                print("No such option. Check your input")
                    elif chosen_table == '0':
                        break
                    else:
                        print("No such option. Check your input")
                    view.back_to_menu()
                    back_to_menu = input()
                    if back_to_menu == '0':
                        continue
                    elif back_to_menu == '1':
                        break
                    else:
                        print("No such option. Check your input")
        elif option == '6':
            view.print_table('3', game_price_range())            
        elif option == '7':
            dev = input("Input authors names separated with comma: ")
            dev = dev.split(', ')
            for dev_list in game_of_developers(dev):
                view.print_table('3', dev_list)

        elif option == '8':
            num_of_rand = input("Number of random players\n")
            res = model.random_author(num_of_rand)
            if not res:
                print("Data wasn't updated")
            else:
                print("Successfully updated")
        elif option == '9':
            os.system("cls")
        elif option == '0':
            exit()
        else:
            print("No such option. Check your input")
      
    
if __name__ == "__main__":
    main_menu()