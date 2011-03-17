"""This contains the models for the application.

I'm keeping it low key for the time being.  I'm not bothering with an ORM.

"""


def query_db(query, args=()):
    """Query the database and return a list of dicts.

    For instance:

        query_db('select * from users where username = ?', [username])

    """
    cur = g.db.execute(query, args)
    rv = {}
    for row in cur.fetchall():
        item = {}
        for idx, value in enumerate(row):
            key = cur.description[idx][0]
            item[key] = value
        rv.append(item)
    return rv


def query_db_for_one_record(query, args=()):
    """Call query_db and return exactly one record as a dict.

    If there isn't exactly one record, raise an IndexError.

    """
    rv = query_db(query, args)
    if len(rv) != 1:
        raise IndexError("Expected exactly one row; %s rows returned" %
                         len(rv))
    return rv[0]