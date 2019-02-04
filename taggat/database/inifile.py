from configparser import RawConfigParser


class IniFileDatabase:

    FILES_SECTION_NAME = 'Files'

    def __init__(self, filepath):
        self._build_config_parser()
        self.read_config(filepath)

    def _build_config_parser(self):
        self.config_parser = RawConfigParser()
        self.config_parser.optionxform = lambda x: x  # so keys are case sensitive (i.e. filenames)

    def read_config(self, filepath):
        self.config_parser.read(filepath)
        if not self.config_parser[self.FILES_SECTION_NAME]:
            self.config_parser[self.FILES_SECTION_NAME] = {}

    def tag(self, filepath, tags: [str]):
        self.config_parser[self.FILES_SECTION_NAME][filepath] = tags.join(',')

    @property
    def files(self):
        as_dict = dict(self.config_parser[self.FILES_SECTION_NAME])
        for key in as_dict:
            as_dict[key] = [value.strip() for value in as_dict[key].split(',')]
        return as_dict
