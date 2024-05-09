from argparse import ArgumentParser
import yaml

class Commander(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_subparsers(self):
        return self._subparsers
    
    def _load_plugins(self, target):
        pass
    
def setup_cli_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    # Add subparsers based on the YAML configuration
    for cli in config:
        subparser = subparsers.add_parser(cli['name'], help=cli['help'])
        for arg in cli['arguments']:
            kwargs = {
                'help': arg['help'],
                'type': str if 'type' in arg and arg['type'] == 'str' else None,
                'default': arg.get('default'),
                'action': arg.get('action', None)
            }
            if 'long_name' in arg:
                subparser.add_argument(arg['name'], arg['long_name'], **kwargs)
            else:
                subparser.add_argument(arg['name'], **kwargs)

if __name__ == '__main__':
    setup_cli_from_yaml('cli_config.yaml')
