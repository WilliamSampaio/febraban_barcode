import os
import tempfile
from datetime import date

import pytest

from febraban_barcode import barcode, linha_digitavel
from febraban_barcode.base64 import base64_png, base64_svg, html_base64_teste
from febraban_barcode.constants import (
    MODULO10_VALOR_EFETIVO,
    PRODUTO_ARRECADACAO,
    SEGMENTO_TELECOMUNICACOES,
)

codigo_de_barras = barcode(
    produto=PRODUTO_ARRECADACAO,
    segmento=SEGMENTO_TELECOMUNICACOES,
    codigo_moeda=MODULO10_VALOR_EFETIVO,
    valor=10.99,
    id_empresa_orgao='1042',
    vencimento=date(2023, 12, 31),
    dados_campo_livre='54321',
)

txt_linha_digitavel = linha_digitavel(codigo_de_barras)


def test_base64_png():
    base64 = base64_png(codigo_de_barras, txt_linha_digitavel)
    assert isinstance(base64, str)


def test_base64_png_codigo_de_barras_invalido():
    with pytest.raises(Exception):
        base64_png('zzzzzz', txt_linha_digitavel)


def test_base64_svg():
    base64 = base64_svg(codigo_de_barras, txt_linha_digitavel)
    assert isinstance(base64, str)


def test_base64_svg_codigo_de_barras_invalido():
    with pytest.raises(Exception):
        base64_svg('zzzzzz', txt_linha_digitavel)


def test_html_base64_teste():
    base64 = base64_png(codigo_de_barras, txt_linha_digitavel)
    temp_filename = tempfile.NamedTemporaryFile().name
    html_base64_teste(temp_filename, base64)
    contains = False
    with open(temp_filename) as f:
        if base64 in f.read():
            contains = True
    os.remove(temp_filename)
    assert contains is True
