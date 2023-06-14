import json
from typing import List, Union, Generic, TypeVar, Type
import hmac
import hashlib
from aiohttp import ClientSession
from enum import Enum
from .types import CheckInvoiceStatusResponse, BaseLavaType, CreateInvoiceResponse
from .base import BaseLavaSchema


LTT = TypeVar("LTT", bound=BaseLavaType)


class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'


class BaseLavaRequest(BaseLavaSchema, Generic[LTT]):
    __returning__: Type[LTT] = ...
    __endpoint_url__: str = ...
    __generate_signature__: bool = True
    __http_method__: HTTPMethod = ...


class CreateInvoice(BaseLavaRequest):
    __returning__ = CreateInvoiceResponse
    __endpoint_url__ = "/business/invoice/create"
    __http_method__ = HTTPMethod.POST

    sum: float
    orderId: Union[str, int]
    shopId: str
    hookUrl: str = None
    failUrl: str = None
    successUrl: str = None
    expire: int = None
    customFields: str = None
    comment: str = None
    includeService: List[str] = None
    excludeService: List[str] = None


class CheckInvoiceStatus(BaseLavaRequest):
    __returning__ = CheckInvoiceStatusResponse
    __endpoint_url__ = "/business/invoice/status"
    __http_method__ = HTTPMethod.POST

    shopId: str
    orderId: str
    invoiceId: str
