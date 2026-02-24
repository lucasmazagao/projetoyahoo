from extratorgeral import extrator_acoes
from extratorhist import extrator_historico
from tickers import tickers_atuais
from processo import process_serie
from features import features_mk1
from log import log_inicio, log_etapa, log_info
from ensemble import treino_mk1


def main():

    ''' criar algo tipo assim no futuro pro log nao ficar baguncado
    etapas = [
        "Início da execução",
        "Extração de tickers atuais",
        "Extração de dados históricos",
        "Processamento e limpeza",
        "Criação de features",
        "Modelos e análises"
    ]
    log_inicio()

    for etapa in etapas:
        log_etapa(etapa)
        log_info(f"executando {etapa}...") etc
    
    '''

    # fazer o log de execução e problemas no futuro
    log_inicio()
    
    #1. extração de dados atuais
    tickers = tickers_atuais()
    extrator_acoes(tickers)
    extrator_historico(tickers)

    #2. processamento e limpeza

    # vai limpar dados, gerar df_ohlcv
    process_serie()

    # criação de features para modelos
    
    features_mk1()
    # create_features_2()

    #3. modelos e análises
    treino_mk1(tickers)
    

if __name__ == "__main__":
    main()