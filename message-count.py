from pyrogram import Client

chat_id = 000000  # chat id in which you what to count messages


def chat_message_rating():
    with Client("my_account") as app:
        dic = {}
        all_messages_count = 0
        chat_title = app.get_chat(chat_id).title
        for message in app.iter_history(chat_id):
            if getattr(message, "from_user", None)\
                    and message.from_user.is_bot is False:
                all_messages_count += 1
                username = "Нет логина"
                if message.from_user.username:
                    username = f"@{message.from_user.username}"

                key = f"{message.from_user.first_name} ({username})"
                if key not in dic:
                    dic[f"{message.from_user.first_name} ({username})"] = 1
                else:
                    dic[f"{message.from_user.first_name} ({username})"] += 1

        sorted_dic = {
            k: v for k, v in
            sorted(dic.items(), key=lambda item: item[1])
        }

        count = 0
        dic_len = len(sorted_dic)
        message = (
            f"**Статистика сообщений и пользователей в этом чате "
            f"({chat_title})**\n"
            "\n"
            f"Всего сообщений в чате: **{all_messages_count}**\n"
            "\n"
            "**Топ 10 пользователей:**\n"
        )
        for key in sorted_dic:
            place = dic_len - count
            count += 1
            if place == 1:
                percent = round(sorted_dic[key] / all_messages_count * 100, 2)
                message += (
                    "\n"
                    "<i><strong>И наш победитель!</strong></i>\n"
                    "\n"
                    f"<i><strong>{place}. {key}: {sorted_dic[key]}"
                    f" ({percent}%)</strong></i>\n"
                )
            elif place <= 10:
                percent = round(sorted_dic[key] / all_messages_count * 100, 2)
                message += (f"**{place}**. {key}: **{sorted_dic[key]}" 
                            f" ({percent}%)**\n")

        app.send_message(chat_id, message)
        print(message)


chat_message_rating()
