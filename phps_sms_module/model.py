from typing import NamedTuple, Optional


class RequestSMSData(NamedTuple):
    """SMS 요청 데이터"""
    tel: str
    name1: Optional[str]
    name2: Optional[str]
    text: str


class RequestMMSData(RequestSMSData):
    """MMS 요청 데이터"""
    subject: Optional[str]

