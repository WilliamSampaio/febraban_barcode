from datetime import date

from tinydb import TinyDB

from febraban_barcode import (
    calcular_dac,
    decode_codigo_de_barras,
    gerar_numeracao_codigo_de_barras,
)
from febraban_barcode.base64 import base64_png, base64_svg, html_base64_img
from febraban_barcode.constants import (
    MODULO10_VALOR_EFETIVO,
    PRODUTO_ARRECADACAO,
    SEGMENTO_TELECOMUNICACOES,
)
from febraban_barcode.functions import calc_dac_modulo10, calc_dac_modulo11
from febraban_barcode.image import image_png, image_svg

if __name__ == '__main__':

    # Gera o código de barras
    codigo_de_barras = gerar_numeracao_codigo_de_barras(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor=10.99,
        id_empresa_orgao='1042',
        vencimento=date(2023, 12, 31),
        dados_campo_livre='54321',
    )
    print(codigo_de_barras)

    # Gera linha digitável
    codigo_de_barras_com_dac = calcular_dac(codigo_de_barras)
    print(codigo_de_barras_com_dac)

    # Decodifica o código de barras
    decode_codigo_de_barras(codigo_de_barras)

    # Decodifica o código de barras e grava em um json
    db = TinyDB('db.json')
    db.insert(decode_codigo_de_barras(codigo_de_barras_com_dac, True))

    # Calcula o módulo 10 de 01230067896
    print(calc_dac_modulo10('01230067896'))  # 3

    # Calcula o módulo 11 de 01230067896
    print(calc_dac_modulo11('01230067896'))  # 0

    # Gera o código de barras em PNG
    image_png(
        filename='codigo_de_barras.png',
        codigo_de_barras=codigo_de_barras,
        linha_digitavel=codigo_de_barras_com_dac,
    )

    # Gera o código de barras em SVG
    image_svg(
        filename='codigo_de_barras.svg',
        codigo_de_barras=codigo_de_barras,
        linha_digitavel=codigo_de_barras_com_dac,
    )

    # Gera o código de barras em base64 PNG para utilização em html
    html_base64_img(
        'index1.html',
        base64_png(codigo_de_barras, linha_digitavel=codigo_de_barras_com_dac),
    )

    # Gera o código de barras em base64 SVG para utilização em html
    html_base64_img(
        'index2.html',
        base64_svg(codigo_de_barras, linha_digitavel=codigo_de_barras_com_dac),
    )
