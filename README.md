# Sistema Bancário

Este é um projeto de um sistema bancário simples desenvolvido em Python como parte do curso de Engenharia de Dados com Python da NTT DATA.

## Funcionalidades

O sistema bancário inclui as seguintes operações:

- Depósito
- Saque
- Extrato
- Cadastro de Usuários
- Cadastro de Contas Correntes
- Listagem de Usuários
- Listagem de Contas Correntes
- Sair

## Como usar

1. Clone este repositório
2. Execute o arquivo Python principal
3. Siga as instruções no menu para realizar operações bancárias

## Detalhes de implementação

- O sistema mantém um saldo da conta
- Há um limite de 3 saques diários
- Cada saque tem um limite de R$ 500,00
- O extrato lista todas as operações realizadas
- Os usuários são armazenados com nome, data de nascimento, CPF e endereço
- As contas correntes são vinculadas aos usuários através do CPF

## Changelog

### Versão 1.0.0

- Implementação inicial do sistema bancário
- Funcionalidades básicas: depósito, saque e extrato
- Limite de saques diários e valor máximo por saque

### Versão 2.0.0

- Refatoração do código para utilizar funções modulares
- Adição de cadastro e listagem de usuários
- Adição de cadastro e listagem de contas correntes
- Implementação de validações para CPF e data de nascimento
- Melhoria no tratamento de erros e validações de entrada
- Atualização do menu para incluir novas funcionalidades

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Autor

Ulisses Pereira

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.
