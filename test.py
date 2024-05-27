import pytest
from user import *
from project import *
import bcrypt


@pytest.fixture(autouse=True)
def setup():
    if not info_dir.exists():
        info_dir.mkdir()
    if not users.exists():
        users_file.write(["email", "username", "password", "account"])
    if not projects.exists():
        projects_file.write(
            ["Id", "Title", "Description", "Leader", "Members"])
    if not duty.exists():
        duty_file.write(["Proj_Id", "ID", "Members", "Title", "Description",
                        "Priority", "Status", "Start", "End", "Comments", "History"])

    yield
    if users.exists():
        users.unlink()
    if projects.exists():
        projects.unlink()
    if duty.exists():
        duty.unlink()
    if info_dir.exists():
        info_dir.rmdir()


@pytest.fixture
def user():
    return User()


@pytest.fixture
def project():
    return Project()


def test_user_initialization(user):
    assert user.email == ""
    assert user.username == ""
    assert user.password == ""
    assert user.account == "active"


def test_make_dir_or_file(user):
    user.make_dir_or_file()
    assert info_dir.exists()
    assert users.exists()


def test_check_email_invalid1(user):
    user.email = "email@test"
    assert user.check_email()


def test_check_email_invalid2(user):
    user.email = "test"
    assert user.check_email()


def test_check_email_invalid3(user):
    user.email = "email@test."
    assert user.check_email()


def test_check_email_valid(user):
    user.email = "email@test.com"
    assert not user.check_email()


def test_check_username_invalid1(user):
    user.username = "abc"
    assert user.check_username()


def test_check_username_invalid2(user):
    user.username = "abc@"
    assert user.check_username()


def test_check_username_invalid3(user):
    user.username = "invalid--username"
    assert user.check_username()


def test_check_username_valid(user):
    user.username = "valid-username"
    assert not user.check_username()


def test_check_password_invalid1(user):
    user.password = "weakpass"
    assert user.check_password()


def test_check_password_invalid2(user):
    user.password = "weakpass2"
    assert user.check_password()


def test_check_password_invalid3(user):
    user.password = "Weak#4"
    assert user.check_password()


def test_check_password_valid(user):
    user.password = "StrongPass3@"
    assert not user.check_password()


def test_hash_password(user):
    password = "StrongPass@5"
    hashed_password = user.hash_password(password)
    assert bcrypt.checkpw(password.encode('utf-8'),
                          hashed_password.encode('utf-8'))


def test_check_pass(user):
    entered_password = "StrongPass@5"
    stored_password = user.hash_password(entered_password)
    assert user.check_pass(entered_password, stored_password)


def test_check_pass_invalid(user):
    entered_password = "IncorrectPassword"
    stored_password = user.hash_password("StrongPass@5")
    assert not user.check_pass(entered_password, stored_password)


def test_valid_sign_up(user):
    email = "email1@test.com"
    password = "ValidPassword@4"
    username = "test_user"
    assert user.sign_up(email, password, username) == "NO exception"


def test_sign_up_invalid_email(user):
    email = "invalid-email"
    password = "ValidPassword@1"
    username = "valid_user"

    with pytest.raises(ValueError) as excinfo:
        user.sign_up(email, password, username)
    assert str(excinfo.value) == invalid_email


def test_sign_up_invalid_username(user):
    email = "email@test.com"
    password = "ValidPassword@1"
    username = "inval!d_user"

    with pytest.raises(ValueError) as ex:
        user.sign_up(email, password, username)
    assert str(ex.value) == invalid_username


def test_sign_up_invalid_password(user):
    email = "email@test.com"
    password = "weakpass1"
    username = "valid_user"

    with pytest.raises(ValueError) as ex:
        user.sign_up(email, password, username)
    assert str(ex.value) == invalid_password


def test_sign_up_duplicate_email(user):
    email = "email@test.com"
    password = "Validpassword@1"
    username1 = "valid_user1"
    username2 = "valid_user2"

    user.sign_up(email, password, username1)

    with pytest.raises(ValueError) as ex:
        user.sign_up(email, password, username2)
    assert str(ex.value) == "This email is already in use."


def test_sign_up_duplicate_username(user):
    email1 = "email1@test.com"
    email2 = "email2@test.com"
    password = "ValidPassword@1"
    username = "Duplicate_User"

    user.sign_up(email1, password, username)

    with pytest.raises(ValueError) as ex:
        user.sign_up(email2, password, username)
    assert str(ex.value) == "This username is already in use."


def test_login_successful(user):
    email = "email@test.com"
    password = "ValidPass@1"
    username = "valid_user"

    user.sign_up(email, password, username)

    assert user.log_in(username, password) == "No exception"


def test_login_invalid_credentials(user):
    email = "email@test.com"
    password = "ValidPass@6"
    username = "valid-user"

    user.sign_up(email, password, username)

    with pytest.raises(ValueError) as ex:
        user.log_in(username, "incorrect_password")
    assert str(ex.value) == "Username or password is wrong."


def test_login_inactive_account(user):
    email = "email9@test.com"
    password = "ValidPassword@7"
    username = "valid_user_a"
    user.account = "deactive"

    user.sign_up(email, password, username)

    with pytest.raises(PermissionError) as ex:
        user.log_in(username, password)
    assert str(ex.value) == "Your account is deactivated."


def test_get_leader_projects(user, project):
    project_id = "1"
    project_title = "Project"
    project_description = "None"
    project_leader = user.username
    project.create(project_id, project_title,
                   project_description, project_leader)

    leader_projects = user.get_leader_projects()

    assert len(leader_projects) == 1
    assert leader_projects[0][0] == project_id
    assert leader_projects[0][1] == project_title
    assert leader_projects[0][2] == project_description
    assert leader_projects[0][3] == project_leader


def test_get_user_projects(user, project):
    project_id = "1"
    project_title = "Project"
    project_description = "None"
    project_leader = "leader_username"

    project.create(project_id, project_title,
                   project_description, project_leader)
    project.add_member_func(user.username, project_id)

    user_projects = user.get_user_projects()

    assert len(user_projects) == 1
    assert user_projects[0][0] == project_id
    assert user_projects[0][1] == project_title
    assert user_projects[0][2] == project_description
    assert user_projects[0][3] == project_leader
