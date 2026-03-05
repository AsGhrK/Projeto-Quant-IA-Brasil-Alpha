import time
from threading import Thread
from scripts.collect_all import run_collection

INTERVAL = 60 * 15  # 15 minutos

def _scheduler_loop(interval=INTERVAL):
    """Loop interno que chama run_collection a cada intervalo."""
    while True:
        print("Iniciando coleta...")
        try:
            run_collection()
        except Exception as e:
            print(f"Erro na coleta: {e}")
        print("Aguardando próxima execução...\n")
        time.sleep(interval)


def start_scheduler(interval=INTERVAL, daemon=True):
    """
    Inicia o scheduler de coleta automática em background.

    Args:
        interval (int): Intervalo em segundos entre coletas.
        daemon (bool): Se o thread é daemon.
    """
    """Inicia o scheduler em um thread separado.

    Chamado por aplicações (como o Streamlit) para manter o banco atualizado.
    """
    thread = Thread(target=_scheduler_loop, args=(interval,), daemon=daemon)
    thread.start()
    return thread

if __name__ == "__main__":
    # permite execução direta para teste
    _scheduler_loop()
