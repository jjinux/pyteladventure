class Choice(object):

    """This is a little DSL for choices.

        Choice(
            label="root_menu",
            digits="*2",
            view_callback=lambda:
                render_template("play.xml", url=some_url),
            controller_block=lambda:
                redirect(some_url))

    """

    def __init__(self, label, digits, view_callback, controller_callback):
        self.label = str(label)
        self.digits = str(digits)
        self.view_callback = view_callback
        self.controller_callback = controller_callback