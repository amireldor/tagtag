from argparse import ArgumentParser
from taggat.database.inifile import IniFileDatabase  # TODO: later, use magic configs for advanced usages such as cloud storage and all


class CommanLineController():
    DEFAULT_DB_FILENAME = "taggat.db.txt"

    def main(self):
        self.args = self.parse_args()
        self.db = IniFileDatabase(self.args.db)
        self.update_tags()
        self.db.write()

    def parse_args(self):
        parser = ArgumentParser(description='tag your files using the command-line')
        parser.add_argument("file", help="the file you are tagging")
        parser.add_argument("tags", help="trailing arguments are the tags. No tags will print existing tags and quit", nargs='*')
        parser.add_argument("-d", "--db", help="the database to write the tags to", default=self.DEFAULT_DB_FILENAME)
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-m', '--merge', help="merge with existing tags", dest='merge', action='store_true')
        group.add_argument('--no-merge', help="override previous tags", dest='merge', action='store_false')
        group.add_argument('-r', '--remove', help="remove these tags", dest='remove', action='store_true')
        parser.set_defaults(merge=False, remove=False)
        return parser.parse_args()

    def update_tags(self):
        if len(self.args.tags) == 0:
            print(','.join(self.get_existing_tags()))
        elif self.args.remove:
            self.remove_tags()
        elif self.args.merge:
            self.merge_with_existing_tags()
        else:
            self.db.tag(self.args.file, self.args.tags)

    def remove_tags(self):
        existing_tags = self.get_existing_tags()
        # TODO: support `-r *` to remove all tags
        filtered_tags = [tag for tag in existing_tags if tag not in self.args.tags]
        self.db.tag(self.args.file, filtered_tags)

    def merge_with_existing_tags(self):
        existing_tags = self.get_existing_tags()
        final_tags = set([*self.args.tags, *existing_tags])
        self.db.tag(self.args.file, final_tags)

    def get_existing_tags(self):
        try:
            return self.db.files[self.args.file]
        except KeyError:
            return []


if __name__ == "__main__":
    CommanLineController().main()
