from datetime import date

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
    valor: float,
    id_empresa_orgao: str,
    dados_campo_livre: str = '',
    vencimento: date | None = None,
) -> str:
    """
    Identificação da Empresa/Órgão:
        4  posições: Código Febraban ou código de compensação
        8  posições: (Empresa/Órgão) CNPJ ou primeiras oito posições do cadastro geral de contribuintes do Ministério da Fazenda
    """
    if id_empresa_orgao is None or len(id_empresa_orgao) not in (4, 8):
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
    zeros_totais = (21 if len(id_empresa_orgao) == 8 else 25) - len(
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

    modulo = None
    if (
        codigo_moeda == MODULO10_VALOR_EFETIVO
        or codigo_moeda == MODULO10_QUANTIDADE_MOEDA
    ):
        modulo = modulo10
    elif (
        codigo_moeda == MODULO11_VALOR_EFETIVO
        or codigo_moeda == MODULO11_QUANTIDADE_MOEDA
    ):
        modulo = modulo11
    else:
        raise Exception('Código moeda inválido.')

    str_linha_digitavel = ''

    partes = [barcode[i : i + 11] for i in range(0, len(barcode), 11)]

    for parte in partes:
        str_linha_digitavel += parte + ' ' + str(modulo(parte)) + '   '

    return str_linha_digitavel.strip()


def decode_barcode(barcode: str) -> None:
    barcode_limpo = ''.join([i for i in barcode.split() if i.isdigit()])

    if barcode_limpo[0] == '8':
        print(f'Identificação do Produto: (8) Arrecadação.')
    else:
        raise Exception('Identificação do Produto inválido.')

    if barcode_limpo[1] == '1':
        print(f'Identificação do Segmento: (1) Prefeituras.')
    elif barcode_limpo[1] == '2':
        print(f'Identificação do Segmento: (2) Saneamento.')
    elif barcode_limpo[1] == '3':
        print(f'Identificação do Segmento: (3) Energia Elétrica e Gás.')
    elif barcode_limpo[1] == '4':
        print(f'Identificação do Segmento: (4) Telecomunicações.')
    elif barcode_limpo[1] == '5':
        print(f'Identificação do Segmento: (5) Órgãos Governamentais.')
    elif barcode_limpo[1] == '6':
        print(
            f'Identificação do Segmento: (6) Carnes e Assemelhados ou demais Empresas.'
        )
    elif barcode_limpo[1] == '7':
        print(f'Identificação do Segmento: (7) Multas de trânsito.')
    elif barcode_limpo[1] == '9':
        print(f'Identificação do Segmento: (9) Uso exclusivo do banco.')
    else:
        raise Exception('Identificação do Segmento inválido.')
