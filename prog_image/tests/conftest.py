import pytest
from mongoengine import connect


@pytest.fixture
def mongo(request):
    """Create MongoEngine connection to MongoMock"""
    connection = connect(db='mongotest', host='mongodb://localhost:27017/prog-image')

    def fin():
        """Drop the database at the end of the fixture"""
        connection.drop_database('mongotest')
        return

    request.addfinalizer(fin)
    return connection
