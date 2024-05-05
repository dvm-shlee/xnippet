import yaml
import pytest as pytest_
import xnippy as xnippy_
from pathlib import Path


@pytest_.fixture(scope="function")
def presets():
    return {'empty': {"package_name": "xnippy", 
                      "package_version": xnippy_.__version__,
                      "package__file__": __file__,
                      "config_path": None,
                      "config_filename": 'xnippy.yaml'},
            'example': {"package_name": "xnippy-live", 
                        "package_version": xnippy_.__version__,
                        "package__file__": __file__,
                        "config_path": None,
                        "config_filename": 'xnippy.yaml'}}

@pytest_.fixture(scope="function")
def config():
    with open(Path.resolve(Path(__file__).parents[1] / 'xnippy/yaml/config.yaml'), 'r') as f:
        config = yaml.safe_load(f)
    return config

@pytest_.fixture(scope='function')
def pytest():
    return pytest_

@pytest_.fixture(scope='function')
def xnippy():
    return xnippy_