# Skill: Gerar Backteste Pine Script

## O que esta skill faz
Recebe os arquivos do robô de trading (strategy.py e bot.py), analisa a lógica de sinais e gera automaticamente um Pine Script completo para backteste no TradingView, com passo a passo de uso.

## Quando usar
- Quando o usuário pedir para gerar um backteste
- Quando o usuário enviar arquivos de estratégia de trading
- Quando o usuário quiser testar uma estratégia no TradingView

## Como funciona
1. Solicita os arquivos strategy.py e bot.py ao usuário
2. Lê e analisa os parâmetros e a lógica de sinais
3. Converte para Pine Script //@version=5
4. Entrega o código + passo a passo completo

## Parâmetros extraídos automaticamente
- Período e threshold do RSI
- Gatilhos de DCA (queda % para recompra)
- Stop Loss percentual
- Trailing Profit trigger e callback
- Timeframe e par operado
- Qualquer outro indicador identificado no código

## Formato de entrega
Sempre entrega:
1. O Pine Script completo (pronto para colar)
2. Passo a passo numerado de como usar no TradingView
3. Explicação de cada parâmetro ajustável

## Idioma
Sempre em português brasileiro.
