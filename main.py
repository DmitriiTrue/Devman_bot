import requests
import telegram
import time
import os

from dotenv import load_dotenv
load_dotenv()

bot = telegram.Bot(token=os.getenv('TG_BOT_TOKEN'))


def main():
    token = os.getenv('DEVMAN_TOKEN')
    headers = {'Authorization': token}
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling', headers=headers)
            response.raise_for_status()
            timestamp = response.json()['timestamp_to_request']
            params = {'timestamp': timestamp}
            response = requests.get('https://dvmn.org/api/long_polling', headers=headers,
                                                         params=params, timeout=60)
            response.raise_for_status()
            lesson_info = response.json()['new_attempts'][0]
            if lesson_info['is_negative']:
                message_text = f"Один из твоих уроков '{lesson_info['lesson_title']}' проверен." \
                               f" \n\nУрок не принят, потому что ты косяк.\nЖми на ссылку" \
                               f" {lesson_info['lesson_url']} и исправляй"
            else:
                message_text = f"Один из твоих уроков '{lesson_info['lesson_title']}' проверен." \
                               f"\n\nНаконец-то они оценили твою гениальность.\nЖми на ссылку" \
                               f" {lesson_info['lesson_url']}."
            bot.send_message(text=message_text, chat_id=os.getenv('MY_ID'))
        except requests.exceptions.ConnectionError:
            print('There is no connection to the server. Try later')
            time.sleep(60 * 10)
        except requests.exceptions.ReadTimeout:
            continue


if __name__=='__main__':
    main()




