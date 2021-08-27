# APS 2° Semestre - Criptografia :lock:

## Informações do projeto
Atividades Práticas Supervisionadas (APS) do curso de Ciência da Computação 2° semestre, tendo como tema a criação de uma aplicação que implemente um sistema de encriptação de mensagens informadas pelo usuário.

## Tecnologias utilizadas
Linguagem de programação Python e a biblioteca Crypto, disponibilizada pelo pacote pyCryptodome

## Modo de uso
Com a aplicação aberta, existem 2 possibilidades:

1. Selecione a caixa de texto e digite a mensagem que deseja encriptar;
2. Informe o nome de um arquivo de texto que contém a mensagem que deseja encriptar.

Em seguida, informe uma senha, que será utilizada para realizar a encriptação e decriptação do texto puro. Após digitar a senha desejada, aperte em 'Encriptar' para realizar o processo de encriptação.

Após isso, caso tenha digitado a mensagem na caixa de texto, a mensagem encriptada será retornada e irá substituir o texto puro antes informado, disponibilizando a opção de que o usuário copie o conteúdo para a área de transferência. Caso contrário, será criado um arquivo texto denominado 'encrypted-nome_do_arquivo.txt', e o mesmo irá conter o conteúdo encriptado.

Para desfazer o processo, repita as etapas anteriores, mas dessa vez informe o conteúdo que foi encriptado. Ao final, será retornado, da mesma forma, o conteúdo original.
