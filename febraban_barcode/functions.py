import re

from .constants import (
    MODULO10_QUANTIDADE_MOEDA,
    MODULO10_VALOR_EFETIVO,
    MODULO11_QUANTIDADE_MOEDA,
    MODULO11_VALOR_EFETIVO,
)


def calc_dac_modulo10(sequencia: str) -> int:
    """
    O DAC (Dígito de Auto-Conferência) módulo 10, de um número é calculado
    multiplicando cada algarismo, pela seqüência de multiplicadores 2, 1,
    2, 1, ... posicionados da direita para a esquerda.

    A soma dos algarismos do produto é dividida por 10 e o DAC será a diferença
    entre o divisor (10) e o resto da divisão:

        DAC = 10 - (resto da divisão)

    Observação: quando o resto da divisão for 0 (zero), o DAC calculado é o
    0 (zero).

    EXEMPLO

    Calcular o DAC módulo 10 da seguinte seqüência de números: 01230067896.
    A fórmula do cálculo é:

        1. Multiplicação pela sequência 2, 1, 2, 1, ... da direita para a
        esquerda.
              0  1  2  3  0  0  6  7  8  9  6
            X 2  1  2  1  2  1  2  1  2  1  2
              0  1  4  3  0  0 12  7 16  9 12

        2. Soma dos dígitos do produto
            0 + 1 + 4 + 3 + 0 + 0 + 1 + 2 + 7 + 1 + 6 + 9 + 1 + 2 = 37
            Observação: Cada dígito deverá ser somado individualmente.

        3. Divisão do resultado da soma acima por 10
            37 : 10 = 3 , resto = 7
            DAC = 10 - (resto da divisão), portando 10 - 7 = 3

    O DAC da seqüência numérica é igual a “3”.
    """
    multiplicador_atual = 2
    soma = 0

    for element in sequencia[::-1]:
        resultado = int(element) * multiplicador_atual
        multiplicador_atual = 1 if multiplicador_atual == 2 else 2
        if resultado < 10:
            soma += resultado
        else:
            soma += int(resultado / 10)
            soma += resultado % 10

    resto_divisao = soma % 10
    if resto_divisao == 0:
        return resto_divisao
    return 10 - resto_divisao


def calc_dac_modulo11(sequencia) -> int:
    """
    O DAC (Dígito de Auto-Conferência) módulo 11, de um número é calculado
    multiplicando cada algarismo, pela seqüência de multiplicadores 2,3,4,5,6,
    7,8,9,2,3,4....
    posicionados da direita para a esquerda.

    A soma dos produtos dessa multiplicação é dividida por 11, obtém-se o
    resto da divisão, este resto deve ser subtraído de 11, o produto da
    subtração é o DAC.

    Observação: Quando o resto da divisão for igual a 0 ou 1, atribuí-se ao DV
    o digito “0”, e quando for 10, atribuí-se ao DV o digito “1”.

    EXEMPLO

    Calcular o DAC módulo 11 da seguinte seqüência de números: 01230067896.
    A fórmula do cálculo é:

        1. Multiplicação pela seqüência 2,3,4,5,6,7,8,9, 2,3,4 da direita
        para a esquerda.
              0  1  2  3  0  0  6  7  8  9  6
            X 4  3  2  9  8  7  6  5  4  3  2
              0  3  4 27  0  0 36 35 32 27 12

        2. Soma dos produtos da multiplicação:
            0 + 3 + 4 + 27 + 0 + 0 + 36 + 35 + 32 + 27 + 12 = 176

        3. Divisão do resultado da soma acima por 11
            176 : 11 = 16 , resto = 0

    O DAC da seqüência numérica é igual a “0”.
    """
    multiplicador_atual = 2
    soma = 0

    for element in sequencia[::-1]:
        resultado = int(element) * multiplicador_atual
        multiplicador_atual = (
            2 if multiplicador_atual == 9 else multiplicador_atual + 1
        )
        soma += resultado

    resto_divisao = soma % 11
    if resto_divisao in (0, 1):
        return 0
    if resto_divisao == 10:
        return 1
    return 11 - resto_divisao


def dac_func(codigo_moeda):
    modulo = None
    if (
        int(codigo_moeda) == MODULO10_VALOR_EFETIVO
        or int(codigo_moeda) == MODULO10_QUANTIDADE_MOEDA
    ):
        modulo = calc_dac_modulo10
    elif (
        int(codigo_moeda) == MODULO11_VALOR_EFETIVO
        or int(codigo_moeda) == MODULO11_QUANTIDADE_MOEDA
    ):
        modulo = calc_dac_modulo11
    return modulo


def limpar_codigo_de_barras(codigo_de_barras: str):
    return ''.join([i for i in re.findall(r'\d+', codigo_de_barras)])
