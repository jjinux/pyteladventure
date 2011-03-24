class Choice(object):

    """This is a little DSL for choices.

    It allows me to succinctly capture a choice that the user might select
    such as "Press 9 in order to..."

    label
        This is a "friendly" name for the choice.  It's used in the tests
        so that I don't have to hardcode magical numbers.

    digits
        This is what the user has to actually type in on his phone.

    view_callback
        This callback is called when the list of options is being given to
        the user.  It should play or say something.

    controller_callback
        This callback is called when the user selects a given option.
        Generally you should just redirect the user somewhere.

    Example:

        Choice(
            label="root_menu",
            digits="*2",
            view_callback=lambda:
                Markup(render_template("play.xml", url=some_url)),
            controller_callback=lambda:
                redirect(some_url))

    Warning about Closures
    ----------------------

    Be careful about code like:

        for i in xrange(10):
            ...lambda: f(i)

    The i will always be 9, even though you might expect each lambda to have
    its own version of i.  Try this instead:

        for i in xrange(10):
            ...lambda i=i: f(i)

    """

    def __init__(self, label, digits, view_callback, controller_callback):
        self.label = str(label)
        self.digits = str(digits)
        self.view_callback = view_callback
        self.controller_callback = controller_callback