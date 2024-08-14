from febraban_barcode.modulo11 import digito_verificador_modulo11, modulo11


def test_modulo_11():
    assert modulo11('01230067896') == 0
    assert modulo11('01201611227') == 3


def test_digito_verificador_modulo11():
    assert digito_verificador_modulo11('22222222222', '22222222222') == '1'
