#!/usr/bin/env python3

import argparse
from wiki_client import WikiClient
from agent import DocumentSummarizer
from work_with_file import WikiTextHandler
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_gigachat.chat_models import GigaChat
from langchain.schema import Document

from loguru import logger
from environs import Env


def process_page(page_title: str, summarizer, wiki_client):
    """Обрабатывает одну статью Википедии."""
    wikitext_handler = WikiTextHandler(f"{page_title}.wiki")
    try:
        wikitext = wiki_client.get_page_text(page_title=page_title)
        docs = [Document(page_content=wikitext, metadata={"title": page_title})]

        result = summarizer.summarize(docs=docs)

        wikitext_handler.save_to_file(result.content)

    except Exception as e:
        logger.error(f"Ошибка при обработке {page_title}: {e}")


def main(page_title: str = None, file_path: str = None):
    """Основная функция для обработки WikiText и генерации краткого содержания."""
    env = Env()
    env.read_env()
    giga_chat_authorization_key = env("GIGA_CHAT_AUTHORIZATION_KEY", None)
    scope = env("SCOPE_GIGACHAIN", None)

    open_ai_key = env("OPENAI_API_KEY", None)

    model_llm = env('LLM_MODEL')

    wiki_client = WikiClient()

    model_maps = {
        'gigachat': GigaChat(
        credentials=giga_chat_authorization_key,
        scope=scope,
        model="GigaChat-Max",
        verify_ssl_certs=False,
    ),
        'qwen': ChatOllama(model="qwen2.5:14b", temperature=1),
        'openai': ChatOpenAI(model='gpt-4o', api_key=open_ai_key)
    }

    llm = model_maps.get(model_llm)
    summarizer = DocumentSummarizer(llm=llm)

    if file_path:
        page_titles = WikiTextHandler.process_file(file_path=file_path)
        for page_title in page_titles:
            process_page(page_title, summarizer, wiki_client)
    elif page_title:
        process_page(page_title, summarizer, wiki_client)
    else:
        logger.error("Необходимо указать либо название статьи, либо путь к файлу.")


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Получает и обрабатывает WikiText статьи.")
    parser.add_argument("page_title", nargs="?", type=str, help="Название страницы в Википедии")
    parser.add_argument("-f", "--file", type=str, help="Путь к файлу со списком страниц")
    args = parser.parse_args()

    main(page_title=args.page_title, file_path=args.file)
