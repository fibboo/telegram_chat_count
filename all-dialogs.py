from pyrogram import Client

from config import api_id, api_hash

app = Client("my_account", api_id=api_id, api_hash=api_hash)

with app:
    for dialog in app.get_dialogs():
        # name_data = [dialog.chat.first_name, dialog.chat.last_name,
        #              dialog.chat.username, dialog.chat.title]
        # name = ' '.join([i for i in name_data if i is not None])
        # print(name, dialog.chat.id)
        if dialog.chat.title in [
            'FIRE 🔥 ЧАТ',
            'RationalAnswer Chat'
        ]:
            print(dialog.chat.title, dialog.chat.id)
