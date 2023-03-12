# https://github.com/JoiFoi/JoiChat

import requests
import json
import DataProcessor

bot_token = <bot_token> # Replace <bot_token> with your actual bot token
chatSonic_token = <chatSonic_token> # Replace <chatSonic_token> with your actual ChatSonic token

# Generate request links (https://core.telegram.org/bots/api#making-requests)
def requestLink(method_name):
    return f'https://api.telegram.org/bot{bot_token}/{method_name}'

# Let's make sure our bot is running
if requests.get(requestLink('getMe')).json()['ok'] == True:
    print('@' + requests.get(requestLink('getMe')).json()['result']['username'] + ' is running!')
else:
    print('Something went wrong!')

# Get a list of messages sent to your bot since the last update
def get_updates(offset = None):
    return requests.get(requestLink('getUpdates') , {'offset' : offset}).json()

# Send a message to a user or group that sent a message to your bot
def send_message(chat_id, text_to_send):
    requests.post(requestLink('sendMessage') , {'chat_id' : chat_id , 'text' : text_to_send , 'disable_web_page_preview' : True})

# Connect to ChatSonic API and send requests
def chatsonic_API(chat_id , text_received):
    payload = {
    "enable_google_results": True,
    "enable_memory": False,
    "input_text": text_received
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-API-KEY": chatSonic_token
    }
    send_message(chat_id , requests.post('https://api.writesonic.com/v2/business/content/chatsonic?engine=premium' , json=payload, headers=headers).json()['message'])

# Process user messages to send a proper response to them
def message_handler(update_content):
    if update_content['result'][0]['message']['text'] == '/start': # /start
        send_message(update_content['result'][0]['message']['chat']['id'] , open('PreWrittenMessages/start.txt' , mode = 'r').read())
        send_message(update_content['result'][0]['message']['chat']['id'] , 'Hello, how may I assist you today?')
        DataProcessor.file_creator(update_content)

    elif update_content['result'][0]['message']['text'] == '/source': # /source
        send_message(update_content['result'][0]['message']['chat']['id'] , open('PreWrittenMessages/source.txt' , mode = 'r').read())

    else:
        chatsonic_API(update_content['result'][0]['message']['chat']['id'] , update_content['result'][0]['message']['text'])
        DataProcessor.data_collector(update_content)
          

# Main block
def main():
    last_update_id = None
    while True:
        try:
            if len(get_updates(last_update_id)['result'][0]) > 0: # There's a new message!
                update_content = get_updates(last_update_id)
                last_update_id = update_content['result'][0]['update_id'] + 1
                message_handler(update_content)
        except:
            pass

# Allows you to execute code when the file runs as a script, but not when it's imported as a module
if __name__ == '__main__':
    main()
