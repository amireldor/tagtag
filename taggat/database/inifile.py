from configparser import RawConfigParser


class IniFileDatabase:

    TAGS_SECTION_NAME = 'Tags'

    # MD5_SECTION_NAME = 'MD5'  # TODO later, when we track renames, non-blocking md5 etc

    def __init__(self, filepath):
        self.original_filepath = filepath
        self._build_config_parser()
        self.read_config(filepath)

    def _build_config_parser(self):
        self.config_parser = RawConfigParser()
        self.config_parser.optionxform = lambda x: x  # so keys are case sensitive (i.e. filenames)

    def read_config(self, filepath):
        self.config_parser.read(filepath)
        if not self.config_parser.has_section(self.TAGS_SECTION_NAME):
            self.config_parser[self.TAGS_SECTION_NAME] = {}

    def write(self, filepath=None):
        filepath = filepath or self.original_filepath
        with open(filepath, 'wt') as write_to_me:
            self.config_parser.write(write_to_me)

    def tag(self, filepath, tags: [str]):
        self.config_parser[self.TAGS_SECTION_NAME][filepath] = ','.join(tags)

    def merge_tags(self, filepath, tags: [str]):
        existing_tags = self.files[filepath]
        self.tag(filepath, set(existing_tags + tags))

    def clear_tags(self, filepath, clear_tags: [str]):
        existing_tags = self.files[filepath]
        filtered_tags = [tag for tag in existing_tags if tag not in clear_tags]
        self.tag(filepath, filtered_tags)

    @property
    def files(self):
        as_dict = dict(self.config_parser[self.TAGS_SECTION_NAME])
        for key in as_dict:
            as_dict[key] = [value.strip() for value in as_dict[key].split(',')]
        return as_dict
