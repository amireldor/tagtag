from argparse import ArgumentParser
from taggat.database.inifile import IniFileDatabase  # TODO: later, use magic configs for advanced usages such as cloud storage and all


class CommanLineController():
    DEFAULT_DB_FILENAME = "taggat.db.txt"

    def main(self):
        args = self.parse_args()
        self.db = IniFileDatabase(args.db)

        if args.merge:
            try:
                existing_tags = self.db.files[args.file]
            except KeyError:
                existing_tags = []
            final_tags = set([*args.tags, *existing_tags])
            self.db.tag(args.file, final_tags)

        else:
            self.db.tag(args.file, args.tags)
        
        self.db.write()
            

    def parse_args(self):
        parser = ArgumentParser(description='tag your files using the command-line')
        parser.add_argument("file", help="the file you are tagging")
        parser.add_argument("tags", help="trailing arguments are the tags", nargs='*')
        parser.add_argument("-d", "--db", help="the database to write the tags to", default=self.DEFAULT_DB_FILENAME)
        parser.add_argument('-m', '--merge', help="merge with existing tags", dest='merge', action='store_true')
        parser.add_argument('--no-merge', help="override previous tags", dest='merge', action='store_false')
        parser.set_defaults(merge=False)

        return parser.parse_args()

if __name__ == "__main__":
    CommanLineController().main()
