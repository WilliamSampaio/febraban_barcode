from febraban_barcode.functions import calc_dac_modulo11


def test_calculo_do_digito_de_auto_conferencia_modulo11():
    assert calc_dac_modulo11('01230067896') == 0
    assert calc_dac_modulo11('01201611227') == 3
