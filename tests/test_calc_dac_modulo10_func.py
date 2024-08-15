from febraban_barcode.functions import calc_dac_modulo10


def test_calculo_do_digito_de_auto_conferencia_modulo10():
    assert calc_dac_modulo10('01230067896') == 3
    assert calc_dac_modulo10('00000000000') == 0
