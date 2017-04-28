def comma_float(str: str):
    return float(str.replace(',', '.'))

def parse_percentage(str: str):
    return comma_float(str.replace('%', ''))