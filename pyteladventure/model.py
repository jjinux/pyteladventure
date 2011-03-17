"""This contains the models for the application.

I'm keeping it low key for the time being.  I'm not bothering with an ORM.

"""

from pyteladventure import g


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


def delete_all_nodes():
    query_db("DELETE FROM nodes")


def create_a_root_node():
    # It's been a good morning so far.  You woke up before your alarm.  You got in a
    # shower and even managed to find something to eat.  Something inside you tells
    # you this is going to be a great day.  You exit the front door and start
    # singing "I Feel Lucky".  As you close the door, a mysterious, long black
    # limo pulls up to the curb.  The door opens, and a leg confidently steps
    # out onto the curb.

    # XXX I have to return the insert id.
    import pdb
    pdb.set_trace()
    query_db("""
        INSERT INTO nodes (parent_id, choice, outcome, created_at)
        VALUES (NULL, NULL, ?, NOW())
    """, ["http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/RE48c9b4391d0850546843da3d1c4f1070"])


def create_a_few_nodes():
    """Delete all the nodes and create a few for testing or development."""
    delete_all_nodes()
    create_a_root_node()


#     Node.delete_all
#     root = create_a_root_node
#
#     # Ignore the limo and walk nonchalantly toward your car.
#     #
#     # A man dressed in black confidently steps out of the car.  He is wearing dark
#     # sun glasses.  Suddenly you get this overwhelming feeling that you're stuck in
#     # a rerun of the "Matrix", and you half-way expect the man to call you "Mr.
#     # Anderson".  As you get into your car, the man puts his hands on his hip and
#     # stands in the way of your driving off.
#     root.children.create!(:choice  => "http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/REc7b587f57e9fe8c529fa038112a84bfc",
#                           :outcome => "http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/RE86755b2e4419d1bebfd1677969e53586")
#
#     # Approach the car to have a closer look.
#     #
#     # As you approach the car, a woman confidently steps out.  She is tall and
#     # beautiful.  Her Prada stilettos look more expensive than your entire wardrobe.
#     # Her gaze makes you feel as if she is peering deep into your soul.  The look on
#     # her face tells you that this is a woman who is used to getting what she wants.
#     root.children.create!(:choice  => "http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/REba8fcb64c468734ee36a83dad05140b2",
#                           :outcome => "http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/RE7b10cd216a05a938b8d05bb63a1ed393")
#
#
#
#
#
#
#
#
#     id integer primary key autoincrement,
#
#     -- The root node will have parent_id and choice set to NULL.
#     parent_id integer references nodes on delete cascade,
#     choice string,
#
#     outcome string not null,
#     created_at datetime not null
#
#
#     Node.create!(:outcome => "")