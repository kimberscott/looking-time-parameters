from parse_coding import read_csibra_data
import os
import unittest

class TestReadCsibraData(unittest.TestCase):
    '''Check that parsed data agrees with a manual parsing into trial & looking times'''

    @classmethod
    def setUpClass(self):
        self.csvDir = os.path.join(os.path.dirname(__file__), 'Data', 'Csibra', 'csv')
        
    def test_1(self):
        markings = read_csibra_data(os.path.join(self.csvDir, '0210170930.csv'))
        expectedLines = [
            ['trial',	206.5,	47.1],
            ['trial',	256.2,	55.56666667],
            ['looking', 206.5,	15.1],
            ['looking', 221.6333333,	17.5],
            ['looking', 239.8,	6.533333333],
            ['looking', 248.2333333,	2.966666667],
            ['looking', 254.0666667,	2.133333333],
            ['looking', 256.2,	15.1],
            ['looking', 271.3333333,	8.366666667],
            ['looking', 281.3666667,	9.233333333],
            ['looking', 291.5666667,	13.8],
            ['looking', 306.6333333,	2.7]]
        for line in expectedLines:
            self.assertIn(line, markings, 'missing expected line')
        for line in markings:
            self.assertIn(line, expectedLines, 'unexpected line')
            
    def test_2(self):
        markings = read_csibra_data(os.path.join(self.csvDir, '2509171200.csv'))
        expectedLines = [
            ['trial',	203.3333333,	36.13333333],
            ['trial',	242.4333333,	21.3],
            ['looking',	203.3333333,	15.1],
            ['looking',	218.4666667,	6.166666667],
            ['looking',	225.2333333,	7.3],
            ['looking',	233.3666667,	3.7],
            ['looking',	240.3666667,	2.066666667],
            ['looking',	242.4333333,	15.1],
            ['looking',	257.5666667,	3.766666667],
            ['looking',	263.7333333,	-263.7333333]]
        for line in expectedLines:
            self.assertIn(line, markings, 'missing expected line')
        for line in markings:
            self.assertIn(line, expectedLines, 'unexpected line')

if __name__ == '__main__':
    unittest.main()
