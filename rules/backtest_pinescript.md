# Regra: Gerar Backteste Pine Script

## Quando o usuário pedir um backteste ou Pine Script

### Passo 1 — Solicitar os arquivos
Sempre que o usuário pedir para gerar um backteste, responda EXATAMENTE assim:

"Para gerar o Pine Script do backteste, preciso dos arquivos do seu robô. Pode enviar aqui no chat:

📎 **strategy.py** — contém a lógica de sinais da estratégia
📎 **bot.py** — contém os parâmetros de configuração do robô

Se for um robô Node.js, envie o arquivo principal (ex: robot.js ou bot.js).

Arraste os arquivos diretamente aqui no chat! 🚀"

### Passo 2 — Ao receber os arquivos
Quando os arquivos chegarem em incoming_files/:
1. Leia o conteúdo dos arquivos com read_file
2. Salve temporariamente em /tmp/
3. Execute a skill: run_skill("gerar_backtest_pinescript") com os argumentos corretos
4. Entregue o Pine Script completo + passo a passo

### Passo 3 — Formato de entrega OBRIGATÓRIO
Sempre entregar neste formato:

```
📊 PINE SCRIPT GERADO — [Nome da Estratégia]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[CÓDIGO PINE SCRIPT COMPLETO AQUI]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 PASSO A PASSO NO TRADINGVIEW:

1️⃣ Abra tradingview.com → busque [PAR] → timeframe [TF]
2️⃣ Clique em "Pine Editor" no rodapé
3️⃣ Selecione tudo (Ctrl+A) e delete
4️⃣ Cole o código acima
5️⃣ Clique em "Adicionar ao gráfico"
6️⃣ Vá em "Strategy Tester" para ver os resultados
7️⃣ Clique ⚙️ na estratégia para ajustar os parâmetros
```

### Regras importantes
- NUNCA modificar os arquivos originais do usuário
- SEMPRE gerar arquivo separado .pine
- SEMPRE incluir o passo a passo junto com o código
- SEMPRE salvar o .pine gerado no GitHub (pasta pine_scripts/)
- Suportar robôs Python E Node.js
- Todo conteúdo em português
