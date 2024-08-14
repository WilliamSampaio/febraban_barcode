from datetime import date

import pytest

from febraban_barcode import (
    MODULO10_VALOR_EFETIVO,
    MODULO11_QUANTIDADE_MOEDA,
    PRODUTO_ARRECADACAO,
    SEGMENTO_TELECOMUNICACOES,
    barcode,
)


def test_barcode():
    codigo_de_barras = barcode(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor=10.99,
        id_empresa_orgao='1042',
        vencimento=date(2023, 12, 31),
        dados_campo_livre='54321',
    )
    assert codigo_de_barras == '84670000000109910422023123100000000000054321'


def test_barcode_id_empresa_orgao_exception():
    with pytest.raises(Exception):
        barcode(
            produto=PRODUTO_ARRECADACAO,
            segmento=SEGMENTO_TELECOMUNICACOES,
            codigo_moeda=MODULO10_VALOR_EFETIVO,
            valor=10.99,
            id_empresa_orgao=None,
            vencimento=date(2023, 12, 31),
            dados_campo_livre='54321',
        )


def test_barcode_vencimento_is_none():
    codigo_de_barras = barcode(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor=10.99,
        id_empresa_orgao='1042',
        dados_campo_livre='54321',
    )
    assert codigo_de_barras[19:27] == '00000000'


def test_barcode_modulo_11():
    codigo_de_barras = barcode(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO11_QUANTIDADE_MOEDA,
        valor=1,
        id_empresa_orgao='1042',
        vencimento=date(2023, 12, 31),
        dados_campo_livre='54321',
    )
    assert codigo_de_barras == '84910000000010010422023123100000000000054321'


def test_barcode_digito_verificador_exception():
    with pytest.raises(Exception):
        barcode(
            produto=PRODUTO_ARRECADACAO,
            segmento=SEGMENTO_TELECOMUNICACOES,
            codigo_moeda=None,
            valor=10.99,
            id_empresa_orgao='1042',
            vencimento=date(2023, 12, 31),
            dados_campo_livre='54321',
        )
