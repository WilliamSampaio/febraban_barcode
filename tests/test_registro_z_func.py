import pytest

from febraban_barcode.retorno import registro_Z


def test_registro_z():
    assert isinstance(registro_Z(3, 999.99, ''), str)


def test_total_registros_valor_nao_e_int():
    with pytest.raises(Exception):
        registro_Z('3', 999.99, '')


def test_valor_total_registros_nao_e_float():
    with pytest.raises(Exception):
        registro_Z(3, '999.99', '')


def test_reservado_string_maior_que_126_caracteres():
    with pytest.raises(Exception):
        registro_Z(
            3,
            999.99,
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        )
