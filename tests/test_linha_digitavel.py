import pytest

from febraban_barcode import linha_digitavel


def test_linha_digitavel():
    result = linha_digitavel('84670000000109910422023123100000000000054321')
    assert (
        result
        == '84670000000 9   10991042202 0   31231000000 4   00000054321 5'
    )


def test_linha_digitavel_len_not_equal_44():
    with pytest.raises(Exception):
        linha_digitavel('8467000000010991042202312310000000000005432')


def test_linha_digitavel_modulo_is_none():
    with pytest.raises(Exception):
        linha_digitavel('84070000000109910422023123100000000000054321')
