from extratorgeral import extrator_acoes
from extratorhist import extrator_historico
from tickers import tickers_atuais
from processo import processamento


def main():
    # fazer o log de execução e problemas

    #1. extração de dados atuais
    tickers = tickers_atuais()
    extrator_acoes(tickers)
    extrator_historico(tickers)

    #2. processamento e limpeza
    processamento()

    #3. modelos e análises
    

if __name__ == "__main__":
    main()