import re

from .constants import (
    MODULO10_QUANTIDADE_MOEDA,
    MODULO10_VALOR_EFETIVO,
    MODULO11_QUANTIDADE_MOEDA,
    MODULO11_VALOR_EFETIVO,
)
from .modulo10 import modulo10
from .modulo11 import modulo11


def dac_func(codigo_moeda):
    modulo = None
    if (
        int(codigo_moeda) == MODULO10_VALOR_EFETIVO
        or int(codigo_moeda) == MODULO10_QUANTIDADE_MOEDA
    ):
        modulo = modulo10
    elif (
        int(codigo_moeda) == MODULO11_VALOR_EFETIVO
        or int(codigo_moeda) == MODULO11_QUANTIDADE_MOEDA
    ):
        modulo = modulo11
    return modulo


def clear_barcode(barcode):
    return ''.join([i for i in re.findall(r'\d+', barcode)])
