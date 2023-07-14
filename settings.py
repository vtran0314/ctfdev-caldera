<<<<<<< HEAD
import pathlib
# import os
import logging
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()

#TOKEN = os.getenv("TOKEN")

BASE_DIR = pathlib.Path(__file__).parent

CALD_DIR = BASE_DIR / "caldera-lightweight"
UBUNTU_DIR = BASE_DIR / "ubuntu"
CALD_CONFIG_DIR = CALD_DIR / "conf"
CONF_FILE = CALD_CONFIG_DIR / "default.yml" 

 
LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
            },
        "standard": {"format": "%(levelname)-10s - %(name)15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            'level' : "WARNING",
            'class' : "logging.StreamHandler",
            'formatter': "standard",
        },
        "file": {
            "level" : "INFO",
            "class" : "logging.FileHandler",
            "filename" : "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },       
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {  
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False 
        },
    },
        "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
}

dictConfig(LOGGING_CONFIG)

=======
import pathlib
# import os
# import logging
from dotenv import load_dotenv
# from logging.config import dictConfig

load_dotenv()

#TOKEN = os.getenv("TOKEN")

BASE_DIR = pathlib.Path(__file__).parent

CALD_DIR = BASE_DIR / "caldera-lightweight"
UBUNTU_DIR = BASE_DIR / "ubuntu"
CALD_CONFIG_DIR = CALD_DIR / "conf"
CONF_FILE = CALD_CONFIG_DIR / "default.yml" 

 
LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
            },
        "standard": {"format": "%(levelname)-10s - %(name)15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            'level' : "WARNING",
            'class' : "logging.StreamHandler",
            'formatter': "standard",
        },
        "file": {
            "level" : "INFO",
            "class" : "logging.FileHandler",
            "filename" : "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },       
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {  
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False 
        },
    },
}

dictConfig(LOGGING_CONFIG)

>>>>>>> 9b668ab823b68ed51a823f5fb70b8c3acb1a87c6
