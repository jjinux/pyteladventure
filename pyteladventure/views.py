from flask import url_for, render_template, request, g, Markup

from pyteladventure import app
from pyteladventure.choice import Choice


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/call')
def call():
    return say_message_and_redirect("""
        Hello.
        Teladventure is an interactive, phone-based adventure game.
        You play Teladventure not just by exploring the story, but also by adding to it.
        Let's get started.
    """, url_for('show_node'))


@app.route('/show_node')
def show_node():
    node = find_node()
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

    return render_template("show_node.xml", node=node, choices=choices)


def say_message_and_redirect(message, url):
    """Render a TwiML response containing a message and a redirect."""
    return render_template('say_message_and_redirect.xml', message=message,
                           url=url)


def find_node():
    """Find the node the user is looking for or the root node."""
    node_id = request.form.get("id")
    if node_id is None:
        return g.model.find_root_node()
    else:
        return g.model.find(node_id)