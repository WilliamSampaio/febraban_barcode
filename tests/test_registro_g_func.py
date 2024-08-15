from datetime import date

import pytest

from febraban_barcode import constants as c
from febraban_barcode import gerar_numeracao_codigo_de_barras
from febraban_barcode.retorno import registro_G

codigo_de_barras = gerar_numeracao_codigo_de_barras(
    produto=c.PRODUTO_ARRECADACAO,
    segmento=c.SEGMENTO_TELECOMUNICACOES,
    codigo_moeda=c.MODULO10_VALOR_EFETIVO,
    valor=10.99,
    id_empresa_orgao='1042',
    vencimento=date(2023, 12, 31),
    dados_campo_livre='54321',
)


def test_registro_z():
    assert isinstance(
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        ),
        str,
    )


def test_codigo_banco_invalido():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='0001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='0 1',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_agencia_string_nao_numerica():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1A34',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_conta_string_nao_numerica():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='1B345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_conta_digito_string_nao_numerica():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='C',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_agencia_conta_e_conta_digito_maior_que_17_caracteres():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='12345678',
            conta='123456789',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_data_pagamento_invalida():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento=None,
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_data_credito_invalida():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito=None,
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_codigo_de_barras_invalida():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras + '0',
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_valor_recebido_invalida():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido='99.99',
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_valor_tarifa_invalida():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa='0.01',
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_nsr_invalida():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr='999',
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_codigo_agencia_invalida():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='123456789',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_forma_arrecadacao_maior_que_1_caracteres():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao='99',
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_forma_arrecadacao_desconhecida():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao='z',
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_autenticacao_maior_que_23_caracteres():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='AAAAAAAAAAAAAAAAAAAAAAAA',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='',
        )


def test_forma_pagamento_maior_que_1_caracteres():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento='99',
            reservado='',
        )


def test_forma_pagamento_string_nao_numerica():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento='B',
            reservado='',
        )


def test_reservado_maior_que_9_caracteres():
    with pytest.raises(Exception):
        registro_G(
            codigo_banco='001',
            agencia='1234',
            conta='12345',
            conta_digito='6',
            data_pagamento='20240101',
            data_credito='20240102',
            codigo_de_barras_44=codigo_de_barras,
            valor_recebido=99.99,
            valor_tarifa=0.01,
            nsr=999,
            codigo_agencia='',
            forma_arrecadacao=c.ARRECADACAO_INTERNET_COM_FATURA,
            autenticacao='',
            forma_pagamento=c.PAGAMENTO_DINHEIRO,
            reservado='AAAAAAAAAA',
        )
