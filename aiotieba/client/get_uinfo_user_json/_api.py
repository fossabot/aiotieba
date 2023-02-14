import yarl

from .._core import HttpCore
from .._helper import pack_web_get_request, parse_json, send_request
from ..const import WEB_BASE_HOST
from ..exception import TiebaValueError
from ._classdef import UserInfo_json


def null_ret_factory() -> UserInfo_json:
    return UserInfo_json()


def parse_body(body: bytes) -> UserInfo_json:
    if not body:
        raise TiebaValueError("empty body")

    text = body.decode('utf-8', errors='ignore')
    res_json = parse_json(text)

    user_dict = res_json['creator']
    user = UserInfo_json(user_dict)

    return user


async def request(http_core: HttpCore, user_name: str) -> UserInfo_json:
    params = [
        ('un', user_name),
        ('ie', 'utf-8'),
    ]

    request = pack_web_get_request(
        http_core,
        yarl.URL.build(scheme="http", host=WEB_BASE_HOST, path="/i/sys/user_json"),
        params,
    )

    __log__ = "user_name={user_name}"  # noqa: F841

    body = await send_request(request, http_core.connector, read_bufsize=2 * 1024)
    return parse_body(body)
