import base64
from io import BytesIO
from pathlib import Path

from barcode import ITF
from barcode.writer import ImageWriter, SVGWriter


def base64_png(barcode: str, linha_digitavel: str | None = None) -> str:
    data = BytesIO()
    ITF(barcode, writer=ImageWriter()).write(
        data,
        options={
            'module_width': float(0.3),
            'module_height': float(20),
            'font_size': 16,
            'text_distance': float(8),
            'center_text': True,
        },
        text=linha_digitavel,
    )
    bytes_values = data.getvalue()
    b64 = base64.b64encode(bytes_values).decode('utf-8')
    return 'data:image/png;charset=utf-8;base64,' + b64


def base64_svg(barcode: str, linha_digitavel: str | None = None) -> str:
    data = BytesIO()
    ITF(barcode, writer=SVGWriter()).write(
        data,
        options={
            'module_width': float(0.3),
            'module_height': float(20),
            'font_size': 23,
            'text_distance': float(8),
            'center_text': True,
        },
        text=linha_digitavel,
    )
    bytes_values = data.getvalue()
    b64 = base64.b64encode(bytes_values).decode('utf-8')
    return 'data:image/svg+xml;charset=utf-8;base64,' + b64


def html_base64_teste(filename: str | Path, base64: str) -> None:
    with open(filename, 'w') as f:
        f.write("<img src='{}'>".format(base64))
