import pytest

from febraban_barcode import calcular_dac


def test_calcular_digito_de_auto_conferencia_da_numeracao():
    result = calcular_dac('84670000000109910422023123100000000000054321')
    assert (
        result
        == '84670000000 9   10991042202 0   31231000000 4   00000054321 5'
    )


def test_numeracao_informada_invalida():
    with pytest.raises(Exception):
        calcular_dac('8467000000010991042202312310000000000005432')


def test_codigo_moeda_invalido():
    with pytest.raises(Exception):
        calcular_dac('84070000000109910422023123100000000000054321')
