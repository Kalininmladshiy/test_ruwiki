import mwclient
import time
from loguru import logger

class WikiClient:
    def __init__(self, site_url='ru.ruwiki.ru', max_retries=3, retry_delay=5):

        self.site_url = site_url
        self.site = None
        attempts = 0

        while attempts < max_retries:
            try:
                self.site = mwclient.Site(self.site_url)
                logger.success(f"Успешное подключение к {self.site_url}")
                break
            except Exception as e:
                attempts += 1
                logger.error(f"Ошибка подключения к {self.site_url}: {e}")
                if attempts < max_retries:
                    logger.info(f"Повторная попытка через {retry_delay} секунд... ({attempts}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    raise Exception(f"Не удалось подключиться к {self.site_url} после {max_retries} попыток.")

    def get_page_text(self, page_title):
        """
        Получает вики-текст статьи по её названию.
        :param page_title: Название статьи
        :return: Вики-текст статьи
        """
        try:
            page = self.site.pages[page_title]
            wikitext = page.text()
            return wikitext
        except mwclient.errors.InvalidPageTitle:
            raise Exception(f"Некорректное название страницы: {page_title}")
        except mwclient.errors.APIError as e:
            raise Exception(f"Ошибка API при получении страницы {page_title}: {e}")
        except Exception as e:
            raise Exception(f"Ошибка при получении текста страницы {page_title}: {e}")