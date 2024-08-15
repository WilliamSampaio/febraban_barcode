import pytest

from febraban_barcode import barcode, decode_barcode
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


def test_decode_barcode_as_dict_true():
    barcode_dict = decode_barcode(
        '84670000000109910422023123100000000000054321', True
    )

    assert isinstance(barcode_dict, dict)


def test_decode_barcode_as_dict_false():
    barcode = decode_barcode('84670000000109910422023123100000000000054321')

    assert barcode is None


def test_decode_barcode_as_dict_true_len_48():
    barcode_dict = decode_barcode(
        '84670000000 9   10991042202 0   31231000000 4   00000054321 5', True
    )

    assert isinstance(barcode_dict, dict)


def test_decode_barcode_invalid_barcode():
    with pytest.raises(Exception):
        decode_barcode(
            '84670000000 9   10991042202 0   31231000000 4   00000054321'
        )


def test_decode_barcode_indentificacao_produto_invalido():
    with pytest.raises(Exception):
        decode_barcode('04670000000109910422023123100000000000054321')


def test_decode_barcode_segmento_invalido():
    with pytest.raises(Exception):
        decode_barcode('80670000000109910422023123100000000000054321')


def test_decode_barcode_segmentos_validos():
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
            decode_barcode(
                f'8{str(segmento)}670000000109910422023123100000000000054321',
                True,
            ),
            dict,
        )


def test_decode_barcode_valor_efetivo_ou_referencia_invalido():
    with pytest.raises(Exception):
        decode_barcode('84070000000109910422023123100000000000054321')


def test_decode_barcode_valor_efetivo_ou_referencia_validos():
    for valor in [
        MODULO10_QUANTIDADE_MOEDA,
        MODULO10_VALOR_EFETIVO,
        MODULO11_QUANTIDADE_MOEDA,
        MODULO11_VALOR_EFETIVO,
    ]:
        assert isinstance(
            decode_barcode(
                f'84{str(valor)}70000000109910422023123100000000000054321',
                True,
            ),
            dict,
        )


def test_decode_barcode_data_vencimento_nao_informada():
    codigo_de_barras = barcode(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor=10.99,
        id_empresa_orgao='1042',
        vencimento=None,
        dados_campo_livre='54321',
    )
    result = decode_barcode(codigo_de_barras, True)
    assert result['vencimento'] is None


def test_decode_barcode_dac_invalido():
    barcode_dict = decode_barcode(
        '84670000000 9   10991042202 1   31231000000 4   00000054321 5', True
    )
    assert barcode_dict['valido'] is False


def test_decode_barcode_dac_invalido_as_dict_false():
    barcode_dict = decode_barcode(
        '84670000000 9   10991042202 1   31231000000 4   00000054321 5'
    )
    assert barcode_dict is None
