import base64
from datetime import date
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from barcode import ITF
from barcode.writer import ImageWriter, SVGWriter
from PIL import Image

PRODUTO_ARRECADACAO = 8

SEGMENTO_PREFEITURA = 1
SEGMENTO_SANEAMENTO = 2
SEGMENTO_ENERGIA_ELETRICA_GAS = 3
SEGMENTO_TELECOMUNICACOES = 4
SEGMENTO_ORGAOS_GOVERNAMENTAIS = 5
SEGMENTO_DEMAIS = 6
SEGMENTO_MULTAS_TRANSITO = 7
SEGMENTO_EXCLUSIVO_BANCO = 9

MODULO10_VALOR_EFETIVO = 6
MODULO10_QUANTIDADE_MOEDA = 7
MODULO11_VALOR_EFETIVO = 8
MODULO11_QUANTIDADE_MOEDA = 9


def linha_digitavel(barcode: str):
    if len(barcode) != 44:
        raise Exception('Código de barra inválido.')

    codigo_moeda = int(barcode[2])

    modulo = ''
    if (
        codigo_moeda == MODULO10_VALOR_EFETIVO
        or codigo_moeda == MODULO10_QUANTIDADE_MOEDA
    ):
        modulo = 10
    elif (
        codigo_moeda == MODULO11_VALOR_EFETIVO
        or codigo_moeda == MODULO11_QUANTIDADE_MOEDA
    ):
        modulo = 11
    else:
        raise Exception('Código moeda inválido.')

    str_linha_digitavel = ''

    partes = [barcode[i : i + 11] for i in range(0, len(barcode), 11)]

    for parte in partes:
        if modulo == 10:
            str_linha_digitavel += parte + ' ' + str(modulo10(parte)) + '   '
        else:
            str_linha_digitavel += parte + ' ' + str(modulo11(parte)) + '   '

    return str_linha_digitavel.strip()


def modulo10(sequencia):
    """
    O DAC (Dígito de Auto-Conferência) módulo 10, de um número é calculado
    multiplicando cada algarismo, pela seqüência de multiplicadores 2, 1, 2, 1, ...
    posicionados da direita para a esquerda.

    A soma dos algarismos do produto é dividida por 10 e o DAC será a diferença
    entre o divisor (10) e o resto da divisão:

        DAC = 10 - (resto da divisão)

    Observação: quando o resto da divisão for 0 (zero), o DAC calculado é o 0 (zero).

    EXEMPLO

    Calcular o DAC módulo 10 da seguinte seqüência de números: 01230067896.
    A fórmula do cálculo é:

        1. Multiplicação pela sequência 2, 1, 2, 1, ... da direita para a esquerda.
              0  1  2  3  0  0  6  7  8  9  6
            X 2  1  2  1  2  1  2  1  2  1  2
              0  1  4  3  0  0 12  7 16  9 12

        2. Soma dos dígitos do produto
            0 + 1 + 4 + 3 + 0 + 0 + 1 + 2 + 7 + 1 + 6 + 9 + 1 + 2 = 37
            Observação: Cada dígito deverá ser somado individualmente.

        3. Divisão do resultado da soma acima por 10
            37 : 10 = 3 , resto = 7
            DAC = 10 - (resto da divisão), portando 10 - 7 = 3

    O DAC da seqüência numérica é igual a “3”.
    """
    multiplicador_atual = 2
    soma = 0

    for element in sequencia[::-1]:
        resultado = int(element) * multiplicador_atual
        multiplicador_atual = 1 if multiplicador_atual == 2 else 2
        if resultado < 10:
            soma += resultado
        else:
            soma += int(resultado / 10)
            soma += resultado % 10

    resto_divisao = soma % 10
    if resto_divisao == 0:
        return resto_divisao
    return 10 - resto_divisao


def modulo11(sequencia):
    """
    O DAC (Dígito de Auto-Conferência) módulo 11, de um número é calculado multiplicando
    cada algarismo, pela seqüência de multiplicadores 2,3,4,5,6,7,8,9,2,3,4....
    posicionados da direita para a esquerda.

    A soma dos produtos dessa multiplicação é dividida por 11, obtém-se o resto da
    divisão, este resto deve ser subtraído de 11, o produto da subtração é o DAC.

    Observação: Quando o resto da divisão for igual a 0 ou 1, atribuí-se ao DV o
    digito “0”, e quando for 10, atribuí-se ao DV o digito “1”.

    EXEMPLO

    Calcular o DAC módulo 11 da seguinte seqüência de números: 01230067896.
    A fórmula do cálculo é:

        1. Multiplicação pela seqüência 2,3,4,5,6,7,8,9, 2,3,4 da direita
        para a esquerda.
              0  1  2  3  0  0  6  7  8  9  6
            X 4  3  2  9  8  7  6  5  4  3  2
              0  3  4 27  0  0 36 35 32 27 12

        2. Soma dos produtos da multiplicação:
            0 + 3 + 4 + 27 + 0 + 0 + 36 + 35 + 32 + 27 + 12 = 176

        3. Divisão do resultado da soma acima por 11
            176 : 11 = 16 , resto = 0

    O DAC da seqüência numérica é igual a “0”.
    """
    multiplicador_atual = 2
    soma = 0

    for element in sequencia[::-1]:
        resultado = int(element) * multiplicador_atual
        multiplicador_atual = (
            2 if multiplicador_atual == 9 else multiplicador_atual + 1
        )
        soma += resultado

    resto_divisao = soma % 11
    if resto_divisao in (0, 1):
        return 0
    if resto_divisao == 10:
        return 1
    return 11 - resto_divisao


def digito_verificador_modulo10(campo1: str, campo2: str):
    return str(modulo10(campo1 + campo2))


def digito_verificador_modulo11(campo1: str, campo2: str):
    return str(modulo11(campo1 + campo2))


def campo_livre(
    vencimento: date | None = None,
    dados_campo_livre: str = '',
    comprimento: int = 25,
):
    if vencimento is not None:
        str_vencimento = vencimento.strftime('%Y%m%d')
    else:
        str_vencimento = ''
    zeros_totais = comprimento - len(str_vencimento)
    return str_vencimento + dados_campo_livre.zfill(zeros_totais)


def barcode(
    produto: int,
    segmento: int,
    codigo_moeda: int,
    valor: Decimal,
    id_empresa_orgao: str,
    dados_campo_livre: str = '',
    vencimento: date | None = None,
):
    """
    Identificação da Empresa/Órgão:
        4  posições: Código Febraban ou código de compensação
        8  posições: As primeiras oito posições do cadastro geral de contribuintes do Ministério da Fazenda
        14 posições: CNPJ da Empresa/Órgão
    """
    if id_empresa_orgao is None or len(id_empresa_orgao) not in (4, 8, 14):
        raise Exception(
            'Identificação da Empresa/Órgão não informado ou inválido.'
        )

    numeracao = ''

    str_identificacao_produto = str(produto)
    str_identificacao_segmento = str(segmento)
    str_codigo_moeda = str(codigo_moeda)

    parte1 = (
        str_identificacao_produto
        + str_identificacao_segmento
        + str_codigo_moeda
    )

    str_valor = str(int(valor * 100)).zfill(11)

    """
    Se for utilizado o CNPJ para identificar a Empresa/Órgão, haverá uma
    redução no seu campo livre que passará a conter 21 posições.
    """
    str_campo_livre = campo_livre(
        vencimento=vencimento,
        dados_campo_livre=dados_campo_livre,
        comprimento=(21 if len(id_empresa_orgao) == 14 else 25),
    )

    parte2 = str_valor + id_empresa_orgao + str_campo_livre

    digito_verificador = ''

    if (
        codigo_moeda == MODULO10_VALOR_EFETIVO
        or codigo_moeda == MODULO10_QUANTIDADE_MOEDA
    ):
        digito_verificador = digito_verificador_modulo10(parte1, parte2)
    elif (
        codigo_moeda == MODULO11_VALOR_EFETIVO
        or codigo_moeda == MODULO11_QUANTIDADE_MOEDA
    ):
        digito_verificador = digito_verificador_modulo11(parte1, parte2)

    if digito_verificador == '':
        raise Exception('Dígito verificador inválido.')

    numeracao += parte1 + digito_verificador + parte2

    # print(len(numeracao))

    return numeracao


def image_png(
    filename: str | Path, barcode: str, linha_digitavel: str | None = None
):
    data = BytesIO()
    ITF(barcode, writer=ImageWriter()).write(
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
    filename: str | Path, barcode: str, linha_digitavel: str | None = None
):
    with open(filename, 'wb') as f:
        ITF(barcode, writer=SVGWriter()).write(
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


def base64_png(barcode: str, linha_digitavel: str | None = None):
    data = BytesIO()
    ITF(barcode, writer=ImageWriter()).write(
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
    bytes_values = data.getvalue()
    b64 = base64.b64encode(bytes_values).decode('utf-8')
    return 'data:image/png;charset=utf-8;base64,' + b64


def base64_svg(barcode: str, linha_digitavel: str | None = None):
    data = BytesIO()
    ITF(barcode, writer=SVGWriter()).write(
        data,
        options={
            'module_width': float(0.3),
            'module_height': float(20),
            'font_size': 23,
            'text_distance': float(8),
            'center_text': True,
        },
        text=linha_digitavel,
    )
    bytes_values = data.getvalue()
    b64 = base64.b64encode(bytes_values).decode('utf-8')
    return 'data:image/svg+xml;charset=utf-8;base64,' + b64


def html_base64_teste(filename: str | Path, base64: str):
    with open(filename, 'w') as f:
        f.write("<img src='{}'>".format(base64))


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

    # print(modulo10('01230067896')) # 3
    # print(modulo11('01230067896')) # 0

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
