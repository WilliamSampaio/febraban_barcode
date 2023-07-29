def modulo10(sequencia) -> int:
    """
    O DAC (Dígito de Auto-Conferência) módulo 10, de um número é calculado
    multiplicando cada algarismo, pela seqüência de multiplicadores 2, 1, 2, 1, ...
    posicionados da direita para a esquerda.

    A soma dos algarismos do produto é dividida por 10 e o DAC será a diferença
    entre o divisor (10) e o resto da divisão:

        DAC = 10 - (resto da divisão)

    Observação: quando o resto da divisão for 0 (zero), o DAC calculado é o 0 (zero).

    EXEMPLO

    Calcular o DAC módulo 10 da seguinte seqüência de números: 01230067896.
    A fórmula do cálculo é:

        1. Multiplicação pela sequência 2, 1, 2, 1, ... da direita para a esquerda.
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


def digito_verificador_modulo10(campo1: str, campo2: str) -> str:
    return str(modulo10(campo1 + campo2))
