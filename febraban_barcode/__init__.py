from datetime import date
from decimal import Decimal

from febraban_barcode.modulo10 import digito_verificador_modulo10, modulo10
from febraban_barcode.modulo11 import digito_verificador_modulo11, modulo11

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


def barcode(
    produto: int,
    segmento: int,
    codigo_moeda: int,
    valor: Decimal,
    id_empresa_orgao: str,
    dados_campo_livre: str = '',
    vencimento: date | None = None,
) -> str:
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
    str_campo_livre = ''

    if vencimento is not None:
        str_vencimento = vencimento.strftime('%Y%m%d')
    else:
        str_vencimento = ''
    zeros_totais = (21 if len(id_empresa_orgao) == 14 else 25) - len(
        str_vencimento
    )

    str_campo_livre = str_vencimento + dados_campo_livre.zfill(zeros_totais)

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


def linha_digitavel(barcode: str) -> str:
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
