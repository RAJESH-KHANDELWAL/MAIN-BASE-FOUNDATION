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


def test_username_duplicates_are_allowed_in_database():
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

    service.save_identity(identity_one)
    service.save_identity(identity_two)

    assert identity_one.username == username
    assert identity_two.username == username

    assert identity_one.unique_id != identity_two.unique_id

    assert len(identity_one.unique_id) == 8
    assert len(identity_two.unique_id) == 8

    saved_identities = service.search_identities(
        username
    )

    matching_identities = [
        identity
        for identity in saved_identities
        if identity.username == username
    ]

    assert len(matching_identities) == 2


def test_unique_id_is_unique_in_database():
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

    service.save_identity(identity_one)
    service.save_identity(identity_two)

    assert len(identity_one.unique_id) == 8
    assert len(identity_two.unique_id) == 8

    assert identity_one.unique_id != identity_two.unique_id

    found_one = service.get_by_unique_id(
        identity_one.unique_id
    )

    found_two = service.get_by_unique_id(
        identity_two.unique_id
    )

    assert found_one is not None
    assert found_two is not None

    assert found_one.unique_id == identity_one.unique_id
    assert found_two.unique_id == identity_two.unique_id


def test_username_search_returns_multiple_identities():
    service = create_test_identity_service()

    username = "SHARED_USERNAME"

    identity_one = service.create_identity(
        full_name="Shared User One",
        username=username,
        email="shared-one@example.com",
        phone="9000000005",
    )

    identity_two = service.create_identity(
        full_name="Shared User Two",
        username=username,
        email="shared-two@example.com",
        phone="9000000006",
    )

    service.save_identity(identity_one)
    service.save_identity(identity_two)

    results = service.search_identities(
        username
    )

    matching = [
        identity
        for identity in results
        if identity.username == username
    ]

    assert len(matching) == 2
