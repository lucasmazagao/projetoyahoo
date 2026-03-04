import logging
import time
from pathlib import Path
from datetime import datetime

Path('logs').mkdir(exist_ok=True)
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

# Armazena tempos de início das etapas para calcular duração
_tempos: dict[str, float] = {}

def log_inicio():
    _tempos['__execucao__'] = time.perf_counter()
    logger.info(f"Execução Inicial — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


def log_fim():
    duracao = time.perf_counter() - _tempos.get('__execucao__', time.perf_counter())
    logger.info(f"Execução Final — tempo total: {duracao:.1f}s")


def log_inicio_etapa(nome: str):
    _tempos[nome] = time.perf_counter()
    logger.info(f"{nome} — iniciado")


def log_etapa(nome: str, detalhe: str = None):
    duracao = ""
    if nome in _tempos:
        elapsed = time.perf_counter() - _tempos.pop(nome)
        duracao = f" ({elapsed:.1f}s)"

    msg = f"{nome}{duracao}"
    
    if detalhe:
        msg += f" — {detalhe}"
    logger.info(msg)


def log_erro(nome: str, erro: Exception):
    _tempos.pop(nome, None)
    logger.error(f"{nome} — {type(erro).__name__}: {erro}")


def log_aviso(mensagem: str):
    logger.warning(f"{mensagem}")


def log_info(mensagem: str):
    logger.info(f"{mensagem}")