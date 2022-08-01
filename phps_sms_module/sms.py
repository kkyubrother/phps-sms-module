import datetime as dt
import logging
from typing import Union, Optional

import phpserialize
import requests

from .models import ResultSuccess, ResultError
from .constants import SMS_SERVER_URL


class SMS_V2:
    __tr_id: str
    __tr_key: str
    __tr_from: str
    SERVER_URL: str = SMS_SERVER_URL

    def __init__(self, tr_id: str, tr_key: str, tr_from: str):
        """

        :param tr_id: 서비스를 이용하기 위한 SMS ID (신청시 등록한 계정ID)
        :param tr_key: SMS 서비스를 이용하기위한 인증키, [SMS호스팅관리]-[SMS접속정보]에서 확인가능
        :param tr_from: 메시지에 보낸사람으로 표시되는 번호(발신자 번호)
        """
        if not tr_id or not isinstance(tr_id, str):
            raise ValueError("bad_request.tr_id")

        elif not tr_key or not isinstance(tr_key, str):
            raise ValueError("bad_request.tr_key")

        elif not tr_from or not isinstance(tr_from, str):
            raise ValueError("bad_request.tr_from")

        self.__tr_id = tr_id
        self.__tr_key = tr_key
        self.__tr_from = tr_from

    @property
    def tr_id(self) -> str:
        return self.__tr_id

    @property
    def tr_key(self) -> str:
        return self.__tr_key

    @property
    def tr_from(self) -> str:
        return self.__tr_from

    @tr_from.setter
    def tr_from(self, tr_from: str):
        if not tr_from or not isinstance(tr_from, str):
            raise ValueError("bad_request.tr_from")
        self.__tr_from = tr_from

    def send(self, tr_to: str, tr_txt: str, tr_date: Optional[dt.datetime], tr_comment: Optional[str]):
        """

        :param tr_to: 메시지를 전송할 휴대폰 번호(수신자 번호)
        :param tr_txt: 전송할 메시지(메시지 최대 길이 : 90byte(SMS), 2,000byte(LMS))
        :param tr_date: 예약 발송을 위한 필드 (None : 즉시, 2011-06-16 20:26:23 : 해당시간에 발송)
        :param tr_comment: 메모필드이며 필수항목 아님
        :return:
        """
        if not tr_to or not isinstance(tr_to, str):
            raise ValueError("bad_request.tr_to")

        elif not tr_txt or not isinstance(tr_txt, str):
            raise ValueError("bad_request.tr_txt")

        if tr_date is None:
            tr_date = "0"

        elif not isinstance(tr_date, dt.datetime):
            raise ValueError("bad_request.tr_date")

        else:
            tr_date = tr_date.isoformat(sep=" ", timespec="seconds")

        if tr_comment is None:
            tr_comment = ""

        elif not isinstance(tr_comment, str):
            raise ValueError("bad_request.tr_comment")

        response = requests.post(self.SERVER_URL, {
            "adminuser": self.__tr_id,
            "authkey": self.__tr_key,
            "rphone": self.__tr_from,
            "phone": tr_to,
            "sms": tr_txt.encode("euc-kr"),
            "msg": tr_comment.encode("euc-kr") if tr_comment else "",
            "date": tr_date
        })


        pass

    def send_many(self):
        pass



SMS_V2()

SERVER_URL = "https://sms.phps.kr/lib/send.sms"


class SMS:
    _name = "SMS"
    _server_url = SERVER_URL
    _print_debug_message: bool = False
    logger: logging.Logger = logging.getLogger(__name__)

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
    def _logging(cls, *args):
        if cls._print_debug_message:
            cls.logger.log(" ".join(args))
        else:
            cls.logger.debug(" ".join(args))

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
        cls._logging(cls._name, "::send", response.status_code, response.text)
        result = phpserialize.loads(response.content, decode_strings=True)
        if "status" in result and result["status"] == "success":
            return ResultSuccess.create_result_success(result)
        return ResultError.create_result_error(result)

    @classmethod
    def view(cls, tr_id: str, tr_key: str) -> Union[ResultError, ResultSuccess]:
        response = requests.post(cls._server_url, {
            "adminuser": tr_id,
            "authkey": tr_key,
            "type": "view"
        })
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
            "date": (dt.datetime.now() + dt.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        })
        cls._logging(cls._name, "::cancel", response.status_code, response.text)
        result = phpserialize.loads(response.content, decode_strings=True)
        if "status" in result and result["status"] == "success":
            return ResultSuccess.create_result_success(result)
        return ResultError.create_result_error(result)
    pass
