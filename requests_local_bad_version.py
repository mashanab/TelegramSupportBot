from aiogram import types


# словарь id_message_in_stuff_group -> client_message: type.Message
requests = {}


def request_registration(id_message_from_stuff_group, client_message: types.Message):
    if id_message_from_stuff_group not in requests:
        requests[id_message_from_stuff_group] = client_message
    else:
        print("Error. The id_message was repeated.")


def deleting_request(id_message_in_stuff_group):
    del requests[id_message_in_stuff_group]
