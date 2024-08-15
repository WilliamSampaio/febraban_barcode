import pytest

from febraban_barcode import (
    decode_codigo_de_barras,
    gerar_numeracao_codigo_de_barras,
)
from febraban_barcode.constants import (
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


def test_decode_codigo_de_barras():
    codigo_de_barras = decode_codigo_de_barras(
        '84670000000109910422023123100000000000054321'
    )

    assert codigo_de_barras is None


def test_decode_codigo_de_barras_campo_as_dict_true():
    codigo_de_barras_dict = decode_codigo_de_barras(
        '84670000000109910422023123100000000000054321', True
    )

    assert isinstance(codigo_de_barras_dict, dict)


def test_numeracao_com_dac_tamanho_48():
    codigo_de_barras_dict = decode_codigo_de_barras(
        '84670000000 9   10991042202 0   31231000000 4   00000054321 5', True
    )

    assert isinstance(codigo_de_barras_dict, dict)


def test_numeracao_invalida():
    with pytest.raises(Exception):
        decode_codigo_de_barras(
            '84670000000 9   10991042202 0   31231000000 4   00000054321'
        )


def test_indentificacao_produto_invalido():
    with pytest.raises(Exception):
        decode_codigo_de_barras('04670000000109910422023123100000000000054321')


def test_segmento_invalido():
    with pytest.raises(Exception):
        decode_codigo_de_barras('80670000000109910422023123100000000000054321')


def test_segmentos_validos():
    for segmento in [
        SEGMENTO_PREFEITURA,
        SEGMENTO_SANEAMENTO,
        SEGMENTO_ENERGIA_ELETRICA_GAS,
        SEGMENTO_TELECOMUNICACOES,
        SEGMENTO_ORGAOS_GOVERNAMENTAIS,
        SEGMENTO_DEMAIS,
        SEGMENTO_MULTAS_TRANSITO,
        SEGMENTO_EXCLUSIVO_BANCO,
    ]:
        assert isinstance(
            decode_codigo_de_barras(
                f'8{str(segmento)}670000000109910422023123100000000000054321',
                True,
            ),
            dict,
        )


def test_valor_efetivo_ou_referencia_invalido():
    with pytest.raises(Exception):
        decode_codigo_de_barras('84070000000109910422023123100000000000054321')


def test_efetivo_ou_referencia_validos():
    for valor in [
        MODULO10_QUANTIDADE_MOEDA,
        MODULO10_VALOR_EFETIVO,
        MODULO11_QUANTIDADE_MOEDA,
        MODULO11_VALOR_EFETIVO,
    ]:
        assert isinstance(
            decode_codigo_de_barras(
                f'84{str(valor)}70000000109910422023123100000000000054321',
                True,
            ),
            dict,
        )


def test_data_vencimento_nao_informada():
    codigo_de_barras = gerar_numeracao_codigo_de_barras(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor=10.99,
        id_empresa_orgao='1042',
        vencimento=None,
        dados_campo_livre='54321',
    )
    result = decode_codigo_de_barras(codigo_de_barras, True)
    assert result['vencimento'] is None


def test_dac_invalido():
    codigo_de_barras_dict = decode_codigo_de_barras(
        '84670000000 9   10991042202 1   31231000000 4   00000054321 5', True
    )
    assert codigo_de_barras_dict['valido'] is False


def test_dac_invalido_com_campo_as_dict_false():
    codigo_de_barras_dict = decode_codigo_de_barras(
        '84670000000 9   10991042202 1   31231000000 4   00000054321 5'
    )
    assert codigo_de_barras_dict is None
