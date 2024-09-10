import logging

# Создание логгера
logger = logging.getLogger(__name__)

# Установка уровня логирования
logger.setLevel(logging.DEBUG)

# Создание обработчика консоли
ch = logging.StreamHandler()

# Установка формата логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(ch)
