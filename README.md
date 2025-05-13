# financial
O Sistema de Controle Financeiro é uma aplicação em desenvolvimento com a linguagem Python e banco de dados PostgreSQL. Seu objetivo principal é permitir que usuários organizem suas finanças. A aplicação é pensada com base em princípios de orientação a objetos.


## Estrutura do projeto

financial/
│
├── database/       # SQLs e conexões com banco
├── models/         # Classes que representam os dados (ex: Usuário, Transação)
├── controllers/    # Regras de negócio e manipulação dos dados
├── services/       # Funções auxiliares (ex: exportar CSV, calcular saldo)
├── ui/             # Interface gráfica (se usar Tkinter, PyQt etc.)
├── tests/          # Testes unitários
├── main.py         # Arquivo principal para rodar o app
└── requirements.txt
