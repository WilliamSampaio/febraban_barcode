from datetime import date

import pytest

from febraban_barcode import calcular_dac, gerar_numeracao_codigo_de_barras
from febraban_barcode.base64 import base64_svg
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


def test_base64_svg():
    base64 = base64_svg(codigo_de_barras, codigo_de_barras_com_dac)
    assert isinstance(base64, str)


def test_numeracao_codigo_de_barras_invalido():
    with pytest.raises(Exception):
        base64_svg('zzzzzz', codigo_de_barras_com_dac)
