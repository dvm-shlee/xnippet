import os
import yaml
import shutil
import pytest as pytest_
import xnippet as xnippet_
from pathlib import Path
from xnippet.formatter import IOFormatter


def pytest_configure(config):
    xnippet_.setup_logging(path=Path(__file__).parent / 'logging.yaml')

@pytest_.fixture(scope="session")
def presets(request):
    pytest_dir = Path(__file__).resolve().parent
    cur_path = Path(os.curdir).resolve()
    
    def return_working_directory():
        if os.path.exists('.xnippet'):
            shutil.rmtree('.xnippet')
        os.chdir(cur_path)
        
    request.addfinalizer(return_working_directory)
    
    empty_kwargs = {
        "package_name": "xnippet",
        "package_version": xnippet_.__version__,
        "package__file__": __file__,  # current folder
        "config_path": None,       # in current folder
        "config_filename": 'config.yaml'
    }  # init args
    
    examp_kwargs = {
        "package_name": "xnippet-examp",
        "package_version": xnippet_.__version__,
        "package__file__": pytest_dir,
        "config_path": 'examples',
        "config_filename": 'example_config.yaml'}
    
    return empty_kwargs, examp_kwargs
        

@pytest_.fixture(scope="function")
def default_config():
    with open(Path.resolve(Path(__file__).parents[1] / 'src/xnippet/config/main.yaml'), 'r') as f:
        default_config = yaml.safe_load(f)
    return default_config

@pytest_.fixture(scope='function')
def pytest():
    return pytest_

@pytest_.fixture(scope='function')
def xnippet():
    return xnippet_

@pytest_.fixture(scope='function')
def github_repo():
    return {'repo_url': 'https://github.com/xoani/xnippet.git',
            'path': 'examples/plugin'}
    
@pytest_.fixture(scope='function')
def auth():
    auth = ('token', os.environ["XNIPPET_TOKEN"]) if "XNIPPET_TOKEN" in os.environ.keys() else None
    return auth

@pytest_.fixture(scope='session')
def colored():
    return IOFormatter.colored