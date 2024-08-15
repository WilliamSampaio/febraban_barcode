# Febraban Barcode

[![Documentation Status](https://readthedocs.org/projects/febraban-barcode/badge/?version=stable&style=flat-square)](https://febraban-barcode.readthedocs.io/pt_BR/stable/?badge=stable)
![Codecov](https://img.shields.io/codecov/c/github/WilliamSampaio/febraban_barcode?style=flat-square&logo=codecov&labelColor=white)
![PyPI - Version](https://img.shields.io/pypi/v/febraban_barcode?logo=semver&style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/febraban_barcode?logo=python&logoColor=yellow&labelColor=blue&color=yellow&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/febraban_barcode?logo=pypi&logoColor=gold&style=flat-square)
![GitHub License](https://img.shields.io/github/license/WilliamSampaio/febraban_barcode?logo=github&style=flat-square)

Implementação em python do layout padrão de arrecadação/recebimento com utilização do código de barras da Febraban.

A arrecadação de tributos/taxas estaduais e municipais e contas de concessionárias de serviços públicos com código de barras segue as especificações técnicas definidas pela Febraban - Federação Brasileira de Bancos, atualmente na versão 7 do layout.

[Layout Padrão de Arrecadação/Recebimento com Utilização do Código de Barras - versão 7](https://portal.febraban.org.br/pagina/3327/33/pt-br/layout-codigo-barras)

Com este pacote é possível:

* Gerar a numeração do código de barras
* Gerar a linha digitável com os dígitos verificadores de cada bloco
* Calcular os dígitos verificadores módulo 10
* Calcular os dígitos verificadores módulo 11
* Gerar imagem do código de barras em PNG
* Gerar imagem do código de barras em SVG
* Gerar imagem em base64 PNG para uso em HTML
* Gerar imagem em base64 SVG para uso em HTML

## Instalação

```bash
pip install febraban_barcode
```

## Utilização

```python
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

```
