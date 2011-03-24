from flask import url_for, render_template, request, g, Markup, redirect

from pyteladventure import app
from pyteladventure.choice import Choice


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/call')
def call():
    return _say_message_and_redirect("""
        Hello.
        Teladventure is an interactive, phone-based adventure game.
        You play Teladventure not just by exploring the story, but also by adding to it.
        Let's get started.
    """, url_for('show_node'))


@app.route('/show_node', methods=["GET", "POST"])
def show_node():
    node = _find_node()
    choices = []
    children = g.model.find_children(node["id"])

    for i, child in enumerate(children):
        choices.append(Choice(
            label="child(%s)" % (i + 1),
            digits=(i + 1),
            view_callback=lambda:
                Markup(render_template("play.xml", url=child["choice"])),
            controller_callback=lambda:
                redirect(url_for('show_node', id=child["id"]))))

    # It's too confusing if people edit a parent node because usually they'll
    # break the stories in the child nodes.

    i = 1
    if not children:
        choices.append(Choice(
            label="edit_node",
            digits="*%s" % i,
            view_callback=lambda:
                Markup(render_template("say.xml",
                    message="edit the current choice and outcome.")),
            controller_callback=lambda:
                redirect("edit_node", id=node["id"])))

    i += 1
    choices.append(Choice(
        label="create_node",
        digits="*%s" % i,
        view_callback=lambda:
            Markup(render_template("say.xml",
                message="create a new choice and outcome.")),
        controller_callback=lambda:
            redirect("create_node", parent_id=node["id"])))

    return _get_and_handle_choice(choices=choices, template="show_node.xml",
                                  node=node)


def _say_message_and_redirect(message, url):
    """Render a TwiML response containing a message and a redirect."""
    return render_template('say_message_and_redirect.xml', message=message,
                           url=url)


def _find_node():
    """Find the node the user is looking for or the root node."""
    node_id = request.form.get("id")
    if node_id is None:
        return g.model.find_root_node()
    else:
        return g.model.find(node_id)


def _get_and_handle_choice(choices, template, **template_kargs):
    """Either ask the user for a choice or respond to his choice.
    
    This responds to GETs and POSTs and makes use of _handle_choice.
    
    """
    if request.method == "GET":
        return render_template(template, choices=choices, **template_kargs)
    elif request.method == "POST":
        return _handle_choice(choices)
    else:
        raise ValueError


def _handle_choice(choices):
    """Respond to the user's choice.
    
    Handle errors such as timeouts and invalid digits.
    
    """
    digits = request.form.get("Digits")
    if digits is None:
        return _say_message_and_redirect(
            "I'm sorry.  I didn't get a response.  Let's try again.",
            request.url)
    for choice in choices:
        if digits in (choice.label, choice.digits):
            return choice.controller_callback()
    return _say_message_and_redirect(
        "%s is not a valid entry.  Let's try again." % digits,
        request.url)