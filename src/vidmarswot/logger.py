import logging

class Logger:
    def __init__(self, log_file='agent_watch.log'):
        # Configurar o logger
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)  # Cria uma instância de logger

    def log_info(self, message: str):
        """Registra uma mensagem de nível INFO."""
        self.logger.info(message)

    def log_error(self, message: str):
        """Registra uma mensagem de nível ERROR."""
        self.logger.error(message)

    def log_debug(self, message: str):
        """Registra uma mensagem de nível DEBUG."""
        self.logger.debug(message)

# Exemplo de uso:
# logger = Logger()
# logger.log_info("Este é um log de informação.")
# logger.log_error("Este é um log de erro.")
