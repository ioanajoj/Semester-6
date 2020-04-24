from main import Playground
# import unittest
import numpy as np
import pytest

# class PlaygroundTest(unittest.TestCase):

#     def test_is_valid(self):
#         self.file1 = 'E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'
#         playgr = Playground(self.file1)

#         self.assertFalse(playgr.is_valid((2, 2), [(1,1)]))
#         self.assertFalse(playgr.is_valid((2,2), [(1,1)]))
#         self.assertFalse(playgr.is_valid((1,3), [(1,1)]))
#         self.assertFalse(playgr.is_valid((-1,2), [((1,1))]))
#         self.assertFalse(playgr.is_valid((16,10), [(1,1)]))
#         self.assertTrue(playgr.is_valid((0,0), [(1,1)]))

#     def test_get_orthogonal_neighbours(self):
#         self.file1 = 'E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'
#         playgr = Playground(self.file1)
        
#         self.assertListEqual(playgr.get_orthogonal_neighbours((1, 2)),[(0,2), (2,2), (1,1), (1,3)])

#     def test_get_neighbours(self):
#         self.file1 = 'E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'
#         playgr = Playground(self.file1)
        
#         self.assertEqual(playgr.get_neighbours((1, 2)), [(0,2), (2,2), (1,1), (1,3), (0,1), (2,3), (0,3), (2,1)])

# if __name__ == '__main__':
#     unittest.main()


@pytest.mark.parametrize(
"playgr,input,res", 
[
    (
        Playground('E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_One.csv'),
        (1,2),
        set([(0,2), (2,2), (1,1), (1,3), (0,1), (2,3), (0,3), (2,1), (1,2)])
    )
]
)
def test_generic_case(playgr, input, res):
    assert set(playgr.get_neighbours(input)) == res

if __name__ == '__main__':
    pytest.main(['-v', __file__])
