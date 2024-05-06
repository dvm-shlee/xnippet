import os
import yaml
import logging
import shutil
import pytest as pytest_
import xnippet as xnippet_
from pathlib import Path


def pytest_configure(config):
    # Configure the root logger
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Optionally, you can configure logging to a file instead of the console
    # logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest_.fixture(scope="session")
def presets(request):
    os.chdir('tests')
    def return_working_directory():
        if os.path.exists('.xnippet'):
            shutil.rmtree('.xnippet')
        os.chdir('..')
        
    request.addfinalizer(return_working_directory)
    
    return {'empty': {"package_name": "xnippet", 
                      "package_version": xnippet_.__version__,
                      "package__file__": __file__,
                      "config_path": None,
                      "config_filename": 'config_for_test.yaml'},
            'example': {"package_name": "xnippet-live", 
                        "package_version": xnippet_.__version__,
                        "package__file__": Path(xnippet_.__file__).parent,
                        "config_path": 'examples',
                        "config_filename": 'example_config.yaml'}}
    
        

@pytest_.fixture(scope="function")
def default_config():
    with open(Path.resolve(Path(__file__).parents[1] / 'xnippet/yaml/config.yaml'), 'r') as f:
        default_config = yaml.safe_load(f)
    return default_config

@pytest_.fixture(scope='function')
def pytest():
    return pytest_

@pytest_.fixture(scope='function')
def xnippet():
    return xnippet_