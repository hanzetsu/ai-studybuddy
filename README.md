# AI StudyBuddy

Телеграм-бот на Python, использующий LangChain, GigaChat и OCR для подготовки студентов к сессии.

## Возможности
- Распознавание текста с изображений (pytesseract)
- Генерация ответов GigaChat через LangChain
- Объяснение простыми словами (кнопка 📘)
- Сохранение и просмотр билетов
- Режим тренировки (бот задаёт вопросы)

## Запуск
1. Склонируйте репозиторий или распакуйте архив.
2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # или venv\\Scripts\\activate на Windows
pip install -r requirements.txt
```
3. Установите Tesseract (если планируете использовать pytesseract):
- Ubuntu / Debian:
```bash
sudo apt update && sudo apt install -y tesseract-ocr libtesseract-dev
```
- Windows: скачайте установщик с https://github.com/tesseract-ocr/tesseract и установите, затем укажите путь в agents/ocr_agent.py при необходимости.
4. Создайте `.env` по образцу `.env.example` и заполните токены.
5. Запустите бота:
```bash
python main.py
```

## Примечания
- Не публикуйте `GIGACHAT_CLIENT_SECRET` в публичных репозиториях.
- В зависимости от версии LangChain и наличия нативной поддержки GigaChat, может потребоваться адаптация кода.
