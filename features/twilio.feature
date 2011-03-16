Feature: Twilio
  So that I can entertain myself
  As a user
  I want to call a phone number and create an interactive story

  Scenario: start the adventure
    Given there are a few nodes

    When I receive a phone call
    Then I should get a valid TwiML response
    And it should say "Hello"

    When I follow the redirect
    Then I should get a valid TwiML response

  Scenario: listen to the root node
    Given there is a root node
    And I am on the root node
    Then I should get a valid TwiML response
    And it should tell me the current outcome
    And it should say "create a new choice and outcome."
    And it should say "edit the current choice and outcome."
    And it should ask me for the next choice

  Scenario: you can't edit a node that has children
    Given there are a few nodes
    And I am on the root node
    Then I should get a valid TwiML response
    And it should tell me the current outcome
    And it should say "create a new choice and outcome."
    And it should not say "edit the current choice and outcome."
    And it should ask me for the next choice

  Scenario: listen to the root node and timeout
    Given there are a few nodes
    And I am on the root node
    Then I should get a valid TwiML response
    And it should redirect me to the current node if I haven't made a choice

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "I'm sorry.  I didn't get a response.  Let's try again."

    When I follow the redirect
    Then I should get a valid TwiML response

  Scenario: listen to the root node and enter an invalid entry
    Given there are a few nodes
    When I enter "7" when I am on the root node
    Then I should get a valid TwiML response
    And it should say "7 is not a valid entry."

    When I follow the redirect
    Then I should get a valid TwiML response

  Scenario: navigate to a child node
    Given there are a few nodes
    When I enter "child(1)" when I am on the root node
    Then I should get a valid TwiML response
    And it should play "http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/RE86755b2e4419d1bebfd1677969e53586"

  Scenario: navigate to the parent
    Given there are a few nodes
    When I enter "parent" when I am on the root node's first child
    Then I should get a valid TwiML response
    And it should play "http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/RE48c9b4391d0850546843da3d1c4f1070"

  Scenario: start over
    Given there are a few nodes
    When I enter "start_over" when I am on the root node's first child
    Then I should get a valid TwiML response
    And it should say "Hello"

  Scenario: add a node
    Given there are a few nodes
    When I enter "create_node" when I am on the root node
    Then I should get a valid TwiML response
    And it should say "You are about to create a new choice and outcome."
    And it should say "Take a couple minutes to think about what you will say and press any key when you are ready to continue."

    When I enter "1"
    Then I should get a valid TwiML response
    And it should say "Please record a new choice after the beep.  It may be up to 10 seconds long.  Press any key when you are done."
    And it should record something

    When I record something with the URL "new_choice"
    Then I should get a valid TwiML response
    And it should say "You recorded:"
    And it should play "new_choice"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "continue"
    And it should say "try again"

    When I enter "try_again"
    Then I should get a valid TwiML response
    And it should say "Please record a new choice after the beep.  It may be up to 10 seconds long.  Press any key when you are done."
    And it should record something

    When I record something with the URL "new_choice"
    Then I should get a valid TwiML response
    And it should say "You recorded:"
    And it should play "new_choice"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "continue"
    And it should say "try again"

    When I enter "continue"
    Then I should get a valid TwiML response
    And it should say "Now, record a new outcome after the beep.  It may be up to 60 seconds long.  Press any key when you are done."
    And it should record something

    When I record something with the URL "new_outcome"
    Then I should get a valid TwiML response
    And it should say "You recorded:"
    And it should play "new_outcome"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "continue"
    And it should say "try again"

    When I enter "try_again"
    Then I should get a valid TwiML response
    And it should say "Now, record a new outcome after the beep.  It may be up to 60 seconds long.  Press any key when you are done."
    And it should record something

    When I record something with the URL "new_outcome"
    Then I should get a valid TwiML response
    And it should say "You recorded:"
    And it should play "new_outcome"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "continue"
    And it should say "try again"

    When I enter "continue"
    Then I should get a valid TwiML response
    And it should say "You have created a new choice and outcome."
    And it should say "You can now continue the adventure where you left off."
    And there should be a child of the root node with choice "new_choice" and outcome "new_outcome"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should tell me the current outcome
    And it should say "create a new choice and outcome."

  Scenario: edit a node
    Given there are a few nodes
    When I enter "edit_node" when I am on the root node's first child
    Then I should get a valid TwiML response
    And it should say "You are about to edit the current choice and outcome."
    And it should say "Take a couple minutes to think about what you will say and press any key when you are ready to continue."

    When I enter "1"
    Then I should get a valid TwiML response
    And it should say "Please record a new choice after the beep.  It may be up to 10 seconds long.  Press any key when you are done."
    And it should record something

    When I record something with the URL "new_choice"
    Then I should get a valid TwiML response
    And it should say "You recorded:"
    And it should play "new_choice"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "continue"
    And it should say "try again"

    When I enter "try_again"
    Then I should get a valid TwiML response
    And it should say "Please record a new choice after the beep.  It may be up to 10 seconds long.  Press any key when you are done."
    And it should record something

    When I record something with the URL "new_choice"
    Then I should get a valid TwiML response
    And it should say "You recorded:"
    And it should play "new_choice"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "continue"
    And it should say "try again"

    When I enter "continue"
    Then I should get a valid TwiML response
    And it should say "Now, record a new outcome after the beep.  It may be up to 60 seconds long.  Press any key when you are done."
    And it should record something

    When I record something with the URL "new_outcome"
    Then I should get a valid TwiML response
    And it should say "You recorded:"
    And it should play "new_outcome"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "continue"
    And it should say "try again"

    When I enter "try_again"
    Then I should get a valid TwiML response
    And it should say "Now, record a new outcome after the beep.  It may be up to 60 seconds long.  Press any key when you are done."
    And it should record something

    When I record something with the URL "new_outcome"
    Then I should get a valid TwiML response
    And it should say "You recorded:"
    And it should play "new_outcome"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "continue"
    And it should say "try again"

    When I enter "continue"
    Then I should get a valid TwiML response
    And it should say "You have edited the current choice and outcome."
    And it should say "You can now continue the adventure where you left off."
    And there should be a child of the root node with choice "new_choice" and outcome "new_outcome"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should play "http://api.twilio.com/2010-04-01/Accounts/ACec5bb8f63c52532cb3a8c18a1b2e85b1/Recordings/RE48c9b4391d0850546843da3d1c4f1070"

  Scenario: tell the user more about Teladventure
    Given there is a root node
    And I am on the root node
    Then I should get a valid TwiML response
    And it should say "learn more about Teladventure."

    When I enter "learn_more"
    Then I should get a valid TwiML response
    And it should say "Teladventure was created by"

    When I follow the redirect
    Then I should get a valid TwiML response
    And it should say "Hello"