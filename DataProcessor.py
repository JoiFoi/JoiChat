# https://github.com/JoiFoi/JoiChat

from time import ctime

# Create a file named after user's user_id && add his info to UsersList.txt
def file_creator(update_content):
    user_id = update_content['result'][0]['message']['chat']['id']
    user_firstname = update_content['result'][0]['message']['chat']['first_name']
    try: # The file doesn't exist
        open(f'DataBase/{user_id}' , 'x')
        with open('DataBase/UsersList.txt' , 'a') as UsersList_file:
            UsersList_file.write(f'{user_id} , {user_firstname} , {ctime()}\n')
    except: # The file exists already
        pass

# Append user's file whenever they send a request
def data_collector(update_content):
    user_id = update_content['result'][0]['message']['chat']['id']
    user_text = update_content['result'][0]['message']['text']
    try:
        with open(f'DataBase/{user_id}' , 'a') as user_file:
            user_file.write(f'{ctime()}\n{user_text}\n***\n')
    except:
        pass