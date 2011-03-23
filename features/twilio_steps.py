from __future__ import with_statement

import os
from tempfile import mkstemp

from lettuce import step, before, after, world
from lxml import etree
from nose.tools import assert_true, assert_equal

import pyteladventure


@before.each_scenario
def before_each_scenario(scenario):
    from pyteladventure.model import Model  # Import late.
    world._db_fd, pyteladventure.app.config['DATABASE'] = mkstemp()
    world.app = pyteladventure.app.test_client()
    pyteladventure.init_db()
    world.connection = pyteladventure.connect_db()
    world._cursor = world.connection.cursor()
    world.model = Model(world._cursor)


@after.each_scenario
def after_each_scenario(scenario):
    os.close(world._db_fd)
    os.unlink(pyteladventure.DATABASE)


def print_world_response_data():
    print "world.response.data:"
    print world.response.data


@step(u'When I (GET|POST) "(/.*)"')
def when_i_open_path(step, method, path):
    world.response = world.app.open('/', method=method)


@step(u'Then I should see "(.*)"')
def then_i_should_see_string(step, string):
    assert_true(string in world.response.data)


@step(u'When I receive a phone call')
def when_i_receive_a_phone_call(step):
    world.response = world.app.get('/call')


@step(u'Then I should get a valid TwiML response')
def then_i_should_get_a_valid_twiml_response(step):
    assert_equal(world.response.status, '200 OK')
    try:
        world.root = etree.XML(world.response.data)
    except etree.XMLSyntaxError, e:
        print_world_response_data()
        raise e
    assert_equal(len(world.root.xpath("/Response")), 1)


@step(u'(Then|And) it should (not |)(say|play) "([^"]*)"')
def then_it_should_say_or_play_string(step, then_or_and, not_or_blank,
                                      verb, msg):
    any_matches = False
    expected_matches = (not_or_blank == "")
    tag = verb.title()
    for node in world.root.xpath("//%s" % tag):
        if msg in node.text:
            any_matches = True
    try:
        assert_equal(any_matches, expected_matches)
    except AssertionError, e:
        print_world_response_data()
        raise e


@step(u'When I follow the redirect')
def when_i_follow_the_redirect(step):
    redirect = world.root.xpath("/Response/Redirect")[0]
    world.response = world.app.open(redirect.text,
                                    method=redirect.attrib['method'])


@step(u'Given there are a few nodes')
def given_there_are_a_few_nodes(step):
    with world.connection:
        world.model.create_a_few_nodes()


@step(u'Given there is a root node')
def given_there_is_a_root_node(step):
    with world.connection:
        world.model.create_root_node()


@step(u'And I am on the root node')
def and_i_am_on_the_root_node(step):
    world.response = world.app.get('/show_node')


@step(u'And it should tell me the current outcome')
def and_it_should_tell_me_the_current_outcome(step):
    assert world.root.xpath("/Response/Gather/Play")


@step(u'And it should ask me for the next choice')
def and_it_should_ask_me_for_the_next_choice(step):
    assert world.root.xpath("/Response/Gather")


@step(u'And it should redirect me to the current node if I haven\'t made a choice')
def and_it_should_redirect_me_to_the_current_node_if_i_haven_t_made_a_choice(step):
    assert False, 'This step must be implemented'


@step(u'When I enter "(.*)" when I am on the root node')
def when_i_enter_group1_when_i_am_on_the_root_node(step, group1):
    assert False, 'This step must be implemented'


@step(u'When I enter "(.*)" when I am on the root node\'s first child')
def when_i_enter_group1_when_i_am_on_the_root_node_s_first_child(step, group1):
    assert False, 'This step must be implemented'


@step(u'When I enter "(.*)"')
def when_i_enter_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'And it should record something')
def and_it_should_record_something(step):
    assert False, 'This step must be implemented'


@step(u'When I record something with the URL "(.*)"')
def when_i_record_something_with_the_url_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'And there should be a child of the root node with choice "(.*)" and outcome "(.*)"')
def and_there_should_be_a_child_of_the_root_node_with_choice_group1_and_outcome_group2(step, group1, group2):
    assert False, 'This step must be implemented'


# XXX This is the code that I partially converted to Python.
#
# from lettuce import step
#
#
# @step(u'I should get a valid TwiML response')
# def should_get_a_valid_twiml_response():
#     assert_equal(world.response.status, 200)
#     world.root = etree.XML(world.content)
#     assert_equal(len(world.root.xpath("/Response")), 1)
#
#
# @step(u'I enter "([^"]*)"')
# def enter_digits(digits):
#     gather = world.root.xpath("/Response/Gather").first
#     assert gather
#     world.http.request(gather['action'], sanitize_method(gather['method']), {'Digits': digits})
#
#
# @step(u'I record something with the URL "([^"]*)"')
# def record_something_with_the_url(url):
#     record = world.root.xpath("/Response/Record").first
#     assert record
#     world.http.request(record['action'], sanitize_method(record['method']), {'RecordingUrl': url})
#
#
# @step(u'it should record something')
# def should_record_something():
#     assert world.root.xpath("/Response/Record")
#
#
# @step(u'it should redirect me if I time out')
# def should_redirect_me_if_i_time_out():
#     assert world.root.xpath("/Response/Redirect")
#
#
# @step(u'there are a few nodes')
# def there_are_a_few_nodes():
#     Node.create_a_few_nodes
#
#
# @step(u'it should redirect me to the current node if I haven\'t made a choice')
# def should_redirect_me_to_the_current_node_if_i_havent_made_a_choice():
#     world.root.xpath("/Response/Redirect").should_not be_empty
#
#
# @step(u'I enter "([^"]*)" when I am on the root node'):
# def enter_digits_when_i_am_on_the_root_node(digits):
#     post_via_redirect url_for('controller': 'twilio', 'action': 'show_node', 'Digits': digits)
#
#
# @step(u'I enter "([^"]*)" when I am on the root node\'s first child')
# def enter_digits_when_i_am_on_the_root_nodes_first_child(digits):
#     id = Node.root.children.first.id
#     post_via_redirect url_for('controller': 'twilio', 'action': 'show_node', 'id': id, 'Digits': digits)
#
#
# @step(u'there should be a child of the root node with choice "([^"]*)" and outcome "([^"]*)"')
# def should_be_a_child_of_the_root_node_with_choice_and_outcome(choice, outcome):
#     Node.root.children.find_by_choice_and_outcome(choice, outcome).should_not be_nil
