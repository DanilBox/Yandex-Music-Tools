import os
import sys
from functools import cache

from yandex_music import Client

from utils import hidden_prints


def new_client(token: str | None = None) -> Client:
    with hidden_prints() as _:
        return Client(token)


@cache
def null_client() -> Client:
    return new_client()


@cache
def base_client() -> Client:
    if (token := os.getenv("TOKEN")) is None:
        sys.exit("Не передан токен")

    client = new_client(token).init()

    if (status := client.account_status()) is None:
        sys.exit("Ошибка при получение аккаунта")

    if status.account.login is None:
        sys.exit("Ошибка при получение аккаунта")

    return client
