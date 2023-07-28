from datetime import date
from decimal import Decimal

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
    valor: str,
    id_empresa_orgao: str,
    vencimento: date,
    dados_campo_livre: str,
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

    numeracao += str_identificacao_produto
    numeracao += str_identificacao_segmento
    numeracao += str_codigo_moeda

    numeracao += '_'

    str_valor = str(int(Decimal(valor) * 100)).zfill(11)

    numeracao += str_valor

    numeracao += id_empresa_orgao

    """
    Se for utilizado o CNPJ para identificar a Empresa/Órgão, haverá uma
    redução no seu campo livre que passará a conter 21 posições.
    """
    str_campo_livre = campo_livre(
        vencimento=vencimento,
        dados_campo_livre=dados_campo_livre,
        comprimento=(21 if len(id_empresa_orgao) == 14 else 25),
    )

    numeracao += str_campo_livre

    print(len(numeracao))
    return numeracao


if __name__ == '__main__':

    result = barcode(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_PREFEITURA,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor='999.01',
        id_empresa_orgao='4321',
        vencimento=date(2023, 7, 30),
        dados_campo_livre='99999',
    )

    print(result)
