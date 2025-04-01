def test_login(client):
    """Test that you can successfully login."""
    assert client.is_logged_in()


def test_me(client):
    """Test that the me endpoint works."""
    assert client.me() == {
        "Email": "service+manifold@emeraldcloudlab.com",
        "EmailAddress": "service+manifold@emeraldcloudlab.com",
        "Id": "id:n0k9mG8070Mk",
        "Type": "Object.User.Emerald.Developer",
        "Username": "service+manifold",
    }
