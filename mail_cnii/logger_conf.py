
import logging.config
LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # точный формат не важен, это минимальная информация
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'file':{
            'level':'INFO',
            'class': 'logging.FileHandler',
            'filename': '/tmp/1',
        }
        # Добавить обработчик для Sentry для `warning` и выше
    },
    'loggers': {
    # корневой логгер
        'mail': {
            'level': 'INFO',
            'handlers': ['file'],
         
            'propagate': True,
        },
    },
})