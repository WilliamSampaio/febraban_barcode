from datetime import datetime


def registro_A(
    codigo_registro='A',
    codigo_remessa='2',
    codigo_convenio=' ',
    nome_empresa=' ',
    codigo_banco='0',
    nome_banco=' ',
    data_geracao='',
    nsa='0',
    versao_layout='05',
    servico='CODIGO DE BARRAS',
    reservado=' ',
):
    """
    REGISTRO “A” – HEADER

    Args:
        codigo_registro (str, optional): A.01 - Código do registro = “A”. Defaults to 'A'.
        codigo_remessa (str, optional): A.02 - Código de Remessa
            2 - RETORNO - Enviado pelo Banco para a Empresa/Órgão. Defaults to '2'.
        codigo_convenio (str, optional): A.03 - Código do Convênio
            Definido pelo banco. Defaults to ' '.
        nome_empresa (str, optional): A.04 - Nome da Empresa/Órgão. Defaults to ' '.
        codigo_banco (str, optional): A.05 - Código do Banco
            Código do Banco na câmara de compensação. Defaults to '0'.
        nome_banco (str, optional): A.06 - Nome do Banco. Defaults to ' '.
        data_geracao (str, optional): A.07 - Data da geração do arquivo (AAAAMMDD). Defaults to '0'.
        nsa (str, optional): A.08 - Número seqüencial do arquivo ( NSA )
            Este número deverá evoluir de 1 em 1 para cada arquivo gerado. Defaults to '0'.
        versao_layout (str, optional): A.09 - Versão do lay - out
            atual = versão 04
            nova = versão 05 - disponível a partir de 01.08.2016. Defaults to '05'.
        servico (str, optional): A.10 - Identificação do serviço
            Deverá conter “CÓDIGO DE BARRAS”. Defaults to 'CODIGO DE BARRAS'.
        reservado (str, optional): A.11 - Reservado para o futuro (filler). Defaults to ' '.

    Raises:
        Exception: Campo inválido.

    Returns:
        str: Retorna o header com 150bytes.
    """
    header_str = ''

    if len(codigo_registro) != 1:
        raise Exception('Campo A.01 Inválido. O campo deve ter o tamanho 1.')
    header_str += codigo_registro

    if len(codigo_remessa) != 1:
        raise Exception('Campo A.02 Inválido. O campo deve ter o tamanho 1.')
    if not codigo_remessa.isdigit():
        raise Exception('Campo A.02 Inválido. O campo deve ser numérico.')
    header_str += codigo_remessa

    if len(codigo_convenio) > 20:
        raise Exception(
            'Campo A.03 Inválido. O campo deve ter o tamanho máximo de 20.'
        )
    header_str += codigo_convenio.ljust(20)

    if len(nome_empresa) > 20:
        raise Exception(
            'Campo A.04 Inválido. O campo deve ter o tamanho máximo de 20.'
        )
    header_str += nome_empresa.ljust(20)

    if len(codigo_banco) > 3:
        raise Exception(
            'Campo A.05 Inválido. O campo deve ter o tamanho máximo de 3.'
        )
    if not codigo_banco.isdigit():
        raise Exception('Campo A.05 Inválido. O campo deve ser numérico.')
    header_str += codigo_banco.zfill(3)

    if len(nome_banco) > 20:
        raise Exception(
            'Campo A.06 Inválido. O campo deve ter o tamanho máximo de 20.'
        )
    header_str += nome_banco.upper().ljust(20)

    try:
        datetime.strptime(data_geracao, '%Y%m%d')
    except:
        raise Exception(
            'Campo A.07 Inválido. O campo deve ser uma data no formato AAAAMMDD.'
        )
    header_str += data_geracao

    if len(nsa) > 6:
        raise Exception(
            'Campo A.08 Inválido. O campo deve ter o tamanho máximo de 6.'
        )
    if not nsa.isdigit():
        raise Exception('Campo A.08 Inválido. O campo deve ser numérico.')
    header_str += nsa.zfill(6)

    if len(versao_layout) > 2:
        raise Exception(
            'Campo A.09 Inválido. O campo deve ter o tamanho máximo de 2.'
        )
    if not versao_layout.isdigit():
        raise Exception('Campo A.09 Inválido. O campo deve ser numérico.')
    header_str += versao_layout.zfill(2)

    if len(servico) > 17:
        raise Exception(
            'Campo A.10 Inválido. O campo deve ter o tamanho máximo de 17.'
        )
    header_str += servico.upper().ljust(17)

    if len(reservado) > 52:
        raise Exception(
            'Campo A.11 Inválido. O campo deve ter o tamanho máximo de 52.'
        )
    header_str += reservado.upper().ljust(52)
    return header_str
