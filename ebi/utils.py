from functools import reduce
from tempfile import NamedTemporaryFile

import yaml


class TemporaryMergedYaml:
    def __init__(self, yaml_paths):
        configs = [
            self.__read_yaml(yaml_path)
            for yaml_path in yaml_paths
        ]
        self.config = self.__merge(configs)
        self.tempfile = self.__init_tempfile(self.config)

    def __enter__(self):
        return self.tempfile

    def __exit__(self, *a):
        self.tempfile.close()

    def close(self):
        self.tempfile.close()

    @staticmethod
    def __init_tempfile(config):
        tempfile = NamedTemporaryFile(suffix='.yaml')
        dumped = yaml.dump(config).encode('utf-8')
        tempfile.write(dumped)
        tempfile.flush()
        return tempfile

    @staticmethod
    def __read_yaml(path):
        with open(path) as yaml_file:
            body = yaml_file.read()
            return yaml.load(body)

    @staticmethod
    def __merge(dicts):
        return reduce(lambda a, b: a.update(b) or a, dicts, {})
