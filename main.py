from extratorgeral import extrator_acoes
from extratorhist import extrator_historico
from tickers import tickers_atuais
from processo import process_serie
from features import features_mk1
from log import log_inicio, log_fim, log_inicio_etapa, log_etapa, log_erro, log_info
from ensemble import treino_mk1, estrategia
from backtest import backtest
from validacao import validar


def main():

    log_inicio()

    #1. obtenção dos tickers
    log_inicio_etapa("tickers_atuais")
    try:
        tickers = tickers_atuais()
        log_etapa("tickers_atuais", f"{len(tickers)} tickers obtidos")
    except Exception as e:
        log_erro("tickers_atuais", e)
        log_info("execução interrompida: não foi possível obter os tickers")
        log_fim()
        return
    
    #2. extracao
    log_inicio_etapa("extrator_acoes")
    try:
        extrator_acoes(tickers)
        log_etapa("extrator_acoes")
    except Exception as e:
        log_erro("extrator_acoes", e)

    log_inicio_etapa("extrator_historico")
    try:
        extrator_historico(tickers)
        log_etapa("extrator_historico")
    except Exception as e:
        log_erro("extrator_historico", e)

    #3. limpeza e processamento
    log_inicio_etapa("process_serie")
    try:
        process_serie()
        log_etapa("process_serie")
    except Exception as e:
        log_erro("process_serie", e)

    #4. features
    log_inicio_etapa("features_mk1")
    try:
        features_mk1()
        log_etapa("features_mk1")
    except Exception as e:
        log_erro("features_mk1", e)

    #5. modelos
    log_inicio_etapa("treino_mk1")
    try:
        treino_mk1(tickers)
        log_etapa("treino_mk1")
    except Exception as e:
        log_erro("treino_mk1", e)

    log_inicio_etapa("estrategia")
    try:
        estrategia(tickers)
        log_etapa("estrategia")
    except Exception as e:
        log_erro("estrategia", e)

    #6. backtest
    log_inicio_etapa("backtest")
    try:
        backtest(tickers)
        log_etapa("backtest")
    except Exception as e:
        log_erro("backtest", e)

    #7. validação
    log_inicio_etapa("validar")
    try:
        validar(tickers)
        log_etapa("validar")
    except Exception as e:
        log_erro("validar", e)

    log_fim()


if __name__ == "__main__":
    main()
