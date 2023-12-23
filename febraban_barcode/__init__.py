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


def decode_barcode(barcode: str, as_dict: bool = False) -> None | dict:
    barcode_limpo = ''.join([i for i in barcode.split() if i.isdigit()])

    dac_blocos = []

    if len(barcode_limpo) == 48:
        barcode_digitos = [i for i in barcode_limpo]
        dac_blocos.append(barcode_digitos.pop(47))
        dac_blocos.append(barcode_digitos.pop(35))
        dac_blocos.append(barcode_digitos.pop(23))
        dac_blocos.append(barcode_digitos.pop(11))
        dac_blocos.reverse()
        barcode_44 = ''.join(barcode_digitos)
    elif len(barcode_limpo) == 44:
        barcode_44 = barcode_limpo
    else:
        raise Exception('Código de Barras inválido.')

    barcode_str = 'Código de Barras: '
    partes = [barcode_44[i : i + 11] for i in range(0, len(barcode_44), 11)]
    for i in range(len(partes)):
        dac = ''
        if len(dac_blocos) > 0:
            dac = '-' + dac_blocos[i]
        barcode_str += partes[i] + dac + ' '
    print(barcode_str)

    barcode_dict = {
        'identificador_produto': '',
        'identificador_produto_desc': '',
        'identificador_segmento': '',
        'identificador_segmento_desc': '',
        'identificador_valor_ref': '',
        'identificador_valor_ref_desc': '',
        'digito_verificador': '',
        'digito_verificador_desc': '',
        'valor_efetivo_referencia': '',
        'valor_efetivo_referencia_desc': '',
        'identificador_empresa_orgao': '',
        'vencimento': '',
        'campo_livre': '',
        'valido': False,
        'erro': '',
    }

    if int(barcode_44[0]) == PRODUTO_ARRECADACAO:
        barcode_dict['identificador_produto'] = barcode_44[0]
        barcode_dict[
            'identificador_produto_desc'
        ] = 'Identificação do Produto: (8) Arrecadação.'
    else:
        raise Exception('Identificação do Produto inválido.')

    if int(barcode_44[1]) == SEGMENTO_PREFEITURA:
        barcode_dict['identificador_segmento'] = barcode_44[1]
        barcode_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (1) Prefeituras.'
    elif int(barcode_44[1]) == SEGMENTO_SANEAMENTO:
        barcode_dict['identificador_segmento'] = barcode_44[1]
        barcode_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (2) Saneamento.'
    elif int(barcode_44[1]) == SEGMENTO_ENERGIA_ELETRICA_GAS:
        barcode_dict['identificador_segmento'] = barcode_44[1]
        barcode_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (3) Energia Elétrica e Gás.'
    elif int(barcode_44[1]) == SEGMENTO_TELECOMUNICACOES:
        barcode_dict['identificador_segmento'] = barcode_44[1]
        barcode_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (4) Telecomunicações.'
    elif int(barcode_44[1]) == SEGMENTO_ORGAOS_GOVERNAMENTAIS:
        barcode_dict['identificador_segmento'] = barcode_44[1]
        barcode_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (5) Órgãos Governamentais.'
    elif int(barcode_44[1]) == SEGMENTO_DEMAIS:
        barcode_dict['identificador_segmento'] = barcode_44[1]
        barcode_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (6) Carnes e Assemelhados ou demais Empresas.'
    elif int(barcode_44[1]) == SEGMENTO_MULTAS_TRANSITO:
        barcode_dict['identificador_segmento'] = barcode_44[1]
        barcode_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (7) Multas de trânsito.'
    elif int(barcode_44[1]) == SEGMENTO_EXCLUSIVO_BANCO:
        barcode_dict['identificador_segmento'] = barcode_44[1]
        barcode_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (9) Uso exclusivo do banco.'
    else:
        raise Exception('Identificação do Segmento inválido.')

    if int(barcode_44[2]) == MODULO10_VALOR_EFETIVO:
        barcode_dict['identificador_valor_ref'] = barcode_44[2]
        barcode_dict[
            'identificador_valor_ref_desc'
        ] = 'Identificador de Valor Efetivo ou Referência: (6) Valor a ser cobrado efetivamente em reais com dígito verificador calculado pelo módulo 10 na quarta posição do código de barras.'
    elif int(barcode_44[2]) == MODULO10_QUANTIDADE_MOEDA:
        barcode_dict['identificador_valor_ref'] = barcode_44[2]
        barcode_dict[
            'identificador_valor_ref_desc'
        ] = 'Identificador de Valor Efetivo ou Referência: (7) Quantidade de moeda\n\tZeros – somente na impossibilidade de utilizar o valor;\n\tValor a ser reajustado por um índice\n\tcom dígito verificador calculado pelo módulo 10 na quarta posição do código de barras.'
    elif int(barcode_44[2]) == MODULO11_VALOR_EFETIVO:
        barcode_dict['identificador_valor_ref'] = barcode_44[2]
        barcode_dict[
            'identificador_valor_ref_desc'
        ] = 'Identificador de Valor Efetivo ou Referência: (8) Valor a ser cobrado efetivamente em reais com dígito verificador calculado pelo módulo 11 na quarta posição do código de barras.'
    elif int(barcode_44[2]) == MODULO11_QUANTIDADE_MOEDA:
        barcode_dict['identificador_valor_ref'] = barcode_44[2]
        barcode_dict[
            'identificador_valor_ref_desc'
        ] = 'Identificador de Valor Efetivo ou Referência: (9) Quantidade de moeda\n\tZeros – somente na impossibilidade de utilizar o valor;\n\tValor a ser reajustado por um índice\n\tcom dígito verificador calculado pelo módulo 11 na quarta posição do código de barras.'
    else:
        raise Exception(
            'Identificador de Valor Efetivo ou Referência inválido.'
        )

    valor_efetivo_ref = barcode_44[4:15]

    if int(barcode_44[2]) in (MODULO10_VALOR_EFETIVO, MODULO11_VALOR_EFETIVO):
        barcode_dict['digito_verificador'] = float(valor_efetivo_ref) / 100
        barcode_dict['digito_verificador_desc'] = 'Valor Efetivo: R$ ' + str(
            float(valor_efetivo_ref) / 100
        ).replace('.', ',')
    else:
        barcode_dict['digito_verificador'] = int(valor_efetivo_ref)
        barcode_dict['digito_verificador_desc'] = 'Valor Referência: ' + str(
            int(valor_efetivo_ref)
        )

    if as_dict:
        return barcode_dict

    for key, desc in barcode_dict.items():
        if '_desc' in key:
            print(desc)
