# MCP para tarefas — exercício 4.2

Autor: Kin Modesto Sugai. Implementação com apoio do Codex.

Servidor MCP via stdio, usando o SDK oficial. As ferramentas fazem requisições HTTP reais à API do [exercício 4.1](https://github.com/kinsugai/exercicio-41-api-tarefas).

## Executar

Deixe a API rodando em http://localhost:8000. Neste repositório, com Python 3.10 ou superior:

~~~sh
python -m venv .venv
# Git Bash: source .venv/Scripts/activate
# PowerShell: .venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python cliente_teste.py
~~~

O cliente inicia o servidor como subprocesso usando o mesmo Python do cliente, lista as ferramentas, cria uma tarefa e lista as tarefas. A saída padrão contém apenas um envelope JSON com tools, criar_resultado e listar_resultado; logs vão para stderr. A variável TAREFAS_API_URL permite alterar o endereço da API; o padrão é http://localhost:8000.

## Ferramentas

- criar_tarefa(titulo): POST /tarefas; devolve a tarefa criada pela API.
- listar_tarefas(): GET /tarefas; devolve a lista da API.

Erros HTTP são propagados ao cliente MCP, sem resultados inventados. O cliente confirma que a tarefa recém-criada aparece na lista.

## Abstração e entrega

O MCP esconde as rotas, os verbos HTTP e a serialização: o agente chama uma ferramenta com argumentos, e o servidor traduz a chamada para a API REST.

~~~sh
autograde validar 4.2
~~~

Referência: [tutorial oficial](https://github.com/alexlopespereira/idp_governodigital/blob/main/exercicios/tutorial_4.2.md).

