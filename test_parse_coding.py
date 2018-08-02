from parse_coding import read_csibra_data
import os
import unittest

class TestReadCsibraData(unittest.TestCase):
    '''Check that parsed data agrees with a manual parsing into trial & looking times'''

    @classmethod
    def setUpClass(self):
        self.csvDir = os.path.join(os.path.dirname(__file__), 'Data', 'Csibra', 'csv')
        self.tol = 0.0001 # precision of "expected" values
        
    def close_enough(self, lineA, lineB):
        return (lineA['TrackName'] == lineB['TrackName'] and \
            abs(lineA['Time'] - lineB['Time']) < self.tol and \
            abs(lineA['Duration'] - lineB['Duration']) < self.tol)
    
    def test_0108171630(self):
        markings = read_csibra_data(os.path.join(self.csvDir, '0108171630.csv'))
        expectedLines = [
            {'TrackName': 'trial',      'Time': 206500.,         'Duration': 47100.},
            {'TrackName': 'trial',      'Time': 256200.,         'Duration': 55566.66667},
            {'TrackName': 'looking',    'Time': 206500.,         'Duration': 15100.},
            {'TrackName': 'looking',    'Time': 221633.3333,     'Duration': 17500.},
            {'TrackName': 'looking',    'Time': 239800.,         'Duration': 6533.333333},
            {'TrackName': 'looking',    'Time': 248233.3333,     'Duration': 2966.666667},
            {'TrackName': 'looking',    'Time': 254066.6667,     'Duration': 17233.333333},
            {'TrackName': 'looking',    'Time': 271333.3333,     'Duration': 8366.666667},
            {'TrackName': 'looking',    'Time': 281366.6667,     'Duration': 9233.333333},
            {'TrackName': 'looking',    'Time': 291566.6667,     'Duration': 13800.},
            {'TrackName': 'looking',    'Time': 306633.3333,     'Duration': 2700.}]
        for line in expectedLines:
            self.assertTrue(any([self.close_enough(line, markedLine) for markedLine in markings]), 'missing expected line {}'.format(line))
        for line in markings:
            self.assertTrue(any([self.close_enough(line, expectedLine) for expectedLine in expectedLines]), 'unexpected line {}'.format(line))
            
    def test_2509171200(self):
        markings = read_csibra_data(os.path.join(self.csvDir, '2509171200.csv'))
        expectedLines = [
            {'TrackName': 'trial',      'Time': 203333.3333,    'Duration': 36133.33333},
            {'TrackName': 'trial',      'Time': 242433.3333,    'Duration': 21300.},
            {'TrackName': 'looking',    'Time': 203333.3333,    'Duration': 15100.},
            {'TrackName': 'looking',    'Time': 218466.6667,    'Duration': 6166.666667},
            {'TrackName': 'looking',    'Time': 225233.3333,    'Duration': 7300.},
            {'TrackName': 'looking',    'Time': 233366.6667,    'Duration': 3700.},
            {'TrackName': 'looking',    'Time': 240366.6667,    'Duration': 17166.666667},
            {'TrackName': 'looking',    'Time': 257566.6667,    'Duration': 3766.666667}]
        for line in expectedLines:
            self.assertTrue(any([self.close_enough(line, markedLine) for markedLine in markings]), 'missing expected line {}'.format(line))
        for line in markings:
            self.assertTrue(any([self.close_enough(line, expectedLine) for expectedLine in expectedLines]), 'unexpected line {}'.format(line))

if __name__ == '__main__':
    unittest.main()
