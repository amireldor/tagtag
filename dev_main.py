from taggat.database.inifile import IniFileDatabase


db = IniFileDatabase('dev.db.txt')

print("hey", db.files)