import json
from typing import List, Union
import hmac
import hashlib
from aiohttp import ClientSession

from .schemas.requests import (
    CreateInvoice, CheckInvoiceStatus, BaseLavaRequest,
    LTT, CreateInvoiceResponse, CheckInvoiceStatusResponse, HTTPMethod
)


class BusinessClient:
    def __init__(self,
                 private_key: str,
                 mics_key: str,
                 shop_id: str
                 ):

        self.private_key = private_key
        self.mics_key = mics_key
        self.shop_id = shop_id

    async def _execute_request(self, request: BaseLavaRequest[LTT]) -> LTT:
        data_dict = request.dict(exclude_none=True)
        data_bytes = json.dumps(data_dict).encode()

        signature = None
        if request.__generate_signature__:
            if self.private_key is None:
                raise ValueError("can't generate signature, because key is not provided")

            signature = (
                hmac
                .new(self.private_key.encode('UTF-8'), data_bytes, hashlib.sha256)
                .hexdigest()
            )

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Signature': signature,
        }
        http_method = request.__http_method__
        url = request.__endpoint_url__

        request_call_arguments = {
            "method": http_method.value,
            "url": url,
            "headers": headers,
        }

        if http_method is HTTPMethod.GET and data_bytes:
            raise RuntimeError("inconsistent request. data can only be provided with get request.")
        elif http_method is HTTPMethod.POST:
            request_call_arguments.update({"json": data_dict})
        else:
            raise KeyError(f"http method `{http_method}` not supports by lava client.")

        async with ClientSession(
                base_url='https://api.lava.ru',
        ) as cs:

            response = await cs.request(**request_call_arguments)
            data = await response.json()

        parsed_data = request.__returning__.parse_obj(data)
        return parsed_data

    async def create_invoice(
            self,
            sum_: float,
            order_id: Union[str, int],
            shop_id: str,
            hook_url: str = None,
            fail_url: str = None,
            success_url: str = None,
            expire: int = None,
            custom_fields: str = None,
            comment: str = None,
            include_service: List[str] = None,
            exclude_service: List[str] = None,
    ) -> CreateInvoiceResponse:
        request = CreateInvoice(
            sum=sum_,
            orderId=order_id,
            shopId=shop_id,
            hookUrl=hook_url,
            failUrl=fail_url,
            successUrl=success_url,
            expire=expire,
            customFields=custom_fields,
            comment=comment,
            includeService=include_service,
            excludeService=exclude_service,
        )
        return await self._execute_request(request)

    async def check_invoice_status(
            self,
            order_id: str,
            invoice_id: str
    ) -> CheckInvoiceStatusResponse:

        request = CheckInvoiceStatus(
            shopId=self.shop_id,
            orderId=order_id,
            invoiceId=invoice_id
        )
        return await self._execute_request(request)
