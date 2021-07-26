
from importlib.abc import SourceLoader
import logging

from pathlib import Path
from importlib.machinery import SourceFileLoader


logger = logging.getLogger(__name__)


class TargetBase:

    def __init__(self, path:str=None) -> None:

        if not path:
            self._path = Path.cwd()        
        elif path and Path(path).exists():
            self._path = Path(path)
        else:
            raise RuntimeError(f'The path does not exist, {path}')

    @property
    def path(self) -> Path:
        return self._path


class Target(TargetBase):

    def __init__(self, path: str) -> None:
        super().__init__(path=path)
        self._target_path = self._path.joinpath('TARGET')
        logger.info(f'Target path: {self._target_path}')

        target_module = SourceFileLoader('TARGET', str(self._target_path.absolute())).load_module()
        self._metadata = target_module.TARGET

    @property
    def info(self):
        ''' returns target metadata
        '''
        return self._metadata


class TargetScanner(TargetBase):

    def run(self):
        ''' run scanning of targets in path
        '''
        for target_file in self._path.glob("**/TARGET"):
            target_path = target_file.relative_to(self._path).parent 
            yield target_path

        # print('\nDepreacted targets:')
        # for target_file in self._path.glob("**/metadata"):
        #     target_path = target_file.relative_to(self._path).parent 
        #     print(f"- {target_path}")
