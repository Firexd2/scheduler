import vk
from vkbot_schedule.analyzers import command_analyzer
from vkbot_schedule.settings import TOKEN

session = vk.Session()
api = vk.API(session, v=5.0)


def send_message(user_id, message):
    api.messages.send(access_token=TOKEN, user_id=str(user_id), message=message)


def create_response(message):
    return 'Это не команда'


def message_handler(data):
    uid = data['user_id']  # id пользователя
    message = data['body']  # сообщение/запрос

    if message[0] == '!':
        response = command_analyzer(message, uid)
    else:
        response = create_response(message)

    send_message(uid, response)

