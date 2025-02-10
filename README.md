# WikiText Summarizer

Этот проект позволяет загружать статьи из Википедии и преобразовывать их в краткое содержание с помощью языковых моделей.  

## Установка и запуск  

### 🔹 Требования  
- Python **3.10**  
- Git  
- Виртуальное окружение  

### 🔹 Установка  

1. **Клонировать репозиторий:**  
   ```bash
   git clone <URL_репозитория>
   cd <имя_папки_репозитория>

2. **Создать виртуальное окружение:** 
   ```bash
   python3 -m venv venv

3. **Активировать виртуальное окружение:** 
   ```bashsource venv/bin/activate
   source venv/bin/activate

4. **Установить зависимости:** 
   ```bashsource venv/bin/activate
   pip install -r requirements.txt

### 🔹 Настройка переменных окружения

1. **Создайте файл **`.env`** в корневой папке проекта и добавьте туда API-ключи:** 
   ```ini
    LLM_MODEL=openai  # Использовать OpenAI
    OPENAI_API_KEY=your_openai_api_key
    
    # (Дополнительно) Для GigaChat:
    GIGA_CHAT_AUTHORIZATION_KEY=your_gigachat_key
    SCOPE_GIGACHAIN=your_scope
    LLM_MODEL=gigachat
    
    # (Дополнительно) Для локальной модели Qwen:
    LLM_MODEL=qwen

### 🔹 Использование

1. **Обработка одной статьи:**
    ```bash
      ./main.py "Изотопы"


2. **Обработка списка статей из файла**
    ```bash
      ./main.py -f path/to/file.txt
   
Пример файла file.txt:
    Изотопы
    Вещественные числа
    Митоз

Скрипт обработает каждую статью и сохранит их в папке wiki_pages в корне проекта.




