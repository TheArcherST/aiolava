from pydantic import root_validator

from .base import LavaEndpoint
from ..misc import HTTPMethod

from ..types.invoice_status import CheckInvoiceStatusResponse


class CheckInvoiceStatus(LavaEndpoint):
    __http_method__ = HTTPMethod.POST
    __endpoint__ = "/business/invoice/status"
    __returns__ = CheckInvoiceStatusResponse

    shopId: str
    orderId: str = None
    invoiceId: str = None

    @root_validator()
    def check_invoice_identify_possibility(cls, values):
        if values.get("orderId") is None and values.get("invoiceId") is None:
            raise ValueError("invoice can't be identified, nether of `orderId` nor `invoiceId` are specified")

        return values
