# Máquina de Turing Universal

Disciplina: Teoria da Computação (10A).

## Implementação de uma MTU utilizando a biblioteca automata.
Nesta atividade, vamos desenvolver um microserviço de uma Máquina de Turing Universal. O desafio consiste em utilizar Python com FastAPI1 e a biblioteca automata2. A atividade pode ser realizada em dupla e será conduzida ao longo de duas aulas nesta semana (terça e quarta-feira). Vou guiá-los até o passo 6, e os passos 7 e 8 devem ser concluídos por vocês e entregues como uma atividade no campus.

Esta atividade é válida e útil para entendermos a prática de MTU, bem como as tecnologias utilizadas hoje em dia na indústria, tais como microservice, docker, etc.

A seguir, são apresentados os passos necessários de forma geral:
1. Devemos criar um projeto em Python.
2. Devemos adicionar a lib FastAPI.
3. Devemos adicionar a lib automata.
4. Devemos criar um endpoint (POST) para receber as os inputs da MT a ser
executada. O seguinte link ilustra um exemplo de uma input (https://gist.github.com/rdurelli/52463be8aa9b3976dfce6db41a51da93).
5. Após enviar a input, devemos validar se todos os campos foram enviados. Caso tenha campo faltando, devemos enviar uma mensagem de erro, com o código 404, informando o motivo do erro.
    Por exemplo, o campo "states" não foi enviado. Deve-se o seguinte JSON: {"code": 404, "msg": "Campo state é obrigatório"}
6. Devemos criar um Dockerfile para criar uma imagem do nosso microservice.
7. Salvar em um banco de dados todas as request que chegarem no método POST.
8. Implementar LOG para identificar o fluxo de execução do microservice.