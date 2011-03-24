from __future__ import with_statement

from flask import url_for, render_template, request, g, Markup, redirect, \
                  session

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

            # This is a little tricky.  I have to pass child to the lambda
            # explicitly.  Closures and loops don't get along.  Otherwise,
            # all the lambdas created in the loop will all refer to the last
            # child.

            view_callback=lambda child=child:
                Markup(render_template("play.xml", url=child["choice"])),
            controller_callback=lambda child=child:
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
                redirect(url_for("edit_node", id=node["id"]))))

    i += 1
    choices.append(Choice(
        label="create_node",
        digits="*%s" % i,
        view_callback=lambda:
            Markup(render_template("say.xml",
                message="create a new choice and outcome.")),
        controller_callback=lambda:
            redirect(url_for("create_node", parent_id=node["id"]))))

    i += 1
    if node["parent_id"] is not None:
        parent = g.model.find(node["parent_id"])
        choices.append(Choice(
            label="parent",
            digits="*%s" % i,
            view_callback=lambda:
                Markup(render_template("say.xml",
                    message="go back a step.")),
            controller_callback=lambda:
                redirect(url_for("show_node", id=parent["id"]))))

    choices.append(Choice(
        label="start_over",
        digits="0",
        view_callback=lambda:
            Markup(render_template("say.xml",
                message="start over.")),
        controller_callback=lambda:
            redirect(url_for("call"))))

    return _get_and_handle_choice(choices=choices, template="show_node.xml",
                                  node=node)


@app.route('/create_node/<int:parent_id>')
def create_node(parent_id):
    assert g.model.find(parent_id)
    session["node"] = dict(parent_id=parent_id)
    return redirect(url_for("create_node_pause"))


@app.route('/create_node_pause', methods=["GET", "POST"])
def create_node_pause():
    return _pause("You are about to create a new choice and outcome.",
                  "create_node_record_choice")


@app.route('/create_node_record_choice', methods=["GET", "POST"])
def create_node_record_choice():
    return _record_node_attr("record_choice.xml", "choice",
                             "create_node_verify_choice")


@app.route('/create_node_verify_choice', methods=["GET", "POST"])
def create_node_verify_choice():
    return _confirm("create_node_record_choice", "create_node_record_outcome")


@app.route('/create_node_record_outcome', methods=["GET", "POST"])
def create_node_record_outcome():
    return _record_node_attr("record_outcome.xml", "outcome",
                             "create_node_verify_outcome")


@app.route('/create_node_verify_outcome', methods=["GET", "POST"])
def create_node_verify_outcome():
    return _confirm("create_node_record_outcome", "create_node_congratulations")


@app.route('/create_node_congratulations')
def create_node_congratulations():
    node = session["node"]
    with g.connection:
        g.model.create_node(node["parent_id"], node["choice"], node["outcome"])
    return _say_message_and_redirect("""
        You have created a new choice and outcome.
        You can now continue the adventure where you left off.
    """, url_for("show_node", id=node["parent_id"]))


def _say_message_and_redirect(message, url):
    """Render a TwiML response containing a message and a redirect."""
    return render_template('say_message_and_redirect.xml', message=message,
                           url=url)


def _find_node():
    """Find the node the user is looking for or the root node."""
    node_id = request.values.get("id")
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
    digits = request.values.get("Digits")
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

def _pause(message, next_view_function):
    """Give the user a chance to think.

    Make sure your view function accepts both GET and POST.

    """
    if request.method == "GET":
        message += """
            Take a couple minutes to think about what you will say and press
            any key when you are ready to continue.
        """
        return render_template("pause.xml", message=message)
    assert request.method == "POST"
    return redirect(url_for(next_view_function))


def _record_node_attr(template, attr_name, next_view_function):
    """Record something and save it to session["node"][attr_name].

    Redirect to next_view_function.  Make sure your view function accepts both
    GET and POST.

    """
    if request.method == "GET":
        return render_template(template)
    assert request.method == "POST"
    recording = session["node"][attr_name] = request.values["RecordingUrl"]
    session.modified = True  # Needed because it's a dict in a dict
    return render_template("play_recording_and_redirect.xml",
        recording=recording, redirect=url_for(next_view_function))


def _confirm(incorrect_view_function, correct_view_function):

    """This is a helper method to confirm something.

    The view function that calls this function shouldn't do anything else.  You
    must take care of saying or playing the thing the user is confirming before
    the user gets to the view function that invokes this method.  Make sure
    your view function accepts both GET and POST.

    """

    choices = [
        Choice(
            label="continue",
            digits="1",
            view_callback=lambda:
                Markup(render_template("say.xml", message="continue.")),
            controller_callback=lambda:
                redirect(url_for(correct_view_function))),

        Choice(
            label="try_again",
            digits="3",
            view_callback=lambda:
                Markup(render_template("say.xml", message="try again.")),
            controller_callback=lambda:
                redirect(url_for(incorrect_view_function)))
    ]

    return _get_and_handle_choice(choices, "gather_one_digit_choice.xml")