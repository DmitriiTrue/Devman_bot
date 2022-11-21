import requests
import telegram
import time
import os

from dotenv import load_dotenv
from textwrap import dedent


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.getenv('TG_BOT_TOKEN'))
    headers = {'Authorization': os.getenv('DEVMAN_TOKEN')}
    connection_attempts = 0
    while True:
        try:
            params = {'timestamp':time.time()}
            response = requests.get('https://dvmn.org/api/long_polling', headers=headers,
                                                         params=params, timeout=60)
            response.raise_for_status()
            lesson_info = response.json()['new_attempts'][0]
            if lesson_info['is_negative']:
                message_text = dedent("""
                Один из твоих уроков '{}' проверен.
                Урок не принят, потому что ты косяк.
                Жми на ссылку - {} и исправляй.
                """.format(lesson_info['lesson_title'], lesson_info['lesson_url']))
            else:
                message_text = dedent("""
                Один из твоих уроков '{}' проверен.
                Наконец-то они оценили твою гениальность.
                Жми на ссылку - {}."""
                .format(lesson_info['lesson_title'], lesson_info['lesson_url']))
            bot.send_message(text=message_text, chat_id=os.getenv('RECIPIENT_ID'))
        except requests.exceptions.ConnectionError:
            connection_attempts += 1
            if connection_attempts > 5:
                time.sleep(60 * 60)
                connection_attempts = 0
            print('There is no connection to the server. Try later')
        except requests.exceptions.ReadTimeout:
            continue


if __name__=='__main__':
    main()