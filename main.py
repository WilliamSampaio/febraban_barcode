from datetime import date
from decimal import Decimal

from febraban_barcode import (
    MODULO10_VALOR_EFETIVO,
    PRODUTO_ARRECADACAO,
    barcode,
    linha_digitavel,
    modulo10,
    modulo11,
)
from febraban_barcode.base64 import base64_png, base64_svg, html_base64_teste
from febraban_barcode.image import image_png, image_svg

if __name__ == '__main__':

    result = barcode(
        produto=PRODUTO_ARRECADACAO,
        segmento=0,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor=Decimal('0.01'),
        id_empresa_orgao='0973',
        vencimento=date(2023, 7, 29),
        dados_campo_livre='23300',
    )

    # print(modulo10('01230067896'))   # 3
    # print(modulo11('01230067896'))   # 0

    # print(result)
    # print(linha_digitavel(result))

    # image_png(
    #     filename='teste.png',
    #     barcode=result,
    #     linha_digitavel=linha_digitavel(result),
    # )

    # image_svg(
    #     filename='teste.svg',
    #     barcode=result,
    #     linha_digitavel=linha_digitavel(result),
    # )

    # html_base64_teste(
    #     'index1.html',
    #     base64_png(result, linha_digitavel=linha_digitavel(result)),
    # )

    # html_base64_teste(
    #     'index2.html',
    #     base64_svg(result, linha_digitavel=linha_digitavel(result)),
    # )
