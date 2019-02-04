from taggat.database.inifile import IniFileDatabase


db = IniFileDatabase('dev.db.txt')

print("hey", db.files)

db.tag("destiny.txt", ['song', 'bad lyrics', 'heavy metal'])
db.write()
