from typing import NamedTuple, Optional


class ResultError(NamedTuple):
    status: int
    message: str


class ResultSuccess(NamedTuple):
    status: str
    current_count: int
    send_count: Optional[int]
    phone_count: Optional[int]
    tr_num: Optional[int]
    delete_count: Optional[int]
