import pytest

from febraban_barcode.retorno import registro_A


def test_registro_a():
    assert isinstance(registro_A(data_geracao='20240101'), str)


def test_codigo_remessa_invalido():
    with pytest.raises(Exception):
        registro_A(data_geracao='20240101', codigo_remessa='')
    with pytest.raises(Exception):
        registro_A(data_geracao='20240101', codigo_remessa='a')


def test_codigo_convenio_maior_que_20_caracteres():
    with pytest.raises(Exception):
        registro_A(
            data_geracao='20240101', codigo_convenio='123456789012345678901'
        )


def test_nome_empresa_maior_que_20_caracteres():
    with pytest.raises(Exception):
        registro_A(
            data_geracao='20240101', nome_empresa='EMPRESA DE TESTE - PYTHON'
        )


def test_codigo_banco_maior_que_3_caracteres():
    with pytest.raises(Exception):
        registro_A(data_geracao='20240101', codigo_banco='0001')


def test_codigo_banco_string_nao_numerica():
    with pytest.raises(Exception):
        registro_A(data_geracao='20240101', codigo_banco='A01')


def test_nome_banco_maior_que_20_caracteres():
    with pytest.raises(Exception):
        registro_A(
            data_geracao='20240101',
            nome_banco='EMPRESA DE TESTE - NOME BANCOS',
        )


def test_data_geracao_nao_informado():
    with pytest.raises(Exception):
        registro_A()


def test_nsa_tamanho_maior_que_6_caracteres():
    with pytest.raises(Exception):
        registro_A(data_geracao='20240101', nsa='1234567')


def test_nsa_string_nao_numerica():
    with pytest.raises(Exception):
        registro_A(data_geracao='20240101', nsa='123 56')


def test_versao_layout_maior_que_2_caracteres():
    with pytest.raises(Exception):
        registro_A(data_geracao='20240101', versao_layout='123')


def test_versao_layout_string_nao_numerica():
    with pytest.raises(Exception):
        registro_A(data_geracao='20240101', versao_layout='9A')


def test_servico_tamanho_maior_que_17_caracteres():
    with pytest.raises(Exception):
        registro_A(data_geracao='20240101', servico='                  ')


def test_reservado_tamanho_maior_que_52_caracteres():
    with pytest.raises(Exception):
        registro_A(
            data_geracao='20240101',
            reservado='KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK',
        )
