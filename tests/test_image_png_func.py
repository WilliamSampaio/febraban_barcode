import os
import tempfile
from datetime import date

from febraban_barcode import calcular_dac, gerar_numeracao_codigo_de_barras
from febraban_barcode.constants import (
    MODULO10_VALOR_EFETIVO,
    PRODUTO_ARRECADACAO,
    SEGMENTO_TELECOMUNICACOES,
)
from febraban_barcode.image import image_png

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


def test_image_png():
    temp_filename = tempfile.NamedTemporaryFile(suffix='.png').name
    image_png(temp_filename, codigo_de_barras, codigo_de_barras_com_dac)
    exist = False
    exist = os.path.exists(temp_filename)
    os.remove(temp_filename)
    assert exist is True
