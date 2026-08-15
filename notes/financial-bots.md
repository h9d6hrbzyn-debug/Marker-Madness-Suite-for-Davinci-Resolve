# Financial Bots — Idea Note

Two bot concepts, captured 2026-08-15.

## 1. Food Commodities Bot

Trades food/agricultural commodities. Scope not yet pinned down.

Open questions:
- Which markets — grains (corn, wheat, soybeans), softs (coffee, sugar, cocoa),
  livestock, or all of them?
- Futures directly, or commodity ETFs?
- What's the signal — seasonality, weather, inventory/USDA reports, momentum?

## 2. Inverse Bot — Short High-P/E Stocks

Shorts stocks with a P/E ratio over 25. "Inverse" was the working name, i.e.
the short side counterpart to the long strategies.

Open questions:
- P/E > 25 on its own is a very wide net — a large share of the S&P sits above
  it, and plenty of those are high-growth names that keep running. Probably
  needs a second filter (declining revenue, sector-relative P/E, negative
  momentum, debt load) to be a real screen rather than a market-wide short.
- Trailing or forward P/E? Companies with no earnings (undefined/negative P/E)
  need an explicit rule.
- Direct shorts, put options, or inverse ETFs?
- Rebalance cadence and position sizing.

## To Confirm

Whether "inverse" was the name of bot #2 or a separate third idea. Noted here
as the name of #2.
