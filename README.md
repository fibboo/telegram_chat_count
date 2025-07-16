# telegram chat messages count
### About
This app has three py files.
1. all-dialogs.py shows in console all dialogs.
2. message-count.py counts all messages in specified chat
and sends message to target chat with top 10 users
by message count. <br>
3. download-messages.py downloads messages and attached files
from specified chats and saves them to a local directory. <br>

It is made with a help of [Pyrogram](https://github.com/pyrogram/pyrogram)
### How to install
Clone repository, set up python environment ant install requirements
```shell
$ git clone git@github.com:fibboo/telegram_chat_count.git
$ cd telegram_chat_count/
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirments.txt
```
Copy config.ini.template to config.ini and enter
your **telegram api id** an **api hash**<br>
You can read instructions on how to get this credentials
in [official Telegram documentation](https://core.telegram.org/api/obtaining_api_id)
```shell
$ cp config.py.template config.py
$ nano config.py
```
### How to use
First you need to find out the chat id where you what to count messages.
Run all-dialogs.py and find the chat in the list.
At first time the app will ask you to authorize.
```shell
$ python all-dialogs.py
```
Copy the id of selected chat, go to message-count.py and paste
it instead of _000000_ for chat_id variable.
Run script
```shell
$ python message-count.py
```
It may take some time, but eventually script will send
a message to target chat from your account. It will look like this:
```text
Статистика сообщений и пользователей в этом чате (Название чата)

Всего сообщений в чате: 145654

Топ 10 пользователей:
10. Logan (@logan): 342 (0.45%)
9. Татьяна (@tat): 453 (1.45%)
8. Анна (@ann): 562 (2.45%)
7. Дарья (@dart): 1888 (3.45%)
6. Ира (@irina): 2111 (4.45%)
5. Саша (@alex_x): 3777 (5.45%)
4. Вова (@vovan): 4333 (6.45%)
3. Владимир (@vladB): 5444 (7.45%)
2. Игорь (@igor): 6880 (8.45%)

И наш победитель!

1. Петя (@petya): 7620 (9.55%)
```

### How to download messages and files
To download messages and attached files from a Telegram chat, first find the chat ID using the all-dialogs.py script as described above. Then run the download-messages.py script:

```shell
$ python download-messages.py
```

The script will prompt you to enter a chat ID if none are specified in the script. You can also edit the script to add chat IDs directly:

1. Open download-messages.py
2. Find the `chat_ids` list (around line 124)
3. Add your chat IDs to the list, for example:
   ```python
   chat_ids = [
       "-1001163044366",
       "-1009374794832",
   ]
   ```

The script will:
1. Create a "downloads" directory in the current folder
2. Create a subdirectory for each chat using the chat ID
3. Save all messages to a "messages.txt" file in chronological order (oldest to newest)
4. Download all media files (photos, documents, videos, audio, voice messages)
5. Name files with message ID, date/time, and media type (e.g., "msg12345_20230515_123045_photo_1")
6. Handle multiple files attached to a single message with sequential numbering
7. Show progress and statistics during the download
