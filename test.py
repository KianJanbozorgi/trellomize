import pytest
from user import *
from project import *
import bcrypt


# Fixture for setting up the environment
@pytest.fixture(autouse=True)
def setup():
    # Ensure necessary directories and files exist
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

    # Clean up after tests
    if users.exists():
        users.unlink()
    if projects.exists():
        projects.unlink()
    if duty.exists():
        duty.unlink()
    if info_dir.exists():
        info_dir.rmdir()

# Fixture for creating a User instance
@pytest.fixture
def user():
    return User()

# Fixture for creating a Project instance
@pytest.fixture
def project():
    return Project()


def test_user_initialization(user):
    """Test the initial state of a new User instance."""
    assert user.email == ""
    assert user.username == ""
    assert user.password == ""
    assert user.account == "active"


def test_make_dir_or_file(user):
    """Test if the necessary directories and files are created."""
    user.make_dir_or_file()
    assert info_dir.exists()
    assert users.exists()


def test_check_email_invalid1(user):
    """Test invalid email format."""
    user.email = "email@test"
    assert user.check_email()


def test_check_email_invalid2(user):
    """Test another invalid email format."""
    user.email = "test"
    assert user.check_email()


def test_check_email_invalid3(user):
    """Test yet another invalid email format."""
    user.email = "email@test."
    assert user.check_email()


def test_check_email_valid(user):
    """Test valid email format."""
    user.email = "email@test.com"
    assert not user.check_email()


def test_check_username_invalid1(user):
    """Test invalid username format (too short)."""
    user.username = "abc"
    assert user.check_username()


def test_check_username_invalid2(user):
    """Test invalid username format (contains invalid character)."""
    user.username = "abc@"
    assert user.check_username()


def test_check_username_invalid3(user):
    """Test invalid username format (contains double hyphen)."""
    user.username = "invalid--username"
    assert user.check_username()


def test_check_username_valid(user):
    """Test valid username format."""
    user.username = "valid-username"
    assert not user.check_username()


def test_check_password_invalid1(user):
    """Test invalid password format (too weak)."""
    user.password = "weakpass"
    assert user.check_password()


def test_check_password_invalid2(user):
    """Test invalid password format (contains no special character)."""
    user.password = "weakpass2"
    assert user.check_password()


def test_check_password_invalid3(user):
    """Test invalid password format (too short)."""
    user.password = "Weak#4"
    assert user.check_password()


def test_check_password_valid(user):
    """Test valid password format."""
    user.password = "StrongPass3@"
    assert not user.check_password()


def test_hash_password(user):
    """Test password hashing and verification."""
    password = "StrongPass@5"
    hashed_password = user.hash_password(password)
    assert bcrypt.checkpw(password.encode('utf-8'),
                          hashed_password.encode('utf-8'))


def test_check_pass(user):
    """Test password checking with correct credentials."""
    entered_password = "StrongPass@5"
    stored_password = user.hash_password(entered_password)
    assert user.check_pass(entered_password, stored_password)


def test_check_pass_invalid(user):
    """Test password checking with incorrect credentials."""
    entered_password = "IncorrectPassword"
    stored_password = user.hash_password("StrongPass@5")
    assert not user.check_pass(entered_password, stored_password)


def test_valid_sign_up(user):
    """Test user sign-up with valid credentials."""
    email = "email1@test.com"
    password = "ValidPassword@4"
    username = "test_user"
    assert user.sign_up(email, password, username) == "NO exception"


def test_sign_up_invalid_email(user):
    """Test user sign-up with invalid email."""
    email = "invalid-email"
    password = "ValidPassword@1"
    username = "valid_user"

    with pytest.raises(ValueError) as excinfo:
        user.sign_up(email, password, username)
    assert str(excinfo.value) == invalid_email


def test_sign_up_invalid_username(user):
    """Test user sign-up with invalid username."""
    email = "email@test.com"
    password = "ValidPassword@1"
    username = "inval!d_user"

    with pytest.raises(ValueError) as ex:
        user.sign_up(email, password, username)
    assert str(ex.value) == invalid_username


def test_sign_up_invalid_password(user):
    """Test user sign-up with invalid password."""
    email = "email@test.com"
    password = "weakpass1"
    username = "valid_user"

    with pytest.raises(ValueError) as ex:
        user.sign_up(email, password, username)
    assert str(ex.value) == invalid_password


def test_sign_up_duplicate_email(user):
    """Test user sign-up with an email that's already in use."""
    email = "email@test.com"
    password = "Validpassword@1"
    username1 = "valid_user1"
    username2 = "valid_user2"

    user.sign_up(email, password, username1)

    with pytest.raises(ValueError) as ex:
        user.sign_up(email, password, username2)
    assert str(ex.value) == "This email is already in use."


def test_sign_up_duplicate_username(user):
    """Test user sign-up with a username that's already in use."""
    email1 = "email1@test.com"
    email2 = "email2@test.com"
    password = "ValidPassword@1"
    username = "Duplicate_User"

    user.sign_up(email1, password, username)

    with pytest.raises(ValueError) as ex:
        user.sign_up(email2, password, username)
    assert str(ex.value) == "This username is already in use."


def test_login_successful(user):
    """Test successful user login."""
    email = "email@test.com"
    password = "ValidPass@1"
    username = "valid_user"

    user.sign_up(email, password, username)

    assert user.log_in(username, password) == "No exception"


def test_login_invalid_credentials(user):
    """Test user login with incorrect password."""
    email = "email@test.com"
    password = "ValidPass@6"
    username = "valid-user"

    user.sign_up(email, password, username)

    with pytest.raises(ValueError) as ex:
        user.log_in(username, "incorrect_password")
    assert str(ex.value) == "Username or password is wrong."


def test_login_inactive_account(user):
    """Test user login with a deactivated account."""
    email = "email9@test.com"
    password = "ValidPassword@7"
    username = "valid_user_a"
    user.account = "deactive"

    user.sign_up(email, password, username)

    with pytest.raises(PermissionError) as ex:
        user.log_in(username, password)
    assert str(ex.value) == "Your account is deactivated."


def test_get_leader_projects(user, project):
    """Test retrieving projects where the user is the leader."""
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
    """Test retrieving projects where the user is a member."""
    user.sign_up("email@test.com", "StrongPass@1", "user")
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


def test_create_project(project):
    """Test project creation."""
    project.create("1", "Project", "description", "leader_username")
    reader = projects_file.read()
    assert len(reader) == 2
    assert reader[1] == ["1", "Project", "description", "leader_username"]


def test_create_project_duplicate_id(project):
    """Test project creation with a duplicate ID."""
    project.create("1", "Project", "description", "leader")
    with pytest.raises(ValueError) as ex:
        project.create("1", "Project", "description", "leader")
        assert str(ex) == "The selected id is not unique"


def test_leader_projects(project, user):
    """Test retrieving projects led by the user."""
    project_id = "1"
    project_title = "Project"
    project_description = "description"
    project_leader = user.username

    project.create(project_id, project_title,
                   project_description, project_leader)

    leader_projects = user.get_leader_projects()

    assert len(leader_projects) == 1
    assert leader_projects[0][0] == project_id
    assert leader_projects[0][1] == project_title
    assert leader_projects[0][2] == project_description
    assert leader_projects[0][3] == project_leader


def test_user_projects(project, user):
    """Test retrieving projects where the user is a member."""
    project_id = "1"
    project_title = "Project"
    project_description = "description"
    project_leader = user.username

    project.create(project_id, project_title,
                   project_description, project_leader)

    leader_projects = user.get_leader_projects()

    assert len(leader_projects) == 1
    assert leader_projects[0][0] == project_id
    assert leader_projects[0][1] == project_title
    assert leader_projects[0][2] == project_description
    assert leader_projects[0][3] == project_leader


def test_add_member(user, project):
    """Test adding a member to a project."""
    user.sign_up("email@test.com", "StrongPass@1", "user")
    project.create("1", "Project", "description", "leader_username")
    project.add_member_func("user", "1")
    reader = projects_file.read()
    assert reader[1][4] == "user"


def test_delete_member(user, project):
    """Test deleting a member from a project."""
    user.sign_up("email1@test.com", "StrongPass@1", "user1")
    user.sign_up("email2@test.com", "StrongPass@2", "user2")
    project.create("1", "Project", "description", "leader_username")
    project.add_member_func("user1", "1")
    project.add_member_func("user2", "1")
    project.delete_member_func("user2", "1")
    reader = projects_file.read()
    assert reader[1][4] == "user1"


def test_delete_project(project):
    """Test deleting a project."""
    project.create("1", "Project", "description", "leader_username")
    project.delete_project("1")
    reader = projects_file.read()
    assert len(reader) == 1
