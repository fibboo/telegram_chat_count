import asyncio
import os
from datetime import datetime

from pyrogram import Client

from config import api_hash, api_id

# Directory to save downloaded files
DOWNLOADS_DIR = "downloads"


async def download_messages_and_files(chat_id: str, limit: int = 100):
    """
    Download messages and attached files from a specific chat.

    Args:
        chat_id: The ID of the chat to download messages from
        limit: Maximum number of messages to download (default: 100)
    """
    print(f"\n[INFO] Starting download process for chat ID: {chat_id}")
    print(f"[INFO] Will download up to {limit} messages")

    # Create downloads directory if it doesn't exist
    chat_download_dir = os.path.join(DOWNLOADS_DIR, str(chat_id).replace("-", "minus"))
    print(f"[INFO] Creating download directory: {chat_download_dir}")
    os.makedirs(chat_download_dir, exist_ok=True)

    # Create a text file to save messages
    messages_file_path = os.path.join(chat_download_dir, "messages.txt")
    print(f"[INFO] Messages will be saved to: {messages_file_path}")

    print(f"[INFO] Connecting to Telegram...")
    async with Client("my_account", api_id=api_id, api_hash=api_hash) as app:
        print(f"[INFO] Connection established")

        # Get chat information
        print(f"[INFO] Retrieving chat information for ID: {chat_id}")
        chat = await app.get_chat(chat_id)
        chat_title = chat.title or f"Chat_{chat_id}"
        print(f"[INFO] Downloading messages from: {chat_title}")

        # Open file to write messages
        print(f"[INFO] Opening file to write messages: {messages_file_path}")
        with open(messages_file_path, "w", encoding="utf-8") as messages_file:
            messages_file.write(f"Messages from {chat_title} ({chat_id})\n")
            messages_file.write("=" * 50 + "\n\n")
            print(f"[INFO] File header written")

            # Counter for downloaded files
            downloaded_files_count = 0
            processed_messages_count = 0

            print(f"[INFO] Starting to retrieve messages in chronological order (oldest to newest)...")
            # Get messages in default order (newest to oldest) and process them later
            messages = []
            async for message in app.get_chat_history(chat_id):
                messages.append(message)

            # Reverse the messages to get them in chronological order (oldest to newest)
            messages.reverse()

            # Process each message
            for message in messages:
                processed_messages_count += 1
                print(f"\n[INFO] Processing message #{processed_messages_count}...")

                # Format message date
                message_date = message.date.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[INFO] Message date: {message_date}")

                # Get sender information
                if message.from_user:
                    sender = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
                    if message.from_user.username:
                        sender += f" (@{message.from_user.username})"
                    print(f"[INFO] Sender: {sender}")
                else:
                    sender = "Unknown"
                    print(f"[INFO] Sender: Unknown")

                # Write message header
                print(f"[INFO] Writing message header to file")
                messages_file.write(f"[{message_date}] {sender}:\n")

                # Write message text
                if message.text:
                    print(f"[INFO] Message has text content")
                    messages_file.write(f"{message.text}\n")
                elif message.caption:
                    print(f"[INFO] Message has caption")
                    messages_file.write(f"{message.caption}\n")
                else:
                    print(f"[INFO] Message has no text content")
                print(f"[INFO] Message #{processed_messages_count} text saved to file")

                # Download media files
                print(f"[INFO] Checking for media attachments...")
                media_paths = []
                file_counter = 0  # Counter for multiple files in a single message
                date_time_str = message.date.strftime('%Y%m%d_%H%M%S')
                msg_id = message.id

                # Check for different types of media
                # Using separate if statements instead of if-elif to handle multiple media types
                if message.photo:
                    file_counter += 1
                    print(f"[INFO] Found photo attachment")
                    photo_path = os.path.join(chat_download_dir, f"{date_time_str}_photo_{file_counter}.jpg")
                    print(f"[INFO] Downloading photo to: {photo_path}")
                    media_path = await app.download_media(
                        message,
                        file_name=photo_path
                    )
                    if media_path:
                        print(f"[INFO] Photo downloaded successfully")
                        media_paths.append(media_path)
                        downloaded_files_count += 1
                    else:
                        print(f"[WARNING] Failed to download photo")

                if message.document:
                    file_counter += 1
                    print(f"[INFO] Found document attachment: {message.document.file_name}")
                    original_filename = message.document.file_name
                    extension = os.path.splitext(original_filename)[1] if original_filename else ""
                    doc_path = os.path.join(chat_download_dir, f"{date_time_str}_doc_{file_counter}{extension}")
                    print(f"[INFO] Downloading document to: {doc_path}")
                    media_path = await app.download_media(
                        message,
                        file_name=doc_path
                    )
                    if media_path:
                        print(f"[INFO] Document downloaded successfully")
                        media_paths.append(media_path)
                        downloaded_files_count += 1
                    else:
                        print(f"[WARNING] Failed to download document")

                if message.video:
                    file_counter += 1
                    print(f"[INFO] Found video attachment")
                    video_path = os.path.join(chat_download_dir, f"{date_time_str}_video_{file_counter}.mp4")
                    print(f"[INFO] Downloading video to: {video_path}")
                    media_path = await app.download_media(
                        message,
                        file_name=video_path
                    )
                    if media_path:
                        print(f"[INFO] Video downloaded successfully")
                        media_paths.append(media_path)
                        downloaded_files_count += 1
                    else:
                        print(f"[WARNING] Failed to download video")

                if message.audio:
                    file_counter += 1
                    print(f"[INFO] Found audio attachment: {message.audio.file_name}")
                    original_filename = message.audio.file_name
                    extension = os.path.splitext(original_filename)[1] if original_filename else ""
                    audio_path = os.path.join(chat_download_dir, f"{date_time_str}_audio_{file_counter}{extension}")
                    print(f"[INFO] Downloading audio to: {audio_path}")
                    media_path = await app.download_media(
                        message,
                        file_name=audio_path
                    )
                    if media_path:
                        print(f"[INFO] Audio downloaded successfully")
                        media_paths.append(media_path)
                        downloaded_files_count += 1
                    else:
                        print(f"[WARNING] Failed to download audio")

                if message.voice:
                    file_counter += 1
                    print(f"[INFO] Found voice message attachment")
                    voice_path = os.path.join(chat_download_dir, f"{date_time_str}_voice_{file_counter}.ogg")
                    print(f"[INFO] Downloading voice message to: {voice_path}")
                    media_path = await app.download_media(
                        message,
                        file_name=voice_path
                    )
                    if media_path:
                        print(f"[INFO] Voice message downloaded successfully")
                        media_paths.append(media_path)
                        downloaded_files_count += 1
                    else:
                        print(f"[WARNING] Failed to download voice message")

                # Write file information to message log
                if media_paths:
                    print(f"[INFO] Writing information about {len(media_paths)} attached files to message log")
                    for media_path in media_paths:
                        file_name = os.path.basename(media_path)
                        print(f"[INFO] Recording attachment: {file_name}")
                        messages_file.write(f"[Attached file: {file_name}]\n")
                else:
                    print(f"[INFO] No media attachments to record")

                print(f"[INFO] Adding message separator")
                messages_file.write("\n" + "-" * 40 + "\n\n")

                print(f"[PROGRESS] Processed {processed_messages_count} messages, downloaded {downloaded_files_count} files so far")

        print(f"\n[SUCCESS] Download completed for chat: {chat_title}")
        print(f"[SUMMARY] Chat: {chat_title}")
        print(f"[SUMMARY] Messages processed: {processed_messages_count}")
        print(f"[SUMMARY] Files downloaded: {downloaded_files_count}")
        print(f"[SUMMARY] Saved to: {os.path.abspath(chat_download_dir)}")


async def main():
    print("[INFO] Initializing download process")

    # List of chat IDs to download messages from
    chat_ids = [
        # Add your chat IDs here
        # For example:
        # "-1001163885366",
        # "-1001323994832",
    ]

    print(f"[INFO] Found {len(chat_ids)} chat IDs in configuration")

    # If no chat IDs are specified, ask the user
    if not chat_ids:
        print("[INFO] No chat IDs specified in the script.")
        print("[INFO] You can find chat IDs by running the all-dialogs.py script.")
        chat_id_input = input("[INPUT] Enter a chat ID to download messages from: ")
        if chat_id_input:
            print(f"[INFO] Adding chat ID: {chat_id_input}")
            chat_ids.append(chat_id_input)
        else:
            print("[WARNING] No chat ID provided, exiting")
            return

    # Download messages from each chat
    print(f"[INFO] Starting download for {len(chat_ids)} chats")
    for i, chat_id in enumerate(chat_ids, 1):
        print(f"[INFO] Processing chat {i} of {len(chat_ids)}: {chat_id}")
        await download_messages_and_files(chat_id)
        print(f"[INFO] Completed chat {i} of {len(chat_ids)}")


if __name__ == "__main__":
    start_time = datetime.now()
    print(f"[START] Script execution started at {start_time}")
    print(f"[INFO] Python version: {asyncio.sys.version}")

    # Create main downloads directory
    print(f"[INFO] Creating main downloads directory: {DOWNLOADS_DIR}")
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    try:
        # Run the main function
        print(f"[INFO] Starting main process")
        asyncio.run(main())
        print(f"[INFO] Main process completed successfully")
    except Exception as e:
        print(f"[ERROR] An error occurred during execution: {str(e)}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"[END] Script execution finished at {end_time}")
    print(f"[SUMMARY] Total execution time: {duration}")
    print(f"[SUMMARY] Hours: {duration.seconds // 3600}, Minutes: {(duration.seconds % 3600) // 60}, Seconds: {duration.seconds % 60}")
