from datetime import date

import febraban_barcode as fb
from febraban_barcode.base64 import base64_png, base64_svg, html_base64_teste
from febraban_barcode.image import image_png, image_svg

if __name__ == '__main__':

    # Gera o código de barras
    codigo_de_barras = fb.barcode(
        produto=fb.PRODUTO_ARRECADACAO,
        segmento=fb.SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=fb.MODULO10_QUANTIDADE_MOEDA,
        valor=10.99,
        id_empresa_orgao='1042',
        vencimento=date(2023, 12, 31),
        dados_campo_livre='861500015',
    )
    print(codigo_de_barras)

    # Gera linha digitável
    txt_linha_digitavel = fb.linha_digitavel(codigo_de_barras)
    print(txt_linha_digitavel)

    # Decodifica o código de barras
    fb.decode_barcode(codigo_de_barras)

    # Calcula dígito módulo 10
    print(fb.modulo10('01230067896'))  # 3

    # Calcula dígito módulo 11
    print(fb.modulo11('01230067896'))  # 0

    # Gera o código de barras em PNG
    image_png(
        filename='barcode.png',
        barcode=codigo_de_barras,
        linha_digitavel=txt_linha_digitavel,
    )

    # Gera o código de barras em SVG
    image_svg(
        filename='barcode.svg',
        barcode=codigo_de_barras,
        linha_digitavel=txt_linha_digitavel,
    )

    # Gera o código de barras em base64 PNG para utilização em html
    html_base64_teste(
        'index1.html',
        base64_png(codigo_de_barras, linha_digitavel=txt_linha_digitavel),
    )

    # Gera o código de barras em base64 SVG para utilização em html
    html_base64_teste(
        'index2.html',
        base64_svg(codigo_de_barras, linha_digitavel=txt_linha_digitavel),
    )
