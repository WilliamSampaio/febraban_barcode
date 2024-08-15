from io import BytesIO
from pathlib import Path

from barcode import ITF
from barcode.writer import ImageWriter, SVGWriter
from PIL import Image


def image_png(
    filename: str | Path,
    codigo_de_barras: str,
    linha_digitavel: str | None = None,
) -> None:
    data = BytesIO()
    ITF(codigo_de_barras, writer=ImageWriter()).write(
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
    image = Image.open(data)
    image.save(filename)


def image_svg(
    filename: str | Path,
    codigo_de_barras: str,
    linha_digitavel: str | None = None,
) -> None:
    with open(filename, 'wb') as f:
        ITF(codigo_de_barras, writer=SVGWriter()).write(
            f,
            options={
                'module_width': float(0.3),
                'module_height': float(20),
                'font_size': 23,
                'text_distance': float(8),
                'center_text': True,
            },
            text=linha_digitavel,
        )
