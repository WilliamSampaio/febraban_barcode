from febraban_barcode.modulo10 import digito_verificador_modulo10, modulo10


def test_modulo_10():
    assert modulo10('01230067896') == 3
    assert modulo10('00000000000') == 0


def test_digito_verificador_modulo10():
    assert digito_verificador_modulo10('11111111111', '11111111111') == '7'
