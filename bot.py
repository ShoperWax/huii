from pyrogram import Client, filters
import os

api_id = '25463525'  # Ваш API ID
api_hash = '1b069b2bd4fb5d6793d2c4f4dfbbba29'  # Ваш API hash
SOURCE_CHANNEL_ID = '@nyudsye'  # Канал-источник
TARGET_CHANNEL_ID = '@intimnudess'  # Канал-назначения

app = Client("my_account", api_id, api_hash)

MAX_CAPTION_LENGTH = 4096  # Максимальная длина текста (увеличена до максимума Telegram)

# Функция для извлечения текста кнопок
def extract_buttons_text(reply_markup):
    buttons_text = []
    if reply_markup:
        for row in reply_markup.inline_keyboard:
            for button in row:
                # Получаем текст кнопки и добавляем его в список
                if button.text:
                    buttons_text.append(f"||{button.text}||")  # Скрываем текст кнопки под спойлером
    return "\n".join(buttons_text)  # Возвращаем текст кнопок через новую строку


@app.on_message(filters.chat(SOURCE_CHANNEL_ID))
async def forward_message(client, message):
    try:
        # Извлечение reply_markup (кнопок)
        reply_markup = message.reply_markup

        # Извлекаем текст кнопок, если они есть
        buttons_text = extract_buttons_text(reply_markup) if reply_markup else ""

        # Если это фото
        if message.photo:
            # Получаем file_id фотографии
            photo_file_id = message.photo.file_id
            file_path = await client.download_media(photo_file_id)

            if file_path:
                # Проверяем caption
                caption = message.caption if message.caption else ''
                if not caption and message.text:
                    caption = message.text

                # Добавляем кнопки в конец текста
                if buttons_text:
                    caption += "\n\n" + buttons_text

                # Отправляем фото
                if reply_markup:
                    await client.send_photo(TARGET_CHANNEL_ID, file_path, caption=caption, reply_markup=reply_markup)
                    print("Фото с кнопками переслано.")
                else:
                    await client.send_photo(TARGET_CHANNEL_ID, file_path, caption=caption)
                    print("Фото без кнопок переслано.")

                # Удаляем временный файл
                os.remove(file_path)

        # Если это фото через URL
        elif message.web_page and message.web_page.photo:
            photo_url = message.web_page.photo.file_id

            # Проверяем caption
            caption = message.caption if message.caption else ''
            if not caption and message.text:
                caption = message.text

            # Добавляем кнопки в конец текста
            if buttons_text:
                caption += "\n\n" + buttons_text

            if not caption:
                caption = "Фото из источника без текста"  # Текст по умолчанию

            # Отправляем фото по URL
            if reply_markup:
                await client.send_photo(TARGET_CHANNEL_ID, photo_url, caption=caption, reply_markup=reply_markup)
                print("Фото с кнопками (по URL) переслано.")
            else:
                await client.send_photo(TARGET_CHANNEL_ID, photo_url, caption=caption)
                print("Фото без кнопок (по URL) переслано.")

        # Если это видео
        elif message.video:
            file_id = message.video.file_id
            file_path = await client.download_media(file_id)

            if file_path:
                caption = message.caption if message.caption else ''
                if buttons_text:
                    caption += "\n\n" + buttons_text

                if reply_markup:
                    await client.send_video(TARGET_CHANNEL_ID, file_path, caption=caption, reply_markup=reply_markup)
                else:
                    await client.send_video(TARGET_CHANNEL_ID, file_path, caption=caption)

                # Удаляем временный файл
                os.remove(file_path)
                print("Видео переслано.")

        # Если это документ
        elif message.document:
            file_id = message.document.file_id
            file_path = await client.download_media(file_id)

            if file_path:
                caption = message.caption if message.caption else ''
                if buttons_text:
                    caption += "\n\n" + buttons_text

                if reply_markup:
                    await client.send_document(TARGET_CHANNEL_ID, file_path, caption=caption, reply_markup=reply_markup)
                else:
                    await client.send_document(TARGET_CHANNEL_ID, file_path, caption=caption)

                # Удаляем временный файл
                os.remove(file_path)
                print("Документ переслан.")

        else:
            print("Тип сообщения не поддерживается.")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    print("Бот запущен...")
    app.run()
