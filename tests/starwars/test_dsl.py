import pytest

from gql import Client
from gql.dsl import DSLSchema

from .schema import characterInterface, humanType, queryType


# We construct a Simple DSL objects for easy field referencing

# class Query(object):
#     hero = queryType.fields['hero']
#     human = queryType.fields['human']


# class Character(object):
#     id = characterInterface.fields['id']
#     name = characterInterface.fields['name']
#     friends = characterInterface.fields['friends']
#     appears_in = characterInterface.fields['appearsIn']


# class Human(object):
#     name = humanType.fields['name']


from .schema import StarWarsSchema


@pytest.fixture
def ds():
    client = Client(schema=StarWarsSchema)
    ds = DSLSchema(client)
    return ds


def test_hero_name_query(ds):
    query = '''
hero {
  name
}
    '''.strip()
    query_dsl = ds.Query.hero(
        ds.Character.name
    )
    assert query == str(query_dsl)


def test_hero_name_and_friends_query(ds):
    query = '''
hero {
  id
  name
  friends {
    name
  }
}
    '''.strip()
    query_dsl = ds.Query.hero(
        ds.Character.id,
        ds.Character.name,
        ds.Character.friends(
            ds.Character.name,
        )
    )
    assert query == str(query_dsl)


def test_nested_query(ds):
    query = '''
hero {
  name
  friends {
    name
    appearsIn
    friends {
      name
    }
  }
}
    '''.strip()
    query_dsl = ds.Query.hero(
        ds.Character.name,
        ds.Character.friends(
            ds.Character.name,
            ds.Character.appears_in,
            ds.Character.friends(
                ds.Character.name
            )
        )
    )
    assert query == str(query_dsl)


def test_fetch_luke_query(ds):
    query = '''
human(id: "1000") {
  name
}
    '''.strip()
    query_dsl = ds.Query.human.args(id="1000").get(
        ds.Human.name,
    )

    assert query == str(query_dsl)


# def test_fetch_some_id_query():
#     query = '''
#         query FetchSomeIDQuery($someId: String!) {
#           human(id: $someId) {
#             name
#           }
#         }
#     '''
#     params = {
#         'someId': '1000',
#     }
#     expected = {
#         'human': {
#             'name': 'Luke Skywalker',
#         }
#     }
#     result = schema.execute(query, None, params)
#     assert not result.errors
#     assert result.data == expected


# def test_fetch_some_id_query2():
#     query = '''
#         query FetchSomeIDQuery($someId: String!) {
#           human(id: $someId) {
#             name
#           }
#         }
#     '''
#     params = {
#         'someId': '1002',
#     }
#     expected = {
#         'human': {
#             'name': 'Han Solo',
#         }
#     }
#     result = schema.execute(query, None, params)
#     assert not result.errors
#     assert result.data == expected


# def test_invalid_id_query():
#     query = '''
#         query humanQuery($id: String!) {
#           human(id: $id) {
#             name
#           }
#         }
#     '''
#     params = {
#         'id': 'not a valid id',
#     }
#     expected = {
#         'human': None
#     }
#     result = schema.execute(query, None, params)
#     assert not result.errors
#     assert result.data == expected


def test_fetch_luke_aliased(ds):
    query = '''
luke: human(id: "1000") {
  name
}
    '''.strip()
    query_dsl = ds.Query.human.args(id=1000).alias('luke').get(
        ds.Character.name,
    )
    assert query == str(query_dsl)


# def test_fetch_luke_and_leia_aliased():
#     query = '''
#         query FetchLukeAndLeiaAliased {
#           luke: human(id: "1000") {
#             name
#           }
#           leia: human(id: "1003") {
#             name
#           }
#         }
#     '''
#     expected = {
#         'luke': {
#             'name': 'Luke Skywalker',
#         },
#         'leia': {
#             'name': 'Leia Organa',
#         }
#     }
#     result = schema.execute(query)
#     assert not result.errors
#     assert result.data == expected


# def test_duplicate_fields():
#     query = '''
#         query DuplicateFields {
#           luke: human(id: "1000") {
#             name
#             homePlanet
#           }
#           leia: human(id: "1003") {
#             name
#             homePlanet
#           }
#         }
#     '''
#     expected = {
#         'luke': {
#             'name': 'Luke Skywalker',
#             'homePlanet': 'Tatooine',
#         },
#         'leia': {
#             'name': 'Leia Organa',
#             'homePlanet': 'Alderaan',
#         }
#     }
#     result = schema.execute(query)
#     assert not result.errors
#     assert result.data == expected


# def test_use_fragment():
#     query = '''
#         query UseFragment {
#           luke: human(id: "1000") {
#             ...HumanFragment
#           }
#           leia: human(id: "1003") {
#             ...HumanFragment
#           }
#         }
#         fragment HumanFragment on Human {
#           name
#           homePlanet
#         }
#     '''
#     expected = {
#         'luke': {
#             'name': 'Luke Skywalker',
#             'homePlanet': 'Tatooine',
#         },
#         'leia': {
#             'name': 'Leia Organa',
#             'homePlanet': 'Alderaan',
#         }
#     }
#     result = schema.execute(query)
#     assert not result.errors
#     assert result.data == expected


# def test_check_type_of_r2():
#     query = '''
#         query CheckTypeOfR2 {
#           hero {
#             __typename
#             name
#           }
#         }
#     '''
#     expected = {
#         'hero': {
#             '__typename': 'Droid',
#             'name': 'R2-D2',
#         }
#     }
#     result = schema.execute(query)
#     assert not result.errors
#     assert result.data == expected


# def test_check_type_of_luke():
#     query = '''
#         query CheckTypeOfLuke {
#           hero(episode: EMPIRE) {
#             __typename
#             name
#           }
#         }
#     '''
#     expected = {
#         'hero': {
#             '__typename': 'Human',
#             'name': 'Luke Skywalker',
#         }
#     }
#     result = schema.execute(query)
#     assert not result.errors
#     assert result.data == expected
