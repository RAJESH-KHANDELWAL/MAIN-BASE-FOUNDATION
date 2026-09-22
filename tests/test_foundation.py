import tempfile

from backend.database.service import DatabaseService
from backend.identity.service import IdentityService


def create_test_identity_service():
    database_file = tempfile.NamedTemporaryFile(
        suffix=".db",
        delete=False,
    )

    database_file.close()

    database = DatabaseService(
        database_path=database_file.name
    )

    return IdentityService(
        database_service=database
    )


def test_identity_service_initializes():
    service = create_test_identity_service()

    identities = service.list_identity()

    assert isinstance(identities, list)


def test_username_duplicates_are_allowed():
    service = create_test_identity_service()

    username = "TEST_DUPLICATE_USERNAME"

    identity_one = service.create_identity(
        full_name="Test User One",
        username=username,
        email="test-one@example.com",
        phone="9000000001",
    )

    identity_two = service.create_identity(
        full_name="Test User Two",
        username=username,
        email="test-two@example.com",
        phone="9000000002",
    )

    assert identity_one.username == username
    assert identity_two.username == username

    assert identity_one.unique_id != identity_two.unique_id

    assert len(identity_one.unique_id) == 8
    assert len(identity_two.unique_id) == 8


def test_unique_id_is_unique():
    service = create_test_identity_service()

    identity_one = service.create_identity(
        full_name="Unique Test One",
        username="UNIQUE_TEST_ONE",
        email="unique-one@example.com",
        phone="9000000003",
    )

    identity_two = service.create_identity(
        full_name="Unique Test Two",
        username="UNIQUE_TEST_TWO",
        email="unique-two@example.com",
        phone="9000000004",
    )

    assert len(identity_one.unique_id) == 8
    assert len(identity_two.unique_id) == 8

    assert identity_one.unique_id != identity_two.unique_id
