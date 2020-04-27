import pytest

from path_finder.domain import Playground

filepath = '..\\2020_Internship_Challenge_Software\\Step_One.csv'


@pytest.mark.parametrize(
    "playgr,point,path",
    [
        (
                Playground(filepath),
                (2, 2),
                [(1, 1)]
        ),
        (
                Playground(filepath),
                (1, 3),
                [(1, 1)]
        ),
        (
                Playground(filepath),
                (-1, 2),
                [(1, 1)]
        ),
        (
                Playground(filepath),
                (16, 10),
                [(1, 1)]
        )
    ]
)
def test_is_valid(playgr, point, path):
    assert not playgr.is_valid(point, path, set())


@pytest.mark.parametrize(
    "playgr,point,res",
    [
        (
                Playground(filepath),
                (1, 2),
                {(0, 2), (2, 2), (1, 1), (1, 3)}
        )
    ]
)
def test_get_orthogonal_neighbours(playgr, point, res):
    assert set(playgr.get_orthogonal_neighbours(point)) == res


@pytest.mark.parametrize(
    "playgr,point,res",
    [
        (
                Playground(filepath),
                (1, 2),
                {(0, 2), (2, 2), (1, 1), (1, 3), (0, 1), (2, 3), (0, 3), (2, 1)}
        )
    ]
)
def test_get_neighbours(playgr, point, res):
    assert set(playgr.get_neighbours(point)) == res


if __name__ == '__main__':
    pytest.main(['-v', __file__])
