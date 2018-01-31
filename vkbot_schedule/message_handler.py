import vk
from Celery import app
from vkbot_schedule.analyzers import command_analyzer, actions_analyzer
from vkbot_schedule.settings import TOKEN

session = vk.Session()
api = vk.API(session, v=5.0)


def send_message(user_id, message):
    api.messages.send(access_token=TOKEN, user_id=str(user_id), message=message)


def create_response(message):
    return 'Это не команда'

# @app.task
# def test_msg4():
#     api.messages.send(access_token=TOKEN, user_id=21509713, message='3,8')


def message_handler(data):
    uid = data['user_id']  # id пользователя
    message = data['body']  # сообщение/запрос

    if message[0] == '!':
        response = command_analyzer(message, uid)
    elif message[0] == '@':
        response = actions_analyzer(message, uid)
    else:
        response = create_response(message)

    send_message(uid, response)

