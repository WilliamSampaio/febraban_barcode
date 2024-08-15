from datetime import date

import pytest

from febraban_barcode import (
    MODULO10_VALOR_EFETIVO,
    MODULO11_QUANTIDADE_MOEDA,
    PRODUTO_ARRECADACAO,
    SEGMENTO_TELECOMUNICACOES,
    gerar_numeracao_codigo_de_barras,
)


def test_gerar_numeracao_codigo_de_barras():
    codigo_de_barras = gerar_numeracao_codigo_de_barras(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor=10.99,
        id_empresa_orgao='1042',
        vencimento=date(2023, 12, 31),
        dados_campo_livre='54321',
    )
    assert codigo_de_barras == '84670000000109910422023123100000000000054321'


def test_gerar_numeracao_codigo_de_barras_com_dac():
    codigo_de_barras = gerar_numeracao_codigo_de_barras(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor=10.99,
        id_empresa_orgao='1042',
        vencimento=date(2023, 12, 31),
        dados_campo_livre='54321',
        incluir_dac=True,
    )
    assert (
        codigo_de_barras
        == '84670000000 9   10991042202 0   31231000000 4   00000054321 5'
    )


def test_campo_id_empresa_orgao_invalido():
    with pytest.raises(Exception):
        gerar_numeracao_codigo_de_barras(
            produto=PRODUTO_ARRECADACAO,
            segmento=SEGMENTO_TELECOMUNICACOES,
            codigo_moeda=MODULO10_VALOR_EFETIVO,
            valor=10.99,
            id_empresa_orgao=None,
            vencimento=date(2023, 12, 31),
            dados_campo_livre='54321',
        )


def test_campo_vencimento_nao_informado():
    codigo_de_barras = gerar_numeracao_codigo_de_barras(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO10_VALOR_EFETIVO,
        valor=10.99,
        id_empresa_orgao='1042',
        dados_campo_livre='54321',
    )
    assert codigo_de_barras[19:27] == '00000000'


def test_campo_codigo_moeda_modulo11():
    codigo_de_barras = gerar_numeracao_codigo_de_barras(
        produto=PRODUTO_ARRECADACAO,
        segmento=SEGMENTO_TELECOMUNICACOES,
        codigo_moeda=MODULO11_QUANTIDADE_MOEDA,
        valor=1,
        id_empresa_orgao='1042',
        vencimento=date(2023, 12, 31),
        dados_campo_livre='54321',
    )
    assert codigo_de_barras == '84910000000010010422023123100000000000054321'


def test_campo_codigo_moeda_invalido():
    with pytest.raises(Exception):
        gerar_numeracao_codigo_de_barras(
            produto=PRODUTO_ARRECADACAO,
            segmento=SEGMENTO_TELECOMUNICACOES,
            codigo_moeda=None,
            valor=10.99,
            id_empresa_orgao='1042',
            vencimento=date(2023, 12, 31),
            dados_campo_livre='54321',
        )
