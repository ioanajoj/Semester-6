from main import Playground
# import unittest
import numpy as np
import pytest

@pytest.mark.parametrize(
"playgr,point,path", 
[
    (
        Playground('E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'),
        (2,2),
        [(1,1)]
    ),
    (
        Playground('E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'),
        (1,3),
        [(1,1)]
    ),
    (
        Playground('E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'),
        (-1,2),
        [(1,1)]
    ),
    (
        Playground('E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'),
        (16,10),
        [(1,1)]
    )
]
)
def test_is_valid(playgr, point, path):
    assert not playgr.is_valid(point, path)

@pytest.mark.parametrize(
"playgr,input,res", 
[
    (
        Playground('E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'),
        (1,2),
        set([(0,2), (2,2), (1,1), (1,3)])
    )
]
)
def test_get_orthogonal_neighbours(playgr, input, res):
    assert set(playgr.get_orthogonal_neighbours(input)) == res

@pytest.mark.parametrize(
"playgr,input,res", 
[
    (
        Playground('E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'),
        (1,2),
        set([(0,2), (2,2), (1,1), (1,3), (0,1), (2,3), (0,3), (2,1)])
    )
]
)
def test_get_neighbours(playgr, input, res):
    assert set(playgr.get_neighbours(input)) == res


if __name__ == '__main__':
    pytest.main(['-v', __file__])
