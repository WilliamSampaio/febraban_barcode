from datetime import datetime


def header(
    A01='A',
    A02='2',
    A03=' ',
    A04=' ',
    A05='0',
    A06=' ',
    A07='0',
    A08='0',
    A09='05',
    A10='CODIGO DE BARRAS',
    A11=' ',
):
    """
    REGISTRO “A” – HEADER

    Args:
        A01 (str, optional): Código do registro = “A”. Defaults to 'A'.
        A02 (str, optional): Código de Remessa
            2 - RETORNO - Enviado pelo Banco para a Empresa/Órgão. Defaults to '2'.
        A03 (str, optional): Código do Convênio
            Definido pelo banco. Defaults to ' '.
        A04 (str, optional): Nome da Empresa/Órgão. Defaults to ' '.
        A05 (str, optional): Código do Banco
            Código do Banco na câmara de compensação. Defaults to '0'.
        A06 (str, optional): Nome do Banco. Defaults to ' '.
        A07 (str, optional): Data da geração do arquivo (AAAAMMDD). Defaults to '0'.
        A08 (str, optional): Número seqüencial do arquivo ( NSA )
            Este número deverá evoluir de 1 em 1 para cada arquivo gerado. Defaults to '0'.
        A09 (str, optional): Versão do lay - out
            atual = versão 04
            nova = versão 05 - disponível a partir de 01.08.2016. Defaults to '05'.
        A10 (str, optional): Identificação do serviço
            Deverá conter “CÓDIGO DE BARRAS”. Defaults to 'CODIGO DE BARRAS'.
        A11 (str, optional): Reservado para o futuro (filler). Defaults to ' '.

    Raises:
        Exception: Campo inválido.

    Returns:
        str: Retorna o header com 150bytes.
    """
    header_str = ''

    if len(A01) != 1:
        raise Exception('Campo A.01 Inválido. O campo deve ter o tamanho 1.')
    header_str += A01

    if len(A02) != 1:
        raise Exception('Campo A.02 Inválido. O campo deve ter o tamanho 1.')
    if not A02.isdigit():
        raise Exception('Campo A.02 Inválido. O campo deve ser numérico.')
    header_str += A02

    if len(A03) > 20:
        raise Exception(
            'Campo A.03 Inválido. O campo deve ter o tamanho máximo de 20.'
        )
    header_str += A03.ljust(20)

    if len(A04) > 20:
        raise Exception(
            'Campo A.04 Inválido. O campo deve ter o tamanho máximo de 20.'
        )
    header_str += A04.ljust(20)

    if len(A05) > 3:
        raise Exception(
            'Campo A.05 Inválido. O campo deve ter o tamanho máximo de 3.'
        )
    if not A05.isdigit():
        raise Exception('Campo A.05 Inválido. O campo deve ser numérico.')
    header_str += A05.zfill(3)

    if len(A06) > 20:
        raise Exception(
            'Campo A.06 Inválido. O campo deve ter o tamanho máximo de 20.'
        )
    header_str += A06.upper().ljust(20)

    try:
        datetime.strptime(A07, '%Y%m%d')
    except:
        raise Exception(
            'Campo A.07 Inválido. O deve ser uma data no formato AAAAMMDD.'
        )
    header_str += A07

    if len(A08) > 6:
        raise Exception(
            'Campo A.08 Inválido. O campo deve ter o tamanho máximo de 6.'
        )
    if not A08.isdigit():
        raise Exception('Campo A.08 Inválido. O campo deve ser numérico.')
    header_str += A08.zfill(6)

    if len(A09) > 2:
        raise Exception(
            'Campo A.09 Inválido. O campo deve ter o tamanho máximo de 2.'
        )
    if not A09.isdigit():
        raise Exception('Campo A.09 Inválido. O campo deve ser numérico.')
    header_str += A09.zfill(2)

    if len(A10) > 17:
        raise Exception(
            'Campo A.10 Inválido. O campo deve ter o tamanho máximo de 17.'
        )
    header_str += A10.upper().ljust(17)

    if len(A11) > 52:
        raise Exception(
            'Campo A.11 Inválido. O campo deve ter o tamanho máximo de 52.'
        )
    header_str += A11.upper().ljust(52)
    return header_str
