import asyncio
from datetime import datetime, timedelta

from pyrogram import Client

from config import api_id, api_hash

chat_id = -1001619650644  # chat id in which you what to count messages


def chat_message_rating():
    with Client("my_account", api_id=api_id, api_hash=api_hash) as app:
        dic = {}
        all_messages_count = 0
        chat_title = app.get_chat(chat_id).title
        for message in app.iter_history(chat_id):
            if getattr(message, "from_user", None) \
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


class ChatStatistics:
    def __init__(self,
                 title: str,
                 members_count: int,
                 average_messages_per_day: float,
                 average_symbols_per_message: float,
                 average_symbols_per_day: float):
        self.title = title
        self.members_count = members_count
        self.average_messages_per_day = average_messages_per_day
        self.average_symbols_per_message = average_symbols_per_message
        self.average_symbols_per_day = average_symbols_per_day

    def __str__(self):
        return (f'Title: {self.title}\n'
                f'Member Count: {self.members_count}\n'
                f'Average Messages per Day: {self.average_messages_per_day}\n'
                f'Average Symbols per Message: {self.average_symbols_per_message}\n'
                f'Average Symbols per Day: {self.average_symbols_per_day}')


async def chats_statistics(chat_ids: list[str], date_from: datetime, date_to: datetime) -> list[ChatStatistics]:
    days_between = (date_to - date_from).days
    stats_dict: list[ChatStatistics] = []
    async with Client("my_account", api_id=api_id, api_hash=api_hash) as app:
        for chat_id in chat_ids:
            chat = await app.get_chat(chat_id)
            messages_count = 0
            symbols_count = 0
            parsing_date: datetime = datetime.now()
            async for message in app.get_chat_history(chat_id, offset_date=date_to):
                messages_count += 1
                if message.text is not None:
                    symbols_count += len(message.text)
                if message.caption is not None:
                    symbols_count += len(message.caption)
                date_hour = message.date.replace(minute=0, second=0, microsecond=0)
                if date_hour != parsing_date:
                    parsing_date = date_hour
                    print(f'Processing chat "{chat.title}", date_hour "{date_hour}"...')
                if message.date < date_from:
                    break

            average_messages_per_day = round(messages_count / days_between, 2)
            average_symbols_per_day = round(symbols_count / days_between, 2)
            average_symbols_per_message = round(symbols_count / messages_count, 2)
            chat_statistics = ChatStatistics(title=chat.title,
                                             members_count=chat.members_count,
                                             average_messages_per_day=average_messages_per_day,
                                             average_symbols_per_message=average_symbols_per_message,
                                             average_symbols_per_day=average_symbols_per_day)
            stats_dict.append(chat_statistics)

    return stats_dict


if __name__ == "__main__":
    chat_ids = [
        '-1001163885366',
        '-1001324794832',

    ]
    days_between = 3
    date_from = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_between + 1)
    date_to = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(days=1)
    stat_time = datetime.now()
    print(f'Started at {stat_time}')
    result: list[ChatStatistics] = asyncio.run(chats_statistics(chat_ids=chat_ids,
                                                                date_from=date_from,
                                                                date_to=date_to))
    finish_time = datetime.now()
    print(f'Finished at {finish_time}')
    print(f'Processing time: {(finish_time - stat_time)}')
    print()
    print(f'Statistics for selected chats within {days_between} last days ({date_from} - {date_to})')
    for chat in result:
        print()
        print(chat)
