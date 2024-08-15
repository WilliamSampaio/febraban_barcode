from datetime import date, datetime

from febraban_barcode import functions as fn

from .constants import (
    MODULO10_QUANTIDADE_MOEDA,
    MODULO10_VALOR_EFETIVO,
    MODULO11_QUANTIDADE_MOEDA,
    MODULO11_VALOR_EFETIVO,
    PRODUTO_ARRECADACAO,
    SEGMENTO_DEMAIS,
    SEGMENTO_ENERGIA_ELETRICA_GAS,
    SEGMENTO_EXCLUSIVO_BANCO,
    SEGMENTO_MULTAS_TRANSITO,
    SEGMENTO_ORGAOS_GOVERNAMENTAIS,
    SEGMENTO_PREFEITURA,
    SEGMENTO_SANEAMENTO,
    SEGMENTO_TELECOMUNICACOES,
)


def gerar_numeracao_codigo_de_barras(
    produto: int,
    segmento: int,
    codigo_moeda: int,
    valor: float,
    id_empresa_orgao: str,
    dados_campo_livre: str = '',
    vencimento: date | None = None,
    incluir_dac: bool = False,
) -> str:
    """
    Identificação da Empresa/Órgão:
        4  posições: Código Febraban ou código de compensação
        8  posições: (Empresa/Órgão) CNPJ ou primeiras oito posições do
        cadastro geral de contribuintes do Ministério da Fazenda
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
        digito_verificador = fn.calc_dac_modulo10(str(parte1) + str(parte2))
    elif (
        codigo_moeda == MODULO11_VALOR_EFETIVO
        or codigo_moeda == MODULO11_QUANTIDADE_MOEDA
    ):
        digito_verificador = fn.calc_dac_modulo11(str(parte1) + str(parte2))

    if digito_verificador == '':
        raise Exception('Dígito verificador inválido.')

    numeracao += parte1 + str(digito_verificador) + parte2

    if incluir_dac is False:
        return numeracao

    return calcular_dac(numeracao)


def calcular_dac(codigo_de_barras: str) -> str:
    codigo_de_barras_limpo = fn.limpar_codigo_de_barras(codigo_de_barras)
    if len(codigo_de_barras_limpo) != 44:
        raise Exception('Código de barra inválido.')

    codigo_moeda = int(codigo_de_barras_limpo[2])
    modulo = fn.dac_func(codigo_moeda)
    if modulo is None:
        raise Exception('Código moeda inválido.')

    str_linha_digitavel = ''

    partes = [
        codigo_de_barras_limpo[i : i + 11]
        for i in range(0, len(codigo_de_barras_limpo), 11)
    ]

    for parte in partes:
        str_linha_digitavel += parte + ' ' + str(modulo(parte)) + '   '

    return str_linha_digitavel.strip()


def decode_codigo_de_barras(
    codigo_de_barras: str, as_dict: bool = False
) -> None | dict:
    codigo_de_barras_limpo = fn.limpar_codigo_de_barras(codigo_de_barras)

    dac_blocos = []

    if len(codigo_de_barras_limpo) == 48:
        codigo_de_barras_digitos = [i for i in codigo_de_barras_limpo]
        dac_blocos.append(codigo_de_barras_digitos.pop(47))
        dac_blocos.append(codigo_de_barras_digitos.pop(35))
        dac_blocos.append(codigo_de_barras_digitos.pop(23))
        dac_blocos.append(codigo_de_barras_digitos.pop(11))
        dac_blocos.reverse()
        codigo_de_barras_44 = ''.join(codigo_de_barras_digitos)
    elif len(codigo_de_barras_limpo) == 44:
        codigo_de_barras_44 = codigo_de_barras_limpo
    else:
        raise Exception('Código de Barras inválido.')

    modulo = fn.dac_func(codigo_de_barras_44[2])

    codigo_de_barras_dict = {
        'codigo_de_barras_44': codigo_de_barras_44,
        'codigo_de_barras_desc': codigo_de_barras_44,
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
        'identificador_empresa_orgao_desc': '',
        'vencimento': None,
        'vencimento_desc': '',
        'campo_livre': '',
        'campo_livre_desc': '',
        'valido': True,
        'erro': [],
    }

    codigo_de_barras_str = 'Código de Barras: '
    partes = [
        codigo_de_barras_44[i : i + 11]
        for i in range(0, len(codigo_de_barras_44), 11)
    ]
    for i in range(len(partes)):
        dac = ''
        if len(dac_blocos) > 0:
            dac = '-' + dac_blocos[i]
        codigo_de_barras_str += partes[i] + dac + ' '
    codigo_de_barras_dict['codigo_de_barras_desc'] = codigo_de_barras_str

    if int(codigo_de_barras_44[0]) == PRODUTO_ARRECADACAO:
        codigo_de_barras_dict['identificador_produto'] = codigo_de_barras_44[0]
        codigo_de_barras_dict[
            'identificador_produto_desc'
        ] = 'Identificação do Produto: (8) Arrecadação.'
    else:
        raise Exception('Identificação do Produto inválido.')

    if int(codigo_de_barras_44[1]) == SEGMENTO_PREFEITURA:
        codigo_de_barras_dict['identificador_segmento'] = codigo_de_barras_44[
            1
        ]
        codigo_de_barras_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (1) Prefeituras.'
    elif int(codigo_de_barras_44[1]) == SEGMENTO_SANEAMENTO:
        codigo_de_barras_dict['identificador_segmento'] = codigo_de_barras_44[
            1
        ]
        codigo_de_barras_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (2) Saneamento.'
    elif int(codigo_de_barras_44[1]) == SEGMENTO_ENERGIA_ELETRICA_GAS:
        codigo_de_barras_dict['identificador_segmento'] = codigo_de_barras_44[
            1
        ]
        codigo_de_barras_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (3) Energia Elétrica e Gás.'
    elif int(codigo_de_barras_44[1]) == SEGMENTO_TELECOMUNICACOES:
        codigo_de_barras_dict['identificador_segmento'] = codigo_de_barras_44[
            1
        ]
        codigo_de_barras_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (4) Telecomunicações.'
    elif int(codigo_de_barras_44[1]) == SEGMENTO_ORGAOS_GOVERNAMENTAIS:
        codigo_de_barras_dict['identificador_segmento'] = codigo_de_barras_44[
            1
        ]
        codigo_de_barras_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (5) Órgãos Governamentais.'
    elif int(codigo_de_barras_44[1]) == SEGMENTO_DEMAIS:
        codigo_de_barras_dict['identificador_segmento'] = codigo_de_barras_44[
            1
        ]
        codigo_de_barras_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (6) Carnes e Assemelhados ou demais Empresas.'
    elif int(codigo_de_barras_44[1]) == SEGMENTO_MULTAS_TRANSITO:
        codigo_de_barras_dict['identificador_segmento'] = codigo_de_barras_44[
            1
        ]
        codigo_de_barras_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (7) Multas de trânsito.'
    elif int(codigo_de_barras_44[1]) == SEGMENTO_EXCLUSIVO_BANCO:
        codigo_de_barras_dict['identificador_segmento'] = codigo_de_barras_44[
            1
        ]
        codigo_de_barras_dict[
            'identificador_segmento_desc'
        ] = 'Identificação do Segmento: (9) Uso exclusivo do banco.'
    else:
        raise Exception('Identificação do Segmento inválido.')

    if int(codigo_de_barras_44[2]) == MODULO10_VALOR_EFETIVO:
        codigo_de_barras_dict['identificador_valor_ref'] = codigo_de_barras_44[
            2
        ]
        codigo_de_barras_dict[
            'identificador_valor_ref_desc'
        ] = 'Identificador de Valor Efetivo ou Referência: (6) Valor a ser cobrado efetivamente em reais com dígito verificador calculado pelo módulo 10 na quarta posição do código de barras.'
    elif int(codigo_de_barras_44[2]) == MODULO10_QUANTIDADE_MOEDA:
        codigo_de_barras_dict['identificador_valor_ref'] = codigo_de_barras_44[
            2
        ]
        codigo_de_barras_dict[
            'identificador_valor_ref_desc'
        ] = 'Identificador de Valor Efetivo ou Referência: (7) Quantidade de moeda\n\tZeros – somente na impossibilidade de utilizar o valor;\n\tValor a ser reajustado por um índice\n\tcom dígito verificador calculado pelo módulo 10 na quarta posição do código de barras.'
    elif int(codigo_de_barras_44[2]) == MODULO11_VALOR_EFETIVO:
        codigo_de_barras_dict['identificador_valor_ref'] = codigo_de_barras_44[
            2
        ]
        codigo_de_barras_dict[
            'identificador_valor_ref_desc'
        ] = 'Identificador de Valor Efetivo ou Referência: (8) Valor a ser cobrado efetivamente em reais com dígito verificador calculado pelo módulo 11 na quarta posição do código de barras.'
    elif int(codigo_de_barras_44[2]) == MODULO11_QUANTIDADE_MOEDA:
        codigo_de_barras_dict['identificador_valor_ref'] = codigo_de_barras_44[
            2
        ]
        codigo_de_barras_dict[
            'identificador_valor_ref_desc'
        ] = 'Identificador de Valor Efetivo ou Referência: (9) Quantidade de moeda\n\tZeros – somente na impossibilidade de utilizar o valor; \n\tValor a ser reajustado por um índice\n\tcom dígito verificador calculado pelo módulo 11 na quarta posição do código de barras.'
    else:
        raise Exception(
            'Identificador de Valor Efetivo ou Referência inválido.'
        )

    digito_verificador_geral = codigo_de_barras_44[3]
    codigo_de_barras_dict['digito_verificador'] = digito_verificador_geral
    codigo_de_barras_dict['digito_verificador_desc'] = (
        'Dígito verificador geral (módulo 10 ou 11): '
        + digito_verificador_geral
    )

    dac = modulo(codigo_de_barras_44[0:3] + codigo_de_barras_44[4:44])
    if dac != int(digito_verificador_geral):
        codigo_de_barras_dict['erro'].append(
            'Erro: Dígito verificador geral inválido.'
        )
        codigo_de_barras_dict['valido'] = False

    valor_efetivo_ref = codigo_de_barras_44[4:15]

    if int(codigo_de_barras_44[2]) in (
        MODULO10_VALOR_EFETIVO,
        MODULO11_VALOR_EFETIVO,
    ):
        codigo_de_barras_dict['valor_efetivo_referencia'] = (
            float(valor_efetivo_ref) / 100
        )
        codigo_de_barras_dict[
            'valor_efetivo_referencia_desc'
        ] = 'Valor Efetivo: R$ ' + str(float(valor_efetivo_ref) / 100).replace(
            '.', ','
        )
    else:
        codigo_de_barras_dict['valor_efetivo_referencia'] = int(
            valor_efetivo_ref
        )
        codigo_de_barras_dict[
            'valor_efetivo_referencia_desc'
        ] = 'Valor Referência: ' + str(int(valor_efetivo_ref))

    identificador_empresa = codigo_de_barras_44[15:19]
    codigo_de_barras_dict[
        'identificador_empresa_orgao'
    ] = identificador_empresa

    if int(codigo_de_barras_44[1]) == SEGMENTO_EXCLUSIVO_BANCO:
        codigo_de_barras_dict['identificador_empresa_orgao_desc'] = (
            'Identificação da Empresa/Órgão: '
            + identificador_empresa
            + ' código de compensação.'
        )
    else:
        codigo_de_barras_dict['identificador_empresa_orgao_desc'] = (
            'Identificação da Empresa/Órgão: '
            + identificador_empresa
            + ' código de Febraban.'
        )

    campo_livre = codigo_de_barras_44[19:44]

    try:
        vencimento = datetime.strptime(campo_livre[0:8], '%Y%m%d')
        codigo_de_barras_dict['vencimento'] = vencimento.strftime('%Y-%m-%d')
        codigo_de_barras_dict[
            'vencimento_desc'
        ] = 'Data de Vencimento: ' + vencimento.strftime('%d/%m/%Y')
    except Exception:
        codigo_de_barras_dict[
            'vencimento_desc'
        ] = 'Data de Vencimento: Não informado.'

    codigo_de_barras_dict['campo_livre'] = campo_livre
    codigo_de_barras_dict['campo_livre_desc'] = (
        'Campo Livre (25 posições): ' + campo_livre
    )

    partes = [
        codigo_de_barras_44[i : i + 11]
        for i in range(0, len(codigo_de_barras_44), 11)
    ]

    if len(codigo_de_barras_limpo) == 48:
        for i in range(len(partes)):
            if modulo(partes[i]) != int(dac_blocos[i]):
                codigo_de_barras_dict['erro'].append(
                    'Erro: DAC (Dígito de Auto-Conferência) do bloco '
                    + str(i + 1)
                    + ' inválido.'
                )
                codigo_de_barras_dict['valido'] = False

    if as_dict:
        return {
            key: value
            for (key, value) in codigo_de_barras_dict.items()
            if '_desc' not in key
        }

    for key, desc in codigo_de_barras_dict.items():
        if '_desc' in key:
            print(desc)

    if not codigo_de_barras_dict['valido']:
        print('STATUS: Inválido.')
        for erro in codigo_de_barras_dict['erro']:
            print(' -> ' + erro)
    else:
        print('STATUS: Válido.')
