import re


def is_valid_tracking_number(tracking_number: str) -> bool:

    if not re.fullmatch(r"[A-Z0-9]+", tracking_number):
        return False

    patterns = [
        r"^[A-Z]{2}\d{9}[A-Z]{2}$",         # Почта Китая, России, Казахстана
        r"^1Z[0-9A-Z]{16}$",                # UPS
        r"^TBA[0-9]{12,}$",                 # Amazon Logistics
        r"^[0-9]{26,40}$",                  # USPS длинные
        r"^YT[0-9]{16}$",                   # Yanwen
        r"^[0-9]{10,}$",                    # СДЭК, DPD, Pony
    ]
    return any(re.match(pattern, tracking_number.strip()) for pattern in patterns)
