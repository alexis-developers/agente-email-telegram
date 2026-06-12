# 🤖 Agente de Trading Inteligente — Base44 Superagent

Agente pessoal de IA que **monitora emails, responde via Telegram** e **gera backtestes automáticos em Pine Script** para seus robôs de trading — tudo integrado, sem precisar abrir código.

---

## 🚀 O que este agente faz

### 📬 1. Agente de E-mail + Telegram
- Monitora sua caixa de entrada do Gmail em tempo real
- Resume o conteúdo de cada email recebido
- Envia notificação direto no Telegram com remetente, assunto e resumo
- Permite responder emails pelo Telegram sem abrir o computador

### 📊 2. Gerador de Backteste (Pine Script)
- Você envia os arquivos do seu robô (`strategy.py` + `bot.py`)
- O agente **lê e analisa automaticamente** a lógica de sinais
- **Gera o Pine Script completo** fiel à estratégia do robô
- Entrega o código pronto pra colar no TradingView
- Inclui **passo a passo detalhado** de como usar no Strategy Tester
- Suporta robôs em **Python** e **Node.js**
- Nunca modifica os arquivos originais do robô

---

## 🧠 Estratégias suportadas no backteste

| Indicador | Suporte |
|---|---|
| RSI (com suavização de Wilder) | ✅ |
| EMA / SMA | ✅ |
| DCA (Dollar Cost Averaging) | ✅ |
| Trailing Profit | ✅ |
| Stop Loss percentual | ✅ |
| Williams %R | ✅ |
| MACD | ✅ |
| Bollinger Bands | ✅ |
| Fear & Greed Filter | ✅ (simulado) |
| CDV (Cumulative Delta Volume) | ✅ |

---

## 📁 Estrutura do projeto

```
├── functions/
│   └── processNewEmail.ts          # Função backend: processa emails e notifica no Telegram
│
├── skills/
│   └── gerar_backtest_pinescript/
│       ├── SKILL.md                # Documentação da skill
│       └── run.py                  # Script Python que converte robô → Pine Script
│
├── rules/
│   └── backtest_pinescript.md      # Regra do agente: comportamento automático
│
├── pine_scripts/
│   └── alexisprofit_backtest.pine  # Exemplo: AlexisProfit RSI+DCA+Trailing gerado
│
├── base44/
│   └── connectors/
│       └── gmail.jsonc             # Configuração do conector Gmail
│
└── README.md
```

---

## ⚙️ Como funciona o Gerador de Backteste

```
Você envia strategy.py + bot.py
            ↓
Agente lê e extrai parâmetros:
  • RSI period e threshold
  • Gatilhos de DCA (-1.5%, -2.5%)
  • Stop Loss (%)
  • Trailing Profit trigger e callback
  • Timeframe e par operado
            ↓
Gera Pine Script //@version=5
  • Lógica fiel ao robô original
  • Parâmetros editáveis no TradingView
  • Painel visual de status no gráfico
  • Linhas de Stop Loss e Trailing
  • Shapes de entrada e DCA no gráfico
            ↓
Entrega o código + passo a passo completo
            ↓
Você cola no TradingView → Strategy Tester roda
```

---

## 📋 Como usar o Pine Script no TradingView

1. Acesse **[tradingview.com](https://tradingview.com)** e faça login
2. Abra o gráfico do par desejado (ex: `BTCUSDT`)
3. Selecione o timeframe do seu robô (ex: `15m`)
4. No rodapé, clique em **"Pine Editor"**
5. Selecione tudo (`Ctrl+A`) e delete
6. Cole o Pine Script gerado pelo agente
7. Clique em **"Adicionar ao gráfico"**
8. Vá na aba **"Strategy Tester"** para ver os resultados:
   - 💰 Lucro líquido
   - 📊 Total de operações
   - ✅ Taxa de acerto
   - 📉 Drawdown máximo
   - ⚖️ Profit Factor
9. Clique na **engrenagem ⚙️** para ajustar os parâmetros

---

## 📬 Como funciona o Agente de E-mail

```
Gmail recebe email
       ↓
Google Pub/Sub dispara notificação
       ↓
Base44 aciona o agente automaticamente
       ↓
Agente lê o email via Gmail API
       ↓
Resume: remetente, assunto, corpo
       ↓
Envia mensagem formatada no Telegram
       ↓
Você responde pelo Telegram → agente envia o email
```

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| [Base44](https://base44.com) | Plataforma do agente de IA |
| Gmail API (OAuth2) | Leitura e envio de emails |
| Telegram Bot API | Canal de comunicação (@AlexisMail_bot) |
| Deno (Backend Functions) | Processamento em tempo real |
| Pine Script v5 | Backteste no TradingView |
| Python 3 | Motor de conversão de estratégias |
| Binance API + CCXT | Exchange dos robôs de trading |

---

## 🤖 Robôs de trading compatíveis

| Robô | Linguagem | Estratégia | Status |
|---|---|---|---|
| AlexisProfit | Python | RSI + DCA + Trailing Profit | ✅ Backteste gerado |
| Robô Binance | Node.js | EMA 100 + Williams %R + CDV + RSI | ✅ Suportado |

---

## ⚠️ Avisos importantes

- Resultados de backteste **não garantem resultados futuros**
- O agente **nunca modifica** os arquivos originais dos robôs
- O backteste no TradingView não considera **slippage real** e **liquidez** do mercado
- Fear & Greed Index é **simulado** no Pine Script (não existe dado histórico em tempo real no TradingView)
- Recomenda-se testar em pelo menos **6 meses de histórico**

---

## 📄 Licença

MIT — use à vontade!

---

Feito com ❤️ usando [Base44](https://base44.com)
