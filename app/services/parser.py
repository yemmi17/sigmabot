import re
from decimal import Decimal, InvalidOperation

# Regex: allow decimals with dot, optional spaces around '/'
RE = re.compile(r'^\s*([0-9]+(?:\.[0-9]+)?)\s*/\s*([0-9]+(?:\.[0-9]+)?)\s*$')


def parse_caption(text: str):
    if text is None:
        raise ValueError("absent")
    m = RE.match(text)
    if not m:
        raise ValueError("format")
    try:
        income = Decimal(m.group(1))
        commission = Decimal(m.group(2))
    except InvalidOperation:
        raise ValueError("format")
    if income <= 0:
        raise ValueError("income_positive")
    if commission < 0:
        raise ValueError("commission_nonnegative")
    if commission > income:
        raise ValueError("commission_gt_income")
    return float(income), float(commission)
