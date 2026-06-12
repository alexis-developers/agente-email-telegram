#!/usr/bin/env python3
"""
Skill: Gerar Backteste Pine Script
Analisa arquivos de robô de trading (Python/Node.js) e gera Pine Script para TradingView.
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime

def extrair_parametros_python(codigo_strategy, codigo_bot):
    """Extrai parâmetros do robô Python (strategy.py + bot.py)"""
    params = {
        "rsi_period": 14,
        "rsi_threshold": 30.0,
        "dca_trigger_1": 1.5,
        "dca_trigger_2": 2.5,
        "stop_loss_pct": 10.0,
        "trailing_trigger": 2.0,
        "trailing_callback": 0.2,
        "timeframe": "15m",
        "symbol": "BTC/USDT",
        "initial_buy_usdt": 15.0,
        "dca_buy_usdt": 15.0,
        "cooldown_minutes": 15,
        "indicadores": [],
        "tipo_estrategia": "RSI_DCA_TRAILING"
    }

    # Extrai do bot.py via os.getenv defaults
    patterns = {
        "rsi_period":        r'RSI_PERIOD["\s,]+(\d+)',
        "rsi_threshold":     r'RSI_BUY_THRESHOLD["\s,]+([\d.]+)',
        "dca_trigger_1":     r'DCA_TRIGGER_1["\s,]+([\d.]+)',
        "dca_trigger_2":     r'DCA_TRIGGER_2["\s,]+([\d.]+)',
        "stop_loss_pct":     r'STOP_LOSS_PCT["\s,]+([\d.]+)',
        "trailing_trigger":  r'TRAILING_PROFIT_TRIGGER["\s,]+([\d.]+)',
        "trailing_callback": r'TRAILING_PROFIT_CALLBACK["\s,]+([\d.]+)',
        "timeframe":         r'TIMEFRAME["\s,]+"([\w]+)"',
        "symbol":            r'SYMBOL["\s,]+"([\w/]+)"',
        "initial_buy_usdt":  r'INITIAL_BUY_USDT["\s,]+([\d.]+)',
        "dca_buy_usdt":      r'DCA_BUY_USDT["\s,]+([\d.]+)',
        "cooldown_minutes":  r'COOLDOWN_MINUTES["\s,]+(\d+)',
    }

    codigo_completo = codigo_strategy + "\n" + codigo_bot
    for key, pattern in patterns.items():
        match = re.search(pattern, codigo_completo)
        if match:
            val = match.group(1)
            try:
                if key in ["rsi_period", "cooldown_minutes"]:
                    params[key] = int(val)
                elif key in ["timeframe", "symbol"]:
                    params[key] = val
                else:
                    params[key] = float(val)
            except:
                pass

    # Detecta indicadores usados
    indicadores = []
    if "rsi" in codigo_completo.lower():
        indicadores.append("RSI")
    if "ema" in codigo_completo.lower():
        indicadores.append("EMA")
    if "macd" in codigo_completo.lower():
        indicadores.append("MACD")
    if "williams" in codigo_completo.lower() or "willr" in codigo_completo.lower():
        indicadores.append("Williams %R")
    if "bollinger" in codigo_completo.lower() or "bband" in codigo_completo.lower():
        indicadores.append("Bollinger Bands")
    if "cdv" in codigo_completo.lower() or "cumulative delta" in codigo_completo.lower():
        indicadores.append("CDV")
    if "fear" in codigo_completo.lower() and "greed" in codigo_completo.lower():
        indicadores.append("Fear & Greed Filter")
    if "dca" in codigo_completo.lower():
        indicadores.append("DCA")
    if "trailing" in codigo_completo.lower():
        indicadores.append("Trailing Profit")

    params["indicadores"] = indicadores
    return params


def extrair_parametros_nodejs(codigo_bot):
    """Extrai parâmetros de robô Node.js"""
    params = {
        "rsi_period": 14,
        "rsi_threshold": 30.0,
        "ema_period": 100,
        "williams_period": 14,
        "stop_loss_pct": 10.0,
        "trailing_trigger": 2.0,
        "trailing_callback": 0.2,
        "timeframe": "15m",
        "symbol": "BTC/USDT",
        "indicadores": ["EMA", "Williams %R", "RSI", "CDV"],
        "tipo_estrategia": "EMA_WILLIAMS_CDV_RSI"
    }

    patterns = {
        "rsi_period":        r'rsiPeriod[:\s=]+([\d]+)',
        "ema_period":        r'emaPeriod[:\s=]+([\d]+)',
        "williams_period":   r'williamsPeriod[:\s=]+([\d]+)',
        "stop_loss_pct":     r'stopLoss[:\s=]+([\d.]+)',
        "timeframe":         r'timeframe[:\s=\'"]+([0-9]+[mhd])',
        "symbol":            r'symbol[:\s=\'"]+([A-Z]+\/[A-Z]+)',
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, codigo_bot, re.IGNORECASE)
        if match:
            val = match.group(1)
            try:
                if key in ["rsi_period", "ema_period", "williams_period"]:
                    params[key] = int(val)
                elif key in ["timeframe", "symbol"]:
                    params[key] = val
                else:
                    params[key] = float(val)
            except:
                pass

    return params


def gerar_pine_script_python(params, nome_estrategia="AlexisProfit"):
    """Gera Pine Script para estratégia Python (RSI + DCA + Trailing)"""
    
    timeframe_map = {
        "1m": "1", "3m": "3", "5m": "5", "15m": "15",
        "30m": "30", "1h": "60", "2h": "120", "4h": "240",
        "1d": "D", "1w": "W"
    }
    tf_str = params.get("timeframe", "15m")
    
    has_fng = "Fear & Greed Filter" in params.get("indicadores", [])
    fng_comment = "// Nota: Fear & Greed não é replicável em tempo real no TradingView.\n// Simulado aqui como zona de RSI baixo (conservador)." if has_fng else ""

    symbol_clean = params.get("symbol", "BTC/USDT").replace("/", "")
    
    pine = f"""// ============================================================
// {nome_estrategia} — Backteste Pine Script v5
// Estratégia: {' + '.join(params.get('indicadores', ['RSI']))}
// Timeframe original: {tf_str} | Par: {symbol_clean}
// Gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}
// ⚠️ Resultados passados não garantem resultados futuros.
// ============================================================

//@version=5
strategy(
     title            = "{nome_estrategia} — RSI + DCA + Trailing",
     overlay          = true,
     initial_capital  = 1000,
     default_qty_type = strategy.percent_of_equity,
     default_qty_value = {params.get('initial_buy_usdt', 15)},
     commission_type  = strategy.commission.percent,
     commission_value = 0.1,
     slippage         = 2
)

// ============================================================
// PARÂMETROS — editáveis no painel ⚙️ do TradingView
// ============================================================
rsi_period        = input.int({params.get('rsi_period', 14)},   "Período RSI",               group="📈 RSI")
rsi_threshold     = input.float({params.get('rsi_threshold', 30.0)}, "Gatilho Compra (RSI <)",    group="📈 RSI")

dca_trigger_1     = input.float({params.get('dca_trigger_1', 1.5)},  "DCA 1 — Queda % recompra",  group="🔵 DCA")
dca_trigger_2     = input.float({params.get('dca_trigger_2', 2.5)},  "DCA 2 — Queda % recompra",  group="🔵 DCA")
dca_qty_pct       = input.float({params.get('dca_buy_usdt', 15)},    "Capital DCA (%)",            group="🔵 DCA")

stop_loss_pct     = input.float({params.get('stop_loss_pct', 10.0)}, "Stop Loss (%)",              group="🚪 Saída")
trail_trigger_pct = input.float({params.get('trailing_trigger', 2.0)},"Trailing — Gatilho (%)",    group="🚪 Saída")
trail_callback_pct= input.float({params.get('trailing_callback', 0.2)},"Trailing — Callback (%)", group="🚪 Saída")

cooldown_bars     = input.int({params.get('cooldown_minutes', 15)},  "Cooldown (velas pós-venda)", group="⚙️ Filtros")

{fng_comment}

// ============================================================
// CÁLCULO RSI — Suavização de Wilder (idêntico ao bot Python)
// ============================================================
rsi_val = ta.rsi(close, rsi_period)

// ============================================================
// VARIÁVEIS DE ESTADO
// ============================================================
var float avg_price       = 0.0
var int   dca_count       = 0
var bool  trailing_active = false
var float highest_price   = 0.0
var int   bars_since_sell = 999
var bool  in_position     = false

bars_since_sell := in_position ? bars_since_sell : bars_since_sell + 1

// ============================================================
// ENTRADA — RSI abaixo do threshold + cooldown ok
// ============================================================
buy_signal = not in_position and rsi_val < rsi_threshold and bars_since_sell >= cooldown_bars

if buy_signal
    strategy.entry("Long", strategy.long, comment="🟢 Entrada RSI " + str.tostring(rsi_val, "#.#"))
    avg_price       := close
    dca_count       := 0
    trailing_active := false
    highest_price   := 0.0
    in_position     := true
    bars_since_sell := 0

// ============================================================
// GESTÃO DA POSIÇÃO
// ============================================================
if in_position
    price_change_pct = ((close - avg_price) / avg_price) * 100

    // Atualiza pico do trailing
    if trailing_active and close > highest_price
        highest_price := close

    // ── STOP LOSS ─────────────────────────────────────────
    if price_change_pct <= -stop_loss_pct
        strategy.close("Long", comment="🔴 Stop Loss " + str.tostring(price_change_pct, "#.##") + "%")
        in_position     := false
        trailing_active := false
        avg_price       := 0.0
        dca_count       := 0
        bars_since_sell := 0

    // ── TRAILING PROFIT (SAÍDA) ───────────────────────────
    else if trailing_active
        drop_from_peak = ((highest_price - close) / highest_price) * 100
        if drop_from_peak >= trail_callback_pct
            strategy.close("Long", comment="✅ Trailing +" + str.tostring(price_change_pct, "#.##") + "%")
            in_position     := false
            trailing_active := false
            avg_price       := 0.0
            dca_count       := 0
            bars_since_sell := 0

    // ── ATIVAR TRAILING ───────────────────────────────────
    else if price_change_pct >= trail_trigger_pct
        trailing_active := true
        highest_price   := close

    // ── DCA 1 ─────────────────────────────────────────────
    else if dca_count == 0 and price_change_pct <= -dca_trigger_1
        new_qty   = (strategy.equity * dca_qty_pct / 100) / close
        old_cost  = avg_price * strategy.position_size
        avg_price := (old_cost + close * new_qty) / (strategy.position_size + new_qty)
        dca_count := 1
        strategy.entry("Long", strategy.long, qty=new_qty, comment="🔵 DCA 1 (" + str.tostring(price_change_pct, "#.##") + "%)")

    // ── DCA 2 ─────────────────────────────────────────────
    else if dca_count == 1 and price_change_pct <= -dca_trigger_2
        new_qty   = (strategy.equity * dca_qty_pct / 100) / close
        old_cost  = avg_price * strategy.position_size
        avg_price := (old_cost + close * new_qty) / (strategy.position_size + new_qty)
        dca_count := 2
        strategy.entry("Long", strategy.long, qty=new_qty, comment="🔵 DCA 2 (" + str.tostring(price_change_pct, "#.##") + "%)")

// ============================================================
// PLOTAGENS VISUAIS
// ============================================================
avg_line   = in_position ? avg_price : na
stop_line  = in_position ? avg_price * (1 - stop_loss_pct / 100) : na
trail_line = in_position ? avg_price * (1 + trail_trigger_pct / 100) : na

plot(avg_line,   "📊 Preço Médio",      color=color.new(color.yellow, 0), linewidth=2, style=plot.style_linebr)
plot(stop_line,  "🔴 Stop Loss",        color=color.new(color.red,    0), linewidth=1, style=plot.style_linebr)
plot(trail_line, "⚡ Trailing Trigger", color=color.new(color.green,  0), linewidth=1, style=plot.style_linebr)

plotshape(buy_signal,           title="Entrada",  style=shape.triangleup,   location=location.belowbar, color=color.green,  size=size.small)
plotshape(not in_position[1] and in_position[1] == false and in_position, title="DCA", style=shape.circle, location=location.belowbar, color=color.blue, size=size.tiny)

// ============================================================
// PAINEL DE STATUS (canto superior direito)
// ============================================================
var table painel = table.new(position.top_right, 2, 6, bgcolor=color.new(color.black, 60), border_width=1, border_color=color.new(color.gray, 50))

if barstate.islast
    table.cell(painel, 0, 0, "RSI Atual",     text_color=color.white,  text_size=size.small, bgcolor=color.new(color.navy, 40))
    table.cell(painel, 1, 0, str.tostring(rsi_val, "#.##"),
         text_color = rsi_val < rsi_threshold ? color.lime : color.red,
         text_size  = size.small, bgcolor=color.new(color.navy, 40))

    table.cell(painel, 0, 1, "Posição",       text_color=color.white,  text_size=size.small)
    table.cell(painel, 1, 1, in_position ? "✅ SIM" : "⏸ NÃO",
         text_color = in_position ? color.lime : color.gray, text_size=size.small)

    table.cell(painel, 0, 2, "DCA",           text_color=color.white,  text_size=size.small)
    table.cell(painel, 1, 2, str.tostring(dca_count) + " / 2",
         text_color = dca_count > 0 ? color.blue : color.gray, text_size=size.small)

    table.cell(painel, 0, 3, "Trailing",      text_color=color.white,  text_size=size.small)
    table.cell(painel, 1, 3, trailing_active ? "⚡ ATIVO" : "—",
         text_color = trailing_active ? color.yellow : color.gray, text_size=size.small)

    table.cell(painel, 0, 4, "Preço Médio",   text_color=color.white,  text_size=size.small)
    table.cell(painel, 1, 4, in_position ? "$" + str.tostring(avg_price, "#.##") : "—",
         text_color=color.white, text_size=size.small)

    table.cell(painel, 0, 5, "Stop em",       text_color=color.white,  text_size=size.small)
    table.cell(painel, 1, 5, in_position ? "$" + str.tostring(avg_price * (1 - stop_loss_pct/100), "#.##") : "—",
         text_color=color.red, text_size=size.small)
"""
    return pine


def gerar_passo_a_passo(params, nome_arquivo):
    """Gera o passo a passo de uso no TradingView"""
    symbol_clean = params.get("symbol", "BTC/USDT").replace("/", "")
    tf = params.get("timeframe", "15m")

    return f"""
📋 PASSO A PASSO — Como usar no TradingView
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Acesse tradingview.com e faça login

2️⃣  No gráfico, selecione o par correto:
    🔍 Busque por "{symbol_clean}" na barra de pesquisa
    ⏱️  Mude o timeframe para "{tf}" (mesmo do seu robô)

3️⃣  No rodapé do gráfico, clique em "Pine Editor"

4️⃣  Selecione TUDO (Ctrl+A) e DELETE o código atual

5️⃣  Cole o Pine Script do arquivo: {nome_arquivo}

6️⃣  Clique em "Adicionar ao gráfico" (botão azul)

7️⃣  Vá na aba "Strategy Tester" (ao lado do Pine Editor)

8️⃣  Em "Visão Geral" você verá:
    💰 Lucro líquido total
    📊 Número de operações
    ✅ Taxa de acerto (%)
    📉 Drawdown máximo
    ⚖️  Profit Factor

9️⃣  Para testar diferentes períodos:
    📅 Clique no ícone de calendário no topo direito do gráfico
    ↔️  Arraste a barra temporal pra ver mais histórico

🔟  Para ajustar os parâmetros da estratégia:
    ⚙️  Clique na engrenagem ao lado do nome da estratégia no gráfico
    🎛️  Ajuste RSI, DCA, Stop Loss, Trailing conforme quiser
    ✅ Clique em "OK" — o backteste roda automaticamente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  ATENÇÃO: Resultados passados não garantem resultados futuros.
💡  Dica: Teste em pelo menos 6 meses de histórico para ter dados confiáveis.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def main():
    parser = argparse.ArgumentParser(description="Gera Pine Script de backteste a partir de robô Python/Node.js")
    parser.add_argument("--strategy", help="Caminho para strategy.py", default=None)
    parser.add_argument("--bot",      help="Caminho para bot.py ou robot.js", default=None)
    parser.add_argument("--nome",     help="Nome da estratégia", default="MeuRobo")
    parser.add_argument("--tipo",     help="Tipo do robô: python ou nodejs", default="python")
    parser.add_argument("--output",   help="Arquivo de saída .pine", default=None)
    args = parser.parse_args()

    codigo_strategy = ""
    codigo_bot = ""

    if args.strategy and os.path.exists(args.strategy):
        with open(args.strategy, "r", encoding="utf-8") as f:
            codigo_strategy = f.read()
        print(f"✅ strategy.py lido: {args.strategy}")
    else:
        print("⚠️  strategy.py não encontrado — usando parâmetros padrão")

    if args.bot and os.path.exists(args.bot):
        with open(args.bot, "r", encoding="utf-8") as f:
            codigo_bot = f.read()
        print(f"✅ bot.py lido: {args.bot}")
    else:
        print("⚠️  bot.py não encontrado — usando parâmetros padrão")

    if args.tipo == "nodejs":
        params = extrair_parametros_nodejs(codigo_bot)
    else:
        params = extrair_parametros_python(codigo_strategy, codigo_bot)

    print(f"\n📊 Parâmetros detectados:")
    print(json.dumps(params, indent=2, ensure_ascii=False))

    pine_script = gerar_pine_script_python(params, args.nome)

    nome_arquivo = args.output or f"backtest_{args.nome.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pine"
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(pine_script)

    print(f"\n✅ Pine Script gerado: {nome_arquivo}")
    print(gerar_passo_a_passo(params, nome_arquivo))
    print("\n" + "="*60)
    print("📋 PINE SCRIPT GERADO:")
    print("="*60)
    print(pine_script)


if __name__ == "__main__":
    main()
