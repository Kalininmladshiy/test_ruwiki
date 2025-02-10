import os
from loguru import logger
from pathlib import Path

class WikiTextHandler:

    def __init__(self, filename: str = "wikipedia_page.wiki"):

        self.filename = filename
        self.output_dir = "wiki_pages"

    def save_to_file(self, wikitext: str, filename: str = None) -> None:
        filename = filename or self.filename

        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
                logger.info(f"Папка '{self.output_dir}' успешно создана.")
            except OSError as e:
                logger.error(f"Ошибка при создании папки '{self.output_dir}': {e}")
                return

        file_path = os.path.join(self.output_dir, filename)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(wikitext)
            logger.success(f"WikiText успешно сохранен в файл: {file_path}")
        except OSError as e:
            logger.error(f"Ошибка при сохранении в файл {file_path}: {e}")

    @staticmethod
    def process_file(file_path: str) -> list:
        """Обрабатывает список статей из файла."""
        path = Path(file_path)
        page_titles = []
        try:
            with path.open("r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    page_title = line.strip()

                    if not page_title:
                        logger.warning(f"Пустая строка в файле {file_path}, строка {line_number}, пропускаем...")
                        continue

                    logger.info(f"Обрабатываю страницу: {page_title}")
                    page_titles.append(page_title)

            if not page_titles:
                logger.warning(f"Файл {file_path} не содержит валидных названий страниц.")

        except FileNotFoundError:
            logger.error(f"Файл {file_path} не найден.")
        except OSError as e:
            logger.error(f"Ошибка при чтении файла {file_path}: {e}")

        return page_titles
