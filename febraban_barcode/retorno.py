from datetime import datetime

from febraban_barcode import constants as c


def registro_A(
    codigo_remessa='2',
    codigo_convenio=' ',
    nome_empresa=' ',
    codigo_banco='0',
    nome_banco=' ',
    data_geracao='',
    nsa='0',
    versao_layout='05',
    servico='CODIGO DE BARRAS',
    reservado='',
):
    """
    REGISTRO “A” – HEADER

    Args:
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
    registro_a = 'A'

    if len(codigo_remessa) != 1:
        raise Exception('Campo A.02 Inválido. O campo deve ter o tamanho 1.')
    if not codigo_remessa.isdigit():
        raise Exception('Campo A.02 Inválido. O campo deve ser numérico.')
    registro_a += codigo_remessa

    if len(codigo_convenio) > 20:
        raise Exception(
            'Campo A.03 Inválido. O campo deve ter o tamanho máximo de 20.'
        )
    registro_a += codigo_convenio.ljust(20)

    if len(nome_empresa) > 20:
        raise Exception(
            'Campo A.04 Inválido. O campo deve ter o tamanho máximo de 20.'
        )
    registro_a += nome_empresa.ljust(20)

    if len(codigo_banco) > 3:
        raise Exception(
            'Campo A.05 Inválido. O campo deve ter o tamanho máximo de 3.'
        )
    if not codigo_banco.isdigit():
        raise Exception('Campo A.05 Inválido. O campo deve ser numérico.')
    registro_a += codigo_banco.zfill(3)

    if len(nome_banco) > 20:
        raise Exception(
            'Campo A.06 Inválido. O campo deve ter o tamanho máximo de 20.'
        )
    registro_a += nome_banco.upper().ljust(20)

    try:
        datetime.strptime(data_geracao, '%Y%m%d')
    except:
        raise Exception(
            'Campo A.07 Inválido. O campo deve ser uma data no formato AAAAMMDD.'
        )
    registro_a += data_geracao

    if len(nsa) > 6:
        raise Exception(
            'Campo A.08 Inválido. O campo deve ter o tamanho máximo de 6.'
        )
    if not nsa.isdigit():
        raise Exception('Campo A.08 Inválido. O campo deve ser numérico.')
    registro_a += nsa.zfill(6)

    if len(versao_layout) > 2:
        raise Exception(
            'Campo A.09 Inválido. O campo deve ter o tamanho máximo de 2.'
        )
    if not versao_layout.isdigit():
        raise Exception('Campo A.09 Inválido. O campo deve ser numérico.')
    registro_a += versao_layout.zfill(2)

    if len(servico) > 17:
        raise Exception(
            'Campo A.10 Inválido. O campo deve ter o tamanho máximo de 17.'
        )
    registro_a += servico.upper().ljust(17)

    if len(reservado) > 52:
        raise Exception(
            'Campo A.11 Inválido. O campo deve ter o tamanho máximo de 52.'
        )
    registro_a += reservado.upper().ljust(52)
    return registro_a


def registro_G(
    codigo_banco='0',
    agencia='0',
    conta='0',
    conta_digito='0',
    data_pagamento='',
    data_credito='',
    codigo_de_barras_44=' ',
    valor_recebido=0.0,
    valor_tarifa=0.0,
    nsr=None,
    codigo_agencia=' ',
    forma_arrecadacao=' ',
    autenticacao=' ',
    forma_pagamento='0',
    reservado='',
):
    """
    REGISTRO “G” – RETORNO DAS ARRECADAÇÕES IDENTIFICADAS COM CÓDIGO DE BARRAS

    Args:
        codigo_banco (str, optional): G.02 - Identificação do banco da empresa/órgão creditada. Defaults to '0'.
        agencia (str, optional): G.02 - Identificação da agência da empresa/órgão creditada. Defaults to '0'.
        conta (str, optional): G.02 - Identificação da conta da empresa/órgão creditada. Defaults to '0'.
        conta_digito (str, optional): G.02 - Identificação do dígito da conta da empresa/órgão creditada. Defaults to '0'.
        data_pagamento (str, optional): G.03 - Data de pagamento (AAAA/MM/DD). Defaults to ''.
        data_credito (str, optional): G.04 - Data de crédito (AAAA/MM/DD). Defaults to ''.
        codigo_de_barras_44 (str, optional): G.05 - Código de Barras (44 posições). Defaults to ' '.
        valor_recebido (float, optional): G.06 - Valor recebido. Defaults to 0.0.
        valor_tarifa (float, optional): G.07 - Valor da tarifa referente a cada comprovante arrecadado (será informado desde que acordado entre as partes). Defaults to 0.0.
        nsr (_type_, optional): G.08 - NSR - Número Seqüencial de Registro. Defaults to None.
        codigo_agencia (str, optional): G.09 - Código da agência arrecadadora. Defaults to ' '.
        forma_arrecadacao (str, optional): G.10 – Forma de arrecadação/captura (canais de recebimento)
            1 – Guichê de Caixa com fatura/guia de arrecadação
            2 – Arrecadação Eletrônica com fatura/guia de arrecadação (terminais de auto - atendimento, ATM, home/office banking)
            3 – Internet com fatura/guia de arrecadação
            4 – Outros meios com fatura/guia de arrecadação
            5 – Correspondentes bancários com fatura/guia de arrecadação
            6 – Telefone com fatura/guia de arrecadação
            7 – Casas lotéricas com fatura/guia de arrecadação
            a – Guichê de Caixa sem fatura/guia de arrecadação
            b – Arrecadação Eletrônica sem fatura/guia de arrecadação (terminais de auto - atendimento, ATM, home/office banking)
            c – Internet sem fatura/guia de arrecadação
            d – Correspondentes bancários sem fatura/guia de arrecadação
            e – Telefone sem fatura/guia de arrecadação
            f – Outros meios sem fatura/guia de arrecadação
            g – Casas lotéricas sem fatura/guia de arrecadação. Defaults to ' '.
        autenticacao (str, optional): G.11 – Número de autenticação caixa ou código de transação (será informado desde que acordado entre as partes). Defaults to ' '.
        forma_pagamento (str, optional): G.12 – Forma de Pagamento
            1 – Dinheiro
            2 – Cheque
            3 – Não identificado/outras formas. Defaults to '0'.
        reservado (str, optional): G.13 – Reservado para o futuro. Defaults to ' '.

    Raises:
        Exception: Campo inválido.

    Returns:
        str: Retorna um registro com 150bytes.
    """
    registro_g = 'G'

    if len(codigo_banco) > 3:
        raise Exception(
            'Campo G.02 Inválido. O campo deve ter o tamanho máximo de 3.'
        )
    if not codigo_banco.isdigit():
        raise Exception(
            'Campo G.02 Inválido. O campo codigo_banco deve ser numérico.'
        )
    registro_g += codigo_banco.zfill(3)

    if not agencia.isdigit():
        raise Exception(
            'Campo G.02 Inválido. O campo agencia deve ser numérico.'
        )

    if not conta.isdigit():
        raise Exception(
            'Campo G.02 Inválido. O campo conta deve ser numérico.'
        )

    if not conta_digito.isdigit():
        raise Exception(
            'Campo G.02 Inválido. O campo conta_digito deve ser numérico.'
        )

    agencia_conta = agencia + conta + conta_digito
    if len(agencia_conta) > 17:
        raise Exception(
            'Campo G.02 Inválido. Os campos agencia, conta e conta_digito juntos devem ter tamanho máximo de 17.'
        )
    registro_g += agencia_conta.zfill(17)

    try:
        datetime.strptime(data_pagamento, '%Y%m%d')
    except:
        raise Exception(
            'Campo G.03 Inválido. O campo deve ser uma data no formato AAAAMMDD.'
        )
    registro_g += data_pagamento

    try:
        datetime.strptime(data_credito, '%Y%m%d')
    except:
        raise Exception(
            'Campo G.04 Inválido. O campo deve ser uma data no formato AAAAMMDD.'
        )
    registro_g += data_credito

    if len(codigo_de_barras_44) != 44:
        raise Exception(
            'Campo G.05 Inválido. O campo deve ser um código de barras de 44 posições.'
        )
    registro_g += codigo_de_barras_44

    if not isinstance(valor_recebido, float):
        raise Exception('Campo G.06 Inválido. O campo deve ser um float.')
    registro_g += str(int(valor_recebido * 100)).zfill(12)

    if not isinstance(valor_tarifa, float):
        raise Exception('Campo G.07 Inválido. O campo deve ser um float.')
    registro_g += str(int(valor_tarifa * 100)).zfill(7)

    if not isinstance(nsr, int):
        raise Exception('Campo G.08 Inválido. O campo deve ser um int.')
    registro_g += str(nsr).zfill(8)

    if len(codigo_agencia) > 8:
        raise Exception(
            'Campo G.09 Inválido. O campo deve ter o tamanho máximo de 8.'
        )
    registro_g += codigo_agencia.ljust(8)

    if len(forma_arrecadacao) > 1:
        raise Exception('Campo G.10 Inválido. O campo deve ter o tamanho 1.')

    if forma_arrecadacao not in [
        c.ARRECADACAO_GUICHE_COM_FATURA,
        c.ARRECADACAO_ELETRONICA_COM_FATURA,
        c.ARRECADACAO_INTERNET_COM_FATURA,
        c.ARRECADACAO_OUTROS_COM_FATURA,
        c.ARRECADACAO_CORRESPONDENTES_COM_FATURA,
        c.ARRECADACAO_TELEFONE_COM_FATURA,
        c.ARRECADACAO_LOTERICAS_COM_FATURA,
        c.ARRECADACAO_GUICHE_SEM_FATURA,
        c.ARRECADACAO_ELETRONICA_SEM_FATURA,
        c.ARRECADACAO_INTERNET_SEM_FATURA,
        c.ARRECADACAO_CORRESPONDENTES_SEM_FATURA,
        c.ARRECADACAO_TELEFONE_SEM_FATURA,
        c.ARRECADACAO_OUTROS_SEM_FATURA,
        c.ARRECADACAO_LOTERICAS_SEM_FATURA,
    ]:
        raise Exception('Campo G.10 Inválido.')

    registro_g += forma_arrecadacao.ljust(1)

    if len(autenticacao) > 23:
        raise Exception(
            'Campo G.11 Inválido. O campo deve ter o tamanho máximo de 23.'
        )
    registro_g += autenticacao.ljust(23)

    if len(forma_pagamento) > 1:
        raise Exception(
            'Campo G.12 Inválido. O campo deve ter o tamanho máximo de 1.'
        )
    if not forma_pagamento.isdigit():
        raise Exception('Campo G.12 Inválido. O campo deve ser numérico.')
    registro_g += forma_pagamento.zfill(1)

    if len(reservado) > 9:
        raise Exception(
            'Campo G.13 Inválido. O campo deve ter o tamanho máximo de 9.'
        )
    registro_g += reservado.upper().ljust(9)
    return registro_g


def registro_Z(total_registros=0, valor_total_registros=0.0, reservado=''):
    """
    REGISTRO “Z” - TRAILLER

    Args:
        total_registros (int, optional): Z.02 - Total de registros no arquivo
            Total de registros no arquivo, inclusive com header e trailler. Defaults to 0.
        valor_total_registros (float, optional): Z.03 - Valor total dos registros do arquivo. Defaults to 0.0.
        reservado (str, optional): Z.04 - Reservado para o futuro (filler). Defaults to ''.

    Raises:
        Exception: Campo inválido.

    Returns:
        str: Retorna um registro com 150bytes.
    """
    registro_z = 'Z'

    if not isinstance(total_registros, int):
        raise Exception('Campo Z.02 Inválido. O campo deve ser um int.')
    registro_z += str(total_registros).zfill(6)

    if not isinstance(valor_total_registros, float):
        raise Exception('Campo Z.03 Inválido. O campo deve ser um float.')
    registro_z += str(int(valor_total_registros * 100)).zfill(17)

    if len(reservado) > 126:
        raise Exception(
            'Campo Z.04 Inválido. O campo deve ter o tamanho máximo de 126.'
        )
    registro_z += reservado.upper().ljust(126)
    return registro_z
