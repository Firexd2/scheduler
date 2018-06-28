import vk

from vkbot_schedule.action import actions_delete_schedule, actions_all_schedule, actions_wishes
from vkbot_schedule.analyzers import *
from vkbot_schedule.settings import TOKEN

session = vk.Session()
api = vk.API(session, v=5.0)


def send_message(user_id, message):
    api.messages.send(access_token=TOKEN, user_id=str(user_id), message=message)


def create_response(message):
    message = message.lower()
    try:
        return ReplyMessages.objects.get(message=message).answer
    except:
        return 'Я тебя не понимаю. Чтобы понять друг друга, напиши "Помощь".'


def message_handler(data):
    uid = data['user_id']
    message = data['body']

    if message[0] == '!' and len(message) > 1:
        response = command_analyzer(message, uid)
    elif message[0] == '@' and len(message) > 1:
        response = actions_analyzer(message, uid)
    else:
        response = create_response(message)

    send_message(uid, response)


def command_analyzer(query, uid):

    list_query = query.split(' ')
    command = list_query[0].lower()
    q = list_query[1:]

    dict_command = {'!каждыйдень': query_analyzer_every_day,
                    '!кд': query_analyzer_every_day,
                    '!каждуюнеделю': query_analyzer_every_week,
                    '!кн': query_analyzer_every_week,
                    '!каждыймесяц': query_analyzer_every_month,
                    '!км': query_analyzer_every_month,
                    '!каждыйгод': query_analyzer_every_year,
                    '!кг': query_analyzer_every_year,
                    '!день': query_analyzer_day,
                    '!д': query_analyzer_day}
    try:
        response = dict_command[command](q, uid)
    except KeyError:
        response = 'Такой команды не существует'
    except Exception as error_message:
        response = error_message
    else:
        response = 'Команда успешно сохранена и активирована!\n' + response
    finally:
        return response


def actions_analyzer(query, uid):

    list_query = query.split(' ')
    action = list_query[0].lower()
    q = list_query[1:]

    dict_action = {
        '@удалить': actions_delete_schedule,
        '@у': actions_delete_schedule,
        '@список': actions_all_schedule,
        '@с': actions_all_schedule,
        '@пожелания': actions_wishes,
        '@п': actions_wishes,
    }

    try:
        response = dict_action[action](q, uid)
    except KeyError:
        response = 'Такого действия не существует'
    except Exception as error_message:
        response = error_message
    finally:
        return response
