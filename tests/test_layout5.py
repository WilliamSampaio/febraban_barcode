import pytest

import febraban_barcode.retorno.layout5 as l5


def test_registro_a():
    assert isinstance(l5.registro_A(data_geracao='20240101'), str)


def test_registro_a_codigo_remessa_invalido_len_not_equal_1():
    with pytest.raises(Exception):
        l5.registro_A(data_geracao='20240101', codigo_remessa='')


def test_registro_a_codigo_remessa_invalido_is_not_digit():
    with pytest.raises(Exception):
        l5.registro_A(data_geracao='20240101', codigo_remessa='a')


def test_registro_a_codigo_convenio_len_more_than_20():
    with pytest.raises(Exception):
        l5.registro_A(
            data_geracao='20240101', codigo_convenio='123456789012345678901'
        )


def test_registro_a_nome_empresa_len_more_than_20():
    with pytest.raises(Exception):
        l5.registro_A(
            data_geracao='20240101', nome_empresa='EMPRESA DE TESTE - PYTHON'
        )


def test_registro_a_codigo_banco_tamanho_maior_que_3():
    with pytest.raises(Exception):
        l5.registro_A(data_geracao='20240101', codigo_banco='0001')


def test_registro_a_codigo_banco_nao_e_string_digitos():
    with pytest.raises(Exception):
        l5.registro_A(data_geracao='20240101', codigo_banco='A01')


def test_registro_a_nome_banco_len_more_than_20():
    with pytest.raises(Exception):
        l5.registro_A(
            data_geracao='20240101',
            nome_banco='EMPRESA DE TESTE - NOME BANCOS',
        )


def test_registro_a_data_geracao():
    with pytest.raises(Exception):
        l5.registro_A()


def test_registro_a_nsa_tamanho_maior_que_6():
    with pytest.raises(Exception):
        l5.registro_A(data_geracao='20240101', nsa='1234567')


def test_registro_a_nsa_nao_e_string_digitos():
    with pytest.raises(Exception):
        l5.registro_A(data_geracao='20240101', nsa='123 56')


def test_registro_a_versao_layout_tamanho_maior_que_2():
    with pytest.raises(Exception):
        l5.registro_A(data_geracao='20240101', versao_layout='123')


def test_registro_a_versao_layout_nao_e_string_digitos():
    with pytest.raises(Exception):
        l5.registro_A(data_geracao='20240101', versao_layout='9A')


def test_registro_a_servico_tamanho_maior_que_17():
    with pytest.raises(Exception):
        l5.registro_A(data_geracao='20240101', servico='                  ')


def test_registro_a_reservado_tamanho_maior_que_52():
    with pytest.raises(Exception):
        l5.registro_A(
            data_geracao='20240101',
            reservado='KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK',
        )
