import os
from functools import cache

from yandex_music import Client


@cache
def null_client() -> Client:
    return Client()


@cache
def base_client() -> Client:
    if (token := os.getenv("TOKEN")) is None:
        exit("Не передан токен")

    client = Client(token).init()

    if (status := client.account_status()) is None:
        exit("Ошибка при получение аккаунта")

    if status.account.login is None:
        exit("Ошибка при получение аккаунта")

    return client
