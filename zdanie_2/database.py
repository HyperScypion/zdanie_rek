from pony import orm


db = orm.Database()
db.bind("sqlite", filename="database.sqlite", create_db=True)


class ImageDB(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str, unique=True)
    image = orm.Required(bytes, lazy=True)
    red = orm.Optional(float)


if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
