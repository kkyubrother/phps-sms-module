import datetime as dt
from typing import Union, Optional

import phpserialize
import requests

from .models import ResultSuccess, ResultError


SERVER_URL = "https://sms.phps.kr/lib/send.sms"


class SMS:
    _name = "SMS"
    _server_url = SERVER_URL
    _print_debug_message: bool = False

    def __init__(self, tr_id: str, tr_key: str, tr_from: Optional[str]):
        self.tr_id = tr_id
        self.tr_key = tr_key
        self.tr_from = tr_from

    def set_tr_from(self, tr_from: str):
        self.tr_from = tr_from

    def send_msg(self, tr_to: str, tr_txt_msg: str, tr_date: Optional[dt.datetime], tr_comment: Optional[str]) -> Union[ResultError, ResultSuccess]:
        return self.send(self.tr_id, self.tr_key, self.tr_from, tr_to, tr_txt_msg, tr_date, tr_comment)

    def get_count(self) -> Union[ResultError, ResultSuccess]:
        return self.view(self.tr_id, self.tr_key)

    def cancel_msg(self, tr_num: int) -> Union[ResultError, ResultSuccess]:
        return self.cancel(self.tr_id, self.tr_key, tr_num)

    @classmethod
    def set_print_debug_message(cls, is_print: bool):
        cls._print_debug_message = bool(is_print)

    @classmethod
    def send(cls, tr_id: str, tr_key: str, tr_from: str, tr_to: str, tr_txt_msg: str, tr_date: Optional[dt.datetime] = None, tr_comment: Optional[str] = None) -> Union[ResultError, ResultSuccess]:
        response = requests.post(cls._server_url, {
            "adminuser": tr_id,
            "authkey": tr_key,
            "rphone": tr_from,
            "phone": tr_to,
            "sms": tr_txt_msg.encode("euc-kr"),
            "msg": tr_comment.encode("euc-kr") if tr_comment else "",
            "date": tr_date.strftime("%Y-%m-%d %H:%M:%S") if tr_date else 0
        })
        if cls._print_debug_message:
            print(cls._name, "::send", response.status_code, response.text)
        result = phpserialize.loads(response.content, decode_strings=True)
        if "status" in result and result["status"] == "success":
            return ResultSuccess(
                status=result["status"],
                current_count=int(result["curcount"]),
                phone_count=int(result["phonecount"]),
                send_count=int(result["sendcount"]),
                tr_num=int(result['tr_num']) if "tr_num" in result else None,
                delete_count=None,
            )
        return ResultError(
            status=int(result["status"]),
            message=result["message"]
        )

    @classmethod
    def view(cls, tr_id: str, tr_key: str) -> Union[ResultError, ResultSuccess]:
        response = requests.post(cls._server_url, {
            "adminuser": tr_id,
            "authkey": tr_key,
            "type": "view"
        })
        if cls._print_debug_message:
            print(cls._name, "::view", response.status_code, response.text)
        result = phpserialize.loads(response.content, decode_strings=True)
        if "status" in result and result["status"] == "success":
            return ResultSuccess(
                status=result["status"],
                current_count=int(result["curcount"]),
                send_count=None,
                phone_count=None,
                tr_num=None,
                delete_count=None,
            )
        return ResultError(
            status=int(result["status"]),
            message=result["message"]
        )

    @classmethod
    def cancel(cls, tr_id: str, tr_key: str, tr_num: int) -> Union[ResultError, ResultSuccess]:
        response = requests.post(cls._server_url, {
            "adminuser": tr_id,
            "authkey": tr_key,
            "tr_num": tr_num,
            "date": (dt.datetime.now() + dt.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        })
        if cls._print_debug_message:
            print(cls._name, "::cancel", response.status_code, response.text)
        result = phpserialize.loads(response.content, decode_strings=True)
        if "status" in result and result["status"] == "success":
            return ResultSuccess(
                status=result["status"],
                current_count=int(result["curcount"]),
                delete_count=int(result["deletecount"]),
                send_count=None,
                phone_count=None,
                tr_num=None
            )
        return ResultError(
            status=int(result["status"]),
            message=result["message"]
        )
    pass
