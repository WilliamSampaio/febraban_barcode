import os
import tempfile
from datetime import date

from febraban_barcode import calcular_dac, gerar_numeracao_codigo_de_barras
from febraban_barcode.base64 import base64_png, html_base64_img
from febraban_barcode.constants import (
    MODULO10_VALOR_EFETIVO,
    PRODUTO_ARRECADACAO,
    SEGMENTO_TELECOMUNICACOES,
)

codigo_de_barras = gerar_numeracao_codigo_de_barras(
    produto=PRODUTO_ARRECADACAO,
    segmento=SEGMENTO_TELECOMUNICACOES,
    codigo_moeda=MODULO10_VALOR_EFETIVO,
    valor=10.99,
    id_empresa_orgao='1042',
    vencimento=date(2023, 12, 31),
    dados_campo_livre='54321',
)

codigo_de_barras_com_dac = calcular_dac(codigo_de_barras)


def test_html_base64_img():
    base64 = base64_png(codigo_de_barras, codigo_de_barras_com_dac)
    temp_filename = tempfile.NamedTemporaryFile().name
    html_base64_img(temp_filename, base64)
    contains = False
    with open(temp_filename) as f:
        if base64 in f.read():
            contains = True
    os.remove(temp_filename)
    assert contains is True
