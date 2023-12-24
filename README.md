# Febraban Barcode

[![Documentation
Status](https://readthedocs.org/projects/febraban-barcode/badge/?version=stable)](https://febraban-barcode.readthedocs.io/pt_BR/stable/?badge=stable)

Implementação em python do layout padrão de arrecadação/recebimento com utilização do código de barras da Febraban.

A arrecadação de tributos/taxas estaduais e municipais e contas de concessionárias de serviços públicos com código de barras segue as especificações técnicas definidas pela Febraban - Federação Brasileira de Bancos, atualmente na versão 6 do layout.

[Layout Padrão de Arrecadação/Recebimento com Utilização do Código de Barras](https://portal.febraban.org.br/pagina/3166/33/pt-br/layour-arrecadacao)

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

from febraban_barcode import barcode, decode_barcode, linha_digitavel
from febraban_barcode.base64 import base64_png, base64_svg, html_base64_teste
from febraban_barcode.constants import (
    MODULO10_VALOR_EFETIVO,
    PRODUTO_ARRECADACAO,
    SEGMENTO_TELECOMUNICACOES,
)
from febraban_barcode.image import image_png, image_svg
from febraban_barcode.modulo10 import modulo10
from febraban_barcode.modulo11 import modulo11

if __name__ == '__main__':

    # Gera o código de barras
    codigo_de_barras = barcode(
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
    txt_linha_digitavel = linha_digitavel(codigo_de_barras)
    print(txt_linha_digitavel)

    # Decodifica o código de barras
    decode_barcode(codigo_de_barras)

    # Decodifica o código de barras e grava em um json
    db = TinyDB('db.json')
    db.insert(decode_barcode(txt_linha_digitavel, True))

    # Calcula o módulo 10 de 01230067896
    print(modulo10('01230067896'))  # 3

    # Calcula o módulo 11 de 01230067896
    print(modulo11('01230067896'))  # 0

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

```
