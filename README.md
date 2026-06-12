# 🤖 Agente de Trading Inteligente — AlexisProfit

> Agente pessoal de IA construído na plataforma [Base44](https://base44.com) que faz **três coisas poderosas**:
> 1. 📬 Monitora e resume seus emails, enviando notificações pelo Telegram
> 2. 💬 Permite responder emails diretamente pelo Telegram, sem abrir o computador
> 3. 📊 Gera automaticamente **Pine Script** para backteste no TradingView a partir dos seus robôs de trading

---

## 📋 Índice

- [O que o agente faz](#-o-que-o-agente-faz)
- [Como funciona o Agente de E-mail](#-como-funciona-o-agente-de-e-mail)
- [Como funciona o Gerador de Backteste](#-como-funciona-o-gerador-de-backteste)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Passo a passo no TradingView](#-passo-a-passo-no-tradingview)
- [Robôs compatíveis](#-robôs-compatíveis)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Avisos importantes](#-avisos-importantes)

---

## 🚀 O que o agente faz

### 📬 Módulo 1 — Agente de E-mail + Telegram

O agente monitora sua caixa de entrada do Gmail em tempo real e te avisa no Telegram sempre que um novo email chega, com um resumo completo do conteúdo.

**Funcionalidades:**
- ✅ Monitoramento automático do Gmail via Google Pub/Sub
- ✅ Extrai remetente, assunto, data e corpo do email
- ✅ Resume o conteúdo (até 400 caracteres + indicador de continuação)
- ✅ Envia notificação formatada no bot Telegram **@AlexisMail_bot**
- ✅ Permite responder o email direto pelo Telegram com o comando:
  > *"Responda o email [ID] dizendo: [sua mensagem]"*

---

### 📊 Módulo 2 — Gerador de Backteste Pine Script

Você envia os arquivos do seu robô de trading, e o agente converte automaticamente a lógica de sinais para **Pine Script v5**, pronto para rodar no Strategy Tester do TradingView.

**O que o agente faz automaticamente:**
- ✅ Solicita os arquivos `strategy.py` + `bot.py` (Python) ou `robot.js` (Node.js)
- ✅ Lê e extrai todos os parâmetros: RSI, DCA, Stop Loss, Trailing, Timeframe, Par
- ✅ Gera o Pine Script completo e fiel à lógica do robô
- ✅ Entrega o código + passo a passo de como usar no TradingView
- ✅ Salva o arquivo `.pine` gerado na pasta `pine_scripts/`
- ✅ **Nunca modifica** os arquivos originais do robô

---

## 📬 Como funciona o Agente de E-mail

```
Gmail recebe um email
        ↓
Google Pub/Sub dispara notificação em tempo real
        ↓
Base44 aciona a função backend (processNewEmail.ts)
        ↓
Função lê o email via Gmail API (remetente, assunto, corpo)
        ↓
Agente resume e formata a mensagem
        ↓
Envia notificação no Telegram → @AlexisMail_bot
        ↓
Você lê o resumo e responde pelo Telegram se quiser
```

**Exemplo de notificação no Telegram:**
```
📧 Novo email!
De: João Silva <joao@empresa.com>
Assunto: Reunião amanhã às 14h
Data: Sex, 12 Jun 2026

Resumo:
Olá, confirmando nossa reunião de amanhã às 14h na sala 3.
Por favor traga o relatório do mês...

🔑 ID: `18f3a2b1c4d5`
📩 Para responder, me diga: "Responda o email 18f3a2b1c4d5 dizendo: [sua mensagem]"
```

---

## 📊 Como funciona o Gerador de Backteste

```
Você envia strategy.py + bot.py (ou robot.js)
              ↓
Agente analisa o código e extrai:
  • Período e threshold do RSI
  • Gatilhos de DCA (ex: -1.5% e -2.5%)
  • Stop Loss percentual (ex: -10%)
  • Trailing Profit trigger e callback (ex: +2%, recuo 0.2%)
  • Timeframe e par operado (ex: 15m, BTC/USDT)
  • Indicadores: EMA, Williams %R, MACD, CDV, Bollinger...
              ↓
Gera Pine Script //@version=5 com:
  • Lógica de entrada/saída idêntica ao robô
  • Gestão completa de DCA (até 2 recompras)
  • Stop Loss e Trailing Profit
  • Linhas visuais no gráfico (preço médio, stop, trailing)
  • Painel de status no canto do gráfico
  • Parâmetros editáveis pelo painel ⚙️ do TradingView
              ↓
Entrega o código + passo a passo completo
              ↓
Você cola no TradingView → Strategy Tester roda na hora
```

---

## 📁 Estrutura do projeto

```
agente-email-telegram/
│
├── 📄 README.md                          # Esta documentação
│
├── functions/
│   └── processNewEmail.ts                # Função backend (Deno)
│                                         # Processa emails recebidos via Pub/Sub
│                                         # Extrai dados e envia resumo pro agente
│
├── skills/
│   └── gerar_backtest_pinescript/
│       ├── SKILL.md                      # Documentação da skill
│       └── run.py                        # Motor Python de conversão
│                                         # Lê robô → extrai parâmetros → gera Pine Script
│
├── rules/
│   └── backtest_pinescript.md            # Regra do comportamento do agente
│                                         # Define QUANDO e COMO pedir os arquivos
│                                         # e o formato obrigatório de entrega
│
├── pine_scripts/
│   └── alexisprofit_backtest.pine        # Pine Script gerado — AlexisProfit
│                                         # Estratégia: RSI(14) + DCA + Trailing Profit
│
└── base44/
    └── connectors/
        └── gmail.jsonc                   # Configuração do conector OAuth Gmail
```

---

## 📋 Passo a passo no TradingView

Após receber o Pine Script gerado pelo agente:

**1️⃣** Acesse **[tradingview.com](https://tradingview.com)** e faça login

**2️⃣** Abra o gráfico do par do seu robô (ex: `BTCUSDT`)

**3️⃣** Selecione o mesmo timeframe do robô (ex: `15m`)

**4️⃣** No rodapé, clique em **"Pine Editor"**

**5️⃣** Selecione tudo (`Ctrl+A`) e delete o conteúdo

**6️⃣** Cole o Pine Script recebido do agente

**7️⃣** Clique em **"Adicionar ao gráfico"** (botão azul)

**8️⃣** Vá na aba **"Strategy Tester"** para ver os resultados:

| Métrica | O que significa |
|---|---|
| 💰 Lucro líquido | Resultado total da estratégia no período |
| 📊 Nº de operações | Quantas entradas e saídas ocorreram |
| ✅ Taxa de acerto | % de operações lucrativas |
| 📉 Drawdown máximo | Maior queda acumulada do capital |
| ⚖️ Profit Factor | Relação ganhos / perdas (>1 é positivo) |

**9️⃣** Clique na **engrenagem ⚙️** para ajustar os parâmetros e retestar

**🔟** Teste em pelo menos **6 meses de histórico** para resultados confiáveis

---

## 🤖 Robôs compatíveis

| Robô | Linguagem | Exchange | Estratégia | Backteste |
|---|---|---|---|---|
| **AlexisProfit** | Python | Binance Spot | RSI(14) + DCA + Trailing Profit + Fear & Greed Filter | ✅ Gerado |
| **Robô Binance** | Node.js | Binance Spot | EMA(100) + Williams %R + CDV + RSI | ✅ Suportado |

### Indicadores suportados na extração automática

| Indicador | Extração Automática |
|---|---|
| RSI (Wilder) | ✅ |
| EMA / SMA | ✅ |
| DCA (até 2 recompras) | ✅ |
| Trailing Profit | ✅ |
| Stop Loss % | ✅ |
| Williams %R | ✅ |
| MACD | ✅ |
| Bollinger Bands | ✅ |
| CDV (Cumulative Delta Volume) | ✅ |
| Fear & Greed Filter | ✅ (simulado) |
| Cooldown pós-venda | ✅ |

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| [Base44](https://base44.com) | — | Plataforma do agente de IA |
| [Gmail API](https://developers.google.com/gmail) | v1 | Leitura e envio de emails |
| [Telegram Bot API](https://core.telegram.org/bots/api) | — | Canal de comunicação |
| [Deno](https://deno.land) | 2.x | Runtime da função backend |
| [Pine Script](https://www.tradingview.com/pine-script-docs/) | v5 | Backteste no TradingView |
| [Python](https://python.org) | 3.10+ | Motor de conversão de estratégias |
| [Binance API](https://binance-docs.github.io/apidocs/) | — | Exchange dos robôs |
| [CCXT](https://github.com/ccxt/ccxt) | — | Biblioteca de conexão à exchange |
| [pandas](https://pandas.pydata.org) | — | Cálculo de indicadores no robô Python |

---

## ⚠️ Avisos importantes

> **Resultados de backteste não garantem resultados futuros.**

- O agente **nunca modifica** os arquivos originais dos robôs
- O backteste no TradingView **não considera** slippage real e liquidez do mercado
- O índice **Fear & Greed** é simulado no Pine Script (sem dados históricos disponíveis no TradingView)
- Estratégias mal calibradas podem sofrer de **overfitting** (ajuste excessivo ao passado)
- Recomenda-se testar em pelo menos **6 meses de histórico**
- Este projeto é para fins **educacionais e de análise** — não é recomendação de investimento

---

## 📄 Licença

MIT — use, modifique e distribua à vontade!

---

<div align="center">
  Feito com ❤️ por <strong>alexis-developers</strong> usando <a href="https://base44.com">Base44</a>
</div>
