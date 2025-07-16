from app.services.user_service import authenticate_admin, User

# Test for user service

def test_authenticate_admin_success():
    user = authenticate_admin("admin", "admin123")
    assert isinstance(user, User)
    assert user.username == "admin"
    assert user.role == "admin"

def test_authenticate_admin_fail():
    user = authenticate_admin("admin", "wrongpassword")
    assert user is None

    user = authenticate_admin("wronguser", "admin123")
    assert user is None
