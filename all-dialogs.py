from pyrogram import Client, filters

app = Client("my_account")


with app:
    for dialog in app.iter_dialogs():
        name_data = [dialog.chat.first_name, dialog.chat.last_name,
                     dialog.chat.username, dialog.chat.title]
        name = ' '.join([i for i in name_data if i is not None])
        print(name, dialog.chat.id)
