from fastapi import APIRouter
from pydantic import BaseModel
from escpos.printer import Network

router = APIRouter(prefix="/qrcode", tags=["qrcode"])


class QrCodeCreate(BaseModel):
    amount: int


@router.post("")
def print_qr_codes(body: QrCodeCreate):
    printer = Network("192.168.1.99", 9100)

    try:
        printer.hw("INIT")
        printer.set(align="center")

        for i in range(body.amount):
            printer.text(f"QR-code {i + 1}")
            printer.qr(f"code_{i}", size=8)
            printer.cut()

    finally:
        printer.close()

    return {"printed": body.amount}