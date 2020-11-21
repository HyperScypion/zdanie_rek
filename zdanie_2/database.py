from pony import orm


db = orm.Database()


class ImageDB(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str, unique=True)
    image = orm.Required(bytes, lazy=True)
    red = orm.Required(float)
