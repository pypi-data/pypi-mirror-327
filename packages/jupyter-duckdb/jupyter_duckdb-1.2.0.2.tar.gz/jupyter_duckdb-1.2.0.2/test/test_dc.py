from duckdb_kernel.parser import DCParser
from . import Connection


def test_case_insensitivity():
    for query in (
            '{ username | users(id, username) }',
            '{ username | Users(id, username) }',
            '{ username | USERS(id, username) }',
            '{ username | uSers(id, username) }'
    ):
        root = DCParser.parse_query(query)

        # execute to test case insensitivity
        with Connection() as con:
            assert con.execute_dc(root) == [
                ('Alice',),
                ('Bob',),
                ('Charlie',)
            ]


def test_simple_queries():
    with Connection() as con:
        for query in [
            '{ id | Users(id, _) }',
            '{ id | Users (id, _) }',
            '{ id | Users id,_ }',
            '{id|Users(id,_)}',
            'id | Users (id ,_)',
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                (1,),
                (2,),
                (3,)
            ]

        for query in [
            '{ id, name | Users(id, name) }',
            '{ id,name | Users(id, name) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                (1, 'Alice'),
                (2, 'Bob'),
                (3, 'Charlie')
            ]


def test_asterisk_projection():
    with Connection() as con:
        root = DCParser.parse_query('{ * | Users(id, _) }')
        assert con.execute_dc(root) == [
            (1,),
            (2,),
            (3,)
        ]

        root = DCParser.parse_query('{ * | Users(id, name) }')
        assert con.execute_dc(root) == [
            (1, 'Alice'),
            (2, 'Bob'),
            (3, 'Charlie')
        ]


def test_conditions():
    with Connection() as con:
        for query in [
            '{ name | Users(id, name) ∧ id > 1 }',
            '{ name | Users(id, name) ∧ id ≠ 1 }',
            '{ name | Users(id, name) ∧ (id = 2 ∨ id = 3) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Bob',),
                ('Charlie',)
            ]

        for query in [
            '{ id | Users(id, name) ∧ name > "B" ∧ name < "C" }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                (2,)
            ]


def test_shortcut_conditions():
    with Connection() as con:
        # single shortcut conditions
        for query in [
            '{ name | Users(1, name) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Alice',)
            ]

        for query in [
            '{ season_name | Seasons(1, 1, season_name) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 1 / Season 1',)
            ]

        # multiple shortcut conditions
        for query in [
            '{ sname, ename | Seasons(snum, 2, sname) ∧ Episodes(enum, snum, 2, ename) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 1'),
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 2'),
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 3'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 1'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 2'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 3'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 4')
            ]


def test_joins():
    with Connection() as con:
        # with one attribute
        for query in [
            '{ sename | Shows(shid, shname) ∧ Seasons(senum, shid, sename) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 1 / Season 1',),
                ('Show 1 / Season 2',),
                ('Show 2 / Season 1',),
                ('Show 2 / Season 2',)
            ]

        for query in [
            '{ sename | Shows(shid, shname) ∧ Seasons(senum, shid, sename) ∧ shname = "Show 1" }',
            '{ sename | Seasons(senum, shid, sename) ∧ Shows(shid, "Show 1") }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 1 / Season 1',),
                ('Show 1 / Season 2',)
            ]

        # with multiple attributes
        for query in [
            '{ sname, ename | Seasons(snum, shid, sname) ∧ Episodes(enum, snum, shid, ename) ∧ shid = 2 }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 1'),
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 2'),
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 3'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 1'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 2'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 3'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 4')
            ]

        # join three relations
        for query in [
            '{ s2,c5 | Shows(s1,s2) ∧ Episodes(e1,e2,s1,e4) ∧ Characters(c1,e1,c3,s1,c5) ∧ s1=2 ∧ e4="Show 2 / Season 1 / Episode 2" }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2', 'Actor F')
            ]

        # cross join
        root = DCParser.parse_query('{ sename | Shows(shid1, shname) ∧ Seasons(senum, shid2, sename) ∧ shid1 = shid2 }')
        assert con.execute_dc(root) == [
            ('Show 1 / Season 1',),
            ('Show 1 / Season 2',),
            ('Show 2 / Season 1',),
            ('Show 2 / Season 2',)
        ]

        for query in [
            '{ s2,c5 | Shows(sa1,s2) ∧ Episodes(e1,e2,sb1,e4) ∧ Characters(c1,e1,c3,sb1,c5) ∧ sa1=2 ∧ sa1 = sb1 ∧ e4="Show 2 / Season 1 / Episode 2" }',
            '{ s2,c5 | Shows(sa1,s2) ∧ Episodes(e1,e2,sb1,e4) ∧ Characters(c1,e1,c3,sc1,c5) ∧ sa1=2 ∧ sa1 = sb1 ∧ sb1 = sc1 ∧ e4="Show 2 / Season 1 / Episode 2" }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2', 'Actor F')
            ]


def test_underscores():
    with Connection() as con:
        # distinct underscores
        for query in [
            '{ ename | Seasons(snum, shid, sname) ∧ Episodes(_, snum, shid, ename) ∧ shid = 2 }',
            '{ ename | Seasons(snum, shid, sname) ∧ Episodes(enum, _, shid, ename) ∧ shid = 2 }',
            '{ ename | Seasons(snum, shid, sname) ∧ Episodes(__, snum, shid, ename) ∧ shid = 2 }',
            '{ ename | Seasons(snum, shid, sname) ∧ Episodes(_, __, shid, ename) ∧ shid = 2 }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1 / Episode 1',),
                ('Show 2 / Season 1 / Episode 2',),
                ('Show 2 / Season 1 / Episode 3',),
                ('Show 2 / Season 2 / Episode 1',),
                ('Show 2 / Season 2 / Episode 2',),
                ('Show 2 / Season 2 / Episode 3',),
                ('Show 2 / Season 2 / Episode 4',)
            ]

        # reused underscores in a single relation
        for query in [
            '{ ename | Seasons(snum, shid, sname) ∧ Episodes(_, _, shid, ename) ∧ shid = 2 }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1 / Episode 1',),
                ('Show 2 / Season 1 / Episode 2',),
                ('Show 2 / Season 1 / Episode 3',),
                ('Show 2 / Season 2 / Episode 1',),
                ('Show 2 / Season 2 / Episode 2',),
                ('Show 2 / Season 2 / Episode 3',),
                ('Show 2 / Season 2 / Episode 4',)
            ]

        # reused underscores in two different relations
        for query in [
            '{ ename | Seasons(_, shid, _) ∧ Episodes(_, _, shid, ename) ∧ shid = 2 }',
            '{ ename | Seasons(_, shid, __) ∧ Episodes(_, __, shid, ename) ∧ shid = 2 }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1 / Episode 1',),
                ('Show 2 / Season 1 / Episode 2',),
                ('Show 2 / Season 1 / Episode 3',),
                ('Show 2 / Season 2 / Episode 1',),
                ('Show 2 / Season 2 / Episode 2',),
                ('Show 2 / Season 2 / Episode 3',),
                ('Show 2 / Season 2 / Episode 4',)
            ]
