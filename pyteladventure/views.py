from flask import url_for, render_template, request, g

from pyteladventure import app


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
    return 'Hello World!'


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