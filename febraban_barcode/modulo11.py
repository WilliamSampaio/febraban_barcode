def modulo11(sequencia) -> int:
    """
    O DAC (Dígito de Auto-Conferência) módulo 11, de um número é calculado multiplicando
    cada algarismo, pela seqüência de multiplicadores 2,3,4,5,6,7,8,9,2,3,4....
    posicionados da direita para a esquerda.

    A soma dos produtos dessa multiplicação é dividida por 11, obtém-se o resto da
    divisão, este resto deve ser subtraído de 11, o produto da subtração é o DAC.

    Observação: Quando o resto da divisão for igual a 0 ou 1, atribuí-se ao DV o
    digito “0”, e quando for 10, atribuí-se ao DV o digito “1”.

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


def digito_verificador_modulo11(campo1: str, campo2: str) -> str:
    return str(modulo11(campo1 + campo2))
