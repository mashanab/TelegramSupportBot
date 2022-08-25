from aiogram import types


def print_info_for_console(message: types.Message):
    if message.reply_to_message == None:
        print("msg_id: ", message.message_id, "\nusr_id", message.from_user.id, "\n\n")
        return
    print("msg_id: ", message.message_id, "\nusr_id", message.from_user.id, "\nforwarded_msg_id",
          message.reply_to_message.message_id, "\n\n")
