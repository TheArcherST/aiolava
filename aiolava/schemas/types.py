import datetime
from typing import List

from .base import BaseLavaSchema


class BaseLavaType(BaseLavaSchema):
    pass


class Invoice(BaseLavaType):
    id: str
    amount: float
    expired: datetime.datetime
    status: int
    shop_id: str
    url: str
    comment: str = None
    fail_url: str = None
    success_url: str = None
    hook_url: str = None
    custom_fields: str = None
    merchantName: str = None
    exclude_service: List[str] = None
    include_service: List[str] = None


class CreateInvoiceResponse(BaseLavaType):
    data: Invoice
    status: int
    status_check: bool


class InvoiceStatus(BaseLavaType):
    status: str
    error_message: str = None
    id: str
    shop_id: str
    amount: float
    expire: datetime.datetime
    order_id: datetime.datetime
    fail_url: str = None
    success_url: str = None
    hook_url: str = None
    custom_fields: List[str] = None
    include_service: List[str] = None


class CheckInvoiceStatusResponse(BaseLavaType):
    data: InvoiceStatus
    status: int
    status_check: bool
