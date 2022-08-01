import datetime as dt
from io import BytesIO
from logging import Logger
import logging
from typing import Union, Optional, List

import phpserialize
import requests

from .models import ResultSuccess, ResultError
from .sms import SMS


SERVER_URL = "https://sms.phps.kr/lib/sendmms.sms"


class LMS:
    _name = "LMS"
    _server_url = SERVER_URL
    _print_debug_message: bool = False
    logger: Logger = logging.getLogger(__name__)

    @classmethod
    def set_print_debug_message(cls, is_print: bool):
        cls._print_debug_message = bool(is_print)

    @classmethod
    def _logging(cls, *args):
        if cls._print_debug_message:
            cls.logger.log(" ".join(args))
        else:
            cls.logger.debug(" ".join(args))

    @classmethod
    def view(cls, tr_id: str, tr_key: str) -> Union[ResultError, ResultSuccess]:
        data = {
            "adminuser": tr_id,
            "authkey": tr_key,
            "type": "view"
        }
        response = requests.post(cls._server_url, data)
        cls._logging(cls._name, "::view", response.status_code, response.text)
        result = phpserialize.loads(response.content, decode_strings=True)
        if "status" in result and result["status"] == "success":
            return ResultSuccess.create_result_success(result)
        return ResultError.create_result_error(result)

    @classmethod
    def cancel(cls, tr_id: str, tr_key: str, tr_num: int) -> Union[ResultError, ResultSuccess]:
        response = requests.post(cls._server_url, {
            "adminuser": tr_id,
            "authkey": tr_key,
            "tr_num": tr_num,
            "type": "cancel"
        })
        cls._logging(cls._name, "::cancel", response.status_code, response.text)
        result = phpserialize.loads(response.content, decode_strings=True)
        if "status" in result and result["status"] == "success":
            return ResultSuccess.create_result_success(result)
        return ResultError.create_result_error(result)

    @classmethod
    def send(cls, tr_id: str, tr_key: str, tr_from: str, tr_to: str, tr_txt_msg: str,
             tr_subject: Optional[str],
             tr_date: Optional[dt.datetime] = None,
             tr_comment: Optional[str] = None,
             files: List[BytesIO] = tuple()
             ) -> Union[ResultError, ResultSuccess]:
        response = requests.post(cls._server_url, {
            "adminuser": tr_id,
            "authkey": tr_key,
            "rphone": tr_from,
            "phone": tr_to,
            "subject": tr_subject.encode("euc-kr") if tr_subject else "",
            "sms": tr_txt_msg.encode("euc-kr"),
            "msg": tr_comment.encode("euc-kr") if tr_comment else "",
            "date": tr_date.strftime("%Y-%m-%d %H:%M:%S") if tr_date else 0,
        }, files={f"files[{i}]": f for i, f in zip(range(6), files)})
        cls._logging(cls._name, "::send", response.status_code, response.text)
        cls._logging({f"files[{i}]": f for i, f in zip(range(6), files)})
        result = phpserialize.loads(response.content, decode_strings=True)
        if "status" in result and result["status"] == "success":
            return ResultSuccess.create_result_success(result)
        return ResultError.create_result_error(result)
    pass
