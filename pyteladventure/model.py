class Model(object):

    """This class contains the model for the application.

    I'm keeping it low key for the time being.  I'm not bothering with an ORM.

    This class wraps up various queries, but it doesn't manage transactions for
    you.  That's because you might want to wrap multiple method calls in a
    single transaction.  Furthermore, if you don't handle your own transactions,
    all the changes you make will rollback.  The best way to handle
    transactions is to use the connection as a context:

        from __future__ import with_statement

        with connection:
            model.some_method()

    """

    def __init__(self, cursor):
        """Accept an open cursor for the database."""
        self._cursor = cursor

    def _query_db(self, query, args=()):
        """Query the database and return a list of dicts.

        For instance:

            _query_db('select * from users where username = ?', [username])

        """
        cur = self._cursor.execute(query, args)
        rv = []
        for row in cur.fetchall():
            item = {}
            for idx, value in enumerate(row):
                key = cur.description[idx][0]
                item[key] = value
            rv.append(item)
        return rv

    def _query_db_for_one_record(self, query, args=()):
        """Call _query_db and return exactly one record as a dict.

        If there isn't exactly one record, raise an IndexError.

        """
        rv = self._query_db(query, args)
        if len(rv) != 1:
            raise IndexError("Expected exactly one row; %s rows returned" %
                             len(rv))
        return rv[0]

    def delete_all_nodes(self):
        self._query_db("DELETE FROM nodes")

    def create_node(self, parent_id, choice, outcome):
        """Create a node.  Return its id."""
        self._query_db("""
            INSERT INTO nodes (parent_id, choice, outcome, created_at)
            VALUES (?, ?, ?, DATETIME('now'))
        """, [parent_id, choice, outcome])
        assert self._cursor.lastrowid > 0
        return self._cursor.lastrowid

    def update_node(self, node_id, choice, outcome):
        self._query_db("""
            UPDATE nodes
            SET choice = ?, outcome = ?
            WHERE id = ?
        """, [choice, outcome, node_id])

    def create_root_node(self):

        """Create a root node.  Return its id."""

        # It's been a good morning so far.  You woke up before your alarm.  You got in a
        # shower and even managed to find something to eat.  Something inside you tells
        # you this is going to be a great day.  You exit the front door and start
        # singing "I Feel Lucky".  As you close the door, a mysterious, long black
        # limo pulls up to the curb.  The door opens, and a leg confidently steps
        # out onto the curb.

        return self.create_node(parent_id=None, choice=None,
            outcome="http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/RE48c9b4391d0850546843da3d1c4f1070")

    def create_a_few_nodes(self):

        """Delete all the nodes and create a few for testing or development."""

        self.delete_all_nodes()
        root_node_id = self.create_root_node()

        # Ignore the limo and walk nonchalantly toward your car.
        #
        # A man dressed in black confidently steps out of the car.  He is wearing dark
        # sun glasses.  Suddenly you get this overwhelming feeling that you're stuck in
        # a rerun of the "Matrix", and you half-way expect the man to call you "Mr.
        # Anderson".  As you get into your car, the man puts his hands on his hip and
        # stands in the way of your driving off.

        self.create_node(
            parent_id=root_node_id,
            choice="http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/REc7b587f57e9fe8c529fa038112a84bfc",
            outcome="http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/RE86755b2e4419d1bebfd1677969e53586")

        # Approach the car to have a closer look.
        #
        # As you approach the car, a woman confidently steps out.  She is tall and
        # beautiful.  Her Prada stilettos look more expensive than your entire wardrobe.
        # Her gaze makes you feel as if she is peering deep into your soul.  The look on
        # her face tells you that this is a woman who is used to getting what she wants.

        self.create_node(
            parent_id=root_node_id,
            choice="http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/REba8fcb64c468734ee36a83dad05140b2",
            outcome="http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/RE7b10cd216a05a938b8d05bb63a1ed393")

    def find_root_node(self):
        """Find and return the root node.

        This may raise IndexError.

        """
        return self._query_db_for_one_record(
            "SELECT * FROM nodes WHERE parent_id IS NULL")

    def find(self, id):
        """Find and return a node given its id.

        This may raise IndexError.

        """
        return self._query_db_for_one_record(
            "SELECT * FROM nodes WHERE id = ?", (id,))

    def find_children(self, node_id):
        """Find the children of the given node."""
        assert node_id > 0
        return self._query_db("""
            SELECT * FROM nodes
            WHERE parent_id = ?
            ORDER BY created_at, id
        """, (node_id,))

    def find_child_by_choice_and_outcome(self, parent_id, choice, outcome):
        """Find a child of the parent node with the given choice and outcome.

        Raise an IndexError if there is none.

        """
        return self._query_db_for_one_record("""
            SELECT * FROM nodes
            WHERE parent_id = ?
            AND choice = ?
            AND outcome = ?
        """, (parent_id, choice, outcome))