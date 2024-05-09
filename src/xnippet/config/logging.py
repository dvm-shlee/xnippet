import os
import logging
import logging.config
import sys
import yaml
from pathlib import Path


def setup(path: Path = None, default_level=logging.INFO, env_key='LOG_CFG'):
    """    
    | Logging Setup
    |
    :param default_path: Logging configuration path
    :param default_level: Default logging level
    :param env_key: Logging config path set in environment variable
    """
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)                
            except Exception as e:
                logging.warning('Error in Logging Configuration. %e', e)
                logging.debug('Using default config.')
                logging.basicConfig(format="%(message)s", level=default_level, stream=sys.stdout)                
    else:
        logging.basicConfig(format="%(message)s", level=default_level, stream=sys.stdout)
        logging.debug('Using default config.')