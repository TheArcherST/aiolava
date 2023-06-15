from .base import LavaEndpoint
from ..misc import HTTPMethod

from ..types.invoice_status import CheckInvoiceStatusResponse


class CheckInvoiceStatus(LavaEndpoint):
    __http_method__ = HTTPMethod.POST
    __endpoint__ = "/business/invoice/status"
    __returns__ = CheckInvoiceStatusResponse

    shopId: str
    orderId: str
    invoiceId: str
