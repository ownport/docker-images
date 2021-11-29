
import logging
from pathlib import Path

from yaml import safe_load as yaml_load

logger = logging.getLogger(__name__) 


class Settings:
    ''' Builder Settings
    '''
    def __init__(self, path:str = '.builder.yml') -> None:
        path = Path(path).absolute()
        if not path.exists():
            raise RuntimeError(f'The settings file does not exist, {path}')
        
        self._settings = None
        with open(path, 'r') as settings_file:
            self._settings = yaml_load(settings_file)
    
    def get(self, name:str, default:object) -> object:
        ''' return parameter value by name 
        '''
        return self._settings.get(name, default)
