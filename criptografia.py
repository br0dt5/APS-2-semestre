import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode


def encrypt(password:str, plain_text:str=None, filename:str=None):
    """
    Faz a criptografia dos dados informados.

    :param password: Senha informada pelo usuário.
    :param plain_text: (opcional) Texto plano que será criptografado.
    :param filename: (opcional) Nome do arquivo que terá o conteúdo criptografado.
    :return: Texto cifrado.
    """

    # Geração do salt, nonce
    salt = b64encode(get_random_bytes(16)).decode()
    nonce = get_random_bytes(16)

    # Criação de uma chave derivada a partir da senha
    key = scrypt(password, salt, 16, N=2 ** 10, r=8, p=1)

    # Criação do objeto para criptografia
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    try:
        # Verifica se o dado informado é um arquivo ...
        if filename is not None:

            # Define o nome do arquivo de saída do texto cifrado.
            out_filename = 'enc-' + filename

            # Abertura dos arquivos e leitura do texto plano.
            input_file = open(rf'{filename}', 'rb')
            output_file = open(out_filename, 'w')
            to_encrypt = input_file.read()

            # Realiza a encriptação.
            cipher_text, tag = cipher.encrypt_and_digest(to_encrypt)

            # Cria um dicionário contendo os valores de nonce, tag, salt e ciphertext decodificados para string.
            keys = ['nonce', 'tag', 'salt', 'ciphertext']
            values = [b64encode(x).decode() for x in [cipher.nonce, tag, b64decode(salt), cipher_text]]
            data = json.dumps(dict(zip(keys, values)))

            # Escreve o conteúdo no arquivo de saída e fecha os arquivos abertos.
            output_file.write(data)
            input_file.close()
            output_file.close()

            # Mensagem de retorno
            return f'Encriptação realizada com sucesso. Um arquivo denominado {out_filename} foi criado.'

        # ... ou texto puro ....
        elif plain_text is not None:

            # Realiza a encriptação
            to_encrypt = plain_text.encode()
            cipher_text, tag = cipher.encrypt_and_digest(to_encrypt)

            # Criação de uma string contendo os valores de nonce, tag, salt e ciphertext.
            output = [b64encode(x).decode() for x in [cipher.nonce, tag, b64decode(salt), cipher_text]]
            output = ''.join(output)

            # Retorna o texto cifrado
            return output

        # ... ou se foi informado os parâmetros necessários.
        else:
            return 'Erro! Verifique os dados inseridos.'

    # Excessão caso não ache o arquivo informado.
    except FileNotFoundError:
        return 'Arquivo não encontrado.'

    # Excessão caso a encriptação falhe.
    except:
        return 'Algo inesperado aconteceu.'


def decrypt(password:str, cipher_text:str=None, filename:str=None):
    """
    Faz a decriptografia dos dados informado.

    :param password: Senha informada pelo usuário.
    :param cipher_text: (opcional) Texto cifrado que será decriptografado.
    :param filename: (opcional) Nome do arquivo que terá o conteúdo decriptografado.
    :return: Texto plano.
    """

    try:
        # Verifica se o dado informado é um arquivo ...
        if filename is not None:

            # Define o nome do arquivo de saída do texto plano.
            out_filename = filename.replace('enc-', '')

            # Abertura do arquivo e leitura do conteúdo
            file = open(filename, 'r')
            content = json.loads(file.read())

            # Cria um dicionário a partir do conteúdo e transforma seus valores em bytes.
            data = {k: b64decode(content[k]) for k, v in content.items()}

            # Criação da chave derivada a partir da senha informada.
            salt = b64encode(data['salt']).decode()
            key = scrypt(password, salt, 16, N=2 ** 10, r=8, p=1)

            # Cria o objeto de criptografia
            cipher = AES.new(key, AES.MODE_GCM, nonce=data['nonce'])

            # Realiza a decriptação
            plain_text = cipher.decrypt_and_verify(data['ciphertext'], data['tag'])

            # Abre o arquivo de saída
            a = open(out_filename, 'w', encoding='utf-8')

            # Faz a decodificação de binário para string. (1ª linha)
            # Devido ao fato de que o Windows utiliza tanto \r quanto \n para definir linhas em arquivos, foi necessário a remoção de um deles para evitar e corrigir o erro de escrever 2 linhas, ao invés de 1. (2ª linha)
            output = plain_text.decode()
            output = output.replace('\r', '')

            # Escreve o conteúdo no arquivo e fecha os arquivos abertos.
            a.write(output)
            file.close()
            a.close()

            # Mensagem de retorno
            return f'Decriptografia realizada com sucesso. Um arquivo denominado {out_filename} foi criado.'

        # ... ou texto puro ....
        elif cipher_text is not None:

            # Adquire os valores a partir da texto cifrado informado.
            nonce, tag, salt, cipher = cipher_text[:24], cipher_text[24:48], cipher_text[48:72], cipher_text[72:]

            # Gera um dicionário que contém seus valores codificados em bytes.
            keys = ['nonce', 'tag', 'salt', 'ciphertext']
            data = {k: b64decode(v) for k, v in zip(keys, [nonce, tag, salt, cipher])}

            # Criação da chave derivada a partir da senha informada.
            salt = b64encode(data['salt']).decode()
            key = scrypt(password, salt, 16, N=2 ** 10, r=8, p=1)

            # Cria o objeto de criptografia.
            cipher = AES.new(key, AES.MODE_GCM, nonce=data['nonce'])

            # Realiza a decriptação.
            plain_text = cipher.decrypt_and_verify(data['ciphertext'], data['tag'])

            # Retorna o texto plano.
            return plain_text.decode()

        # ... ou se foi informado os parâmetros necessários.
        else:
            return 'Erro na decriptografia. Verifique os dados inseridos.'

    # Excessão caso o arquivo informado não foi encontrado.
    except FileNotFoundError:
        return 'Arquivo não encontrado.'

    # Excessão caso aconteça algum erro na decriptação, respectivo a senha ou MAC.
    except (ValueError, KeyError):
        return 'Erro na decriptografia. Verifique os dados inseridos.'
