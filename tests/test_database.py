def test_user_conversation_and_message(repo):
    user = repo.get_or_create_user("alice")
    conversation = repo.create_conversation(user.id, "Test")
    assert repo.get_conversation(user.id, conversation.id).title == "Test"
    repo.add_message(conversation.id, "user", "Hello")
    assert repo.messages(conversation.id)[0].content == "Hello"
def test_user_isolation(repo):
    alice = repo.get_or_create_user("alice"); bob = repo.get_or_create_user("bob")
    conversation = repo.create_conversation(alice.id)
    assert repo.get_conversation(bob.id, conversation.id) is None

