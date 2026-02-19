import logging
from pathlib import Path
from datetime import datetime

# Nome do arquivo com data/hora
_arquivo_log = f'logs/exec_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

# Configurar logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(_arquivo_log, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('projetoyahoo')

# ============================================================
# FUNÇÕES DE LOG (usar na main.py)
# ============================================================

def log_inicio():
    """Chama no início da execução"""
    logger.info("=" * 50)
    logger.info("INÍCIO DA EXECUÇÃO")
    logger.info(f"Log salvo em: {_arquivo_log}")
    logger.info("=" * 50)

def log_fim():
    """Chama no final da execução"""
    logger.info("=" * 50)
    logger.info("FIM DA EXECUÇÃO")
    logger.info("=" * 50)

def log_etapa(nome: str, detalhe: str = None):
    """Registra uma etapa concluída
    
    Uso:
        log_etapa("extrator_acoes")
        log_etapa("tickers", "503 encontrados")
    """
    if detalhe:
        logger.info(f"✔ {nome} — {detalhe}")
    else:
        logger.info(f"✔ {nome}")

def log_erro(nome: str, erro: Exception):
    """Registra um erro
    
    Uso:
        except Exception as e:
            log_erro("extrator_acoes", e)
    """
    logger.error(f"✖ {nome} — {erro}")

def log_aviso(mensagem: str):
    """Registra um aviso (não fatal)
    
    Uso:
        log_aviso("Ticker BRK.B não encontrado, pulando")
    """
    logger.warning(f"⚠ {mensagem}")

def log_info(mensagem: str):
    """Registra informação genérica
    
    Uso:
        log_info("Iniciando extração...")
    """
    logger.info(mensagem)