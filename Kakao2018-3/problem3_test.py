import unittest

import problem3

class SortTest(unittest.TestCase):
    def test_ex1(self):
        target = ['img12.png', 'img10.png', 'img02.png', 'img1.png', 'IMG01.GIF', 'img2.JPG']
        expected = ['img1.png', 'IMG01.GIF', 'img02.png', 'img2.JPG', 'img10.png', 'img12.png']
        self.assertEqual(expected, problem3.go_sort(target))


    def test_ex2(self):
        target = ['F-5 Freedom Fighter', 'B-50 Superfortress', 'A-10 Thunderbolt II', 'F-14 Tomcat']
        expected = ['A-10 Thunderbolt II', 'B-50 Superfortress', 'F-5 Freedom Fighter', 'F-14 Tomcat']
        self.assertEqual(expected, problem3.go_sort(target))

if __name__ == '__main__':
    unittest.main(verbosity=2)
