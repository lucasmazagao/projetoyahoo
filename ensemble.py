# Quando cada modelo tem mais peso (opcional - ajuste dinâmico)

if volatilidade_alta:
    peso_lstm = 0.40      # LSTM lida melhor com caos
    peso_xgboost = 0.35   # XGBoost captura padrões locais
    peso_garch = 0.25     # GARCH lida com volatilidade
    
elif tendencia_clara:
    peso_lstm = 0.30      
    peso_xgboost = 0.30   
    peso_prophet = 0.40 

else:
    peso_lstm = 0.33
    peso_xgboost = 0.33
    peso_prophet = 0.34

'''
┌─────────────────┬──────────────────┬─────────────────┐
│  Memory Master  │  Feature Hunter  │  Trend Prophet   │
│     (LSTM)      │    (XGBoost)     │     (GARCH)      │
├─────────────────┼──────────────────┼─────────────────┤
│ Sequências      │ Indicadores      │ Sazonalidade    │
│ temporais       │ técnicos         │ e tendências    │
├─────────────────┼──────────────────┼─────────────────┤
│ Longo prazo     │ Curto/médio      │ Médio/longo     │
├─────────────────┼──────────────────┼─────────────────┤
│ Não-linear      │ Não-linear       │ Linear+Sazonal  │
├─────────────────┼──────────────────┼─────────────────┤
│ Caixa-preta     │ Interpretável    │ Interpretável   │
└─────────────────┴──────────────────┴─────────────────┘
vamos mudar para lstm xgboost e garch?
'''
