import unittest
import src.csv_tool as csv_tool

class CSVToolTestCase(unittest.TestCase):

    def test_parser(self):
        (f, d) = csv_tool.parse_args(['file1.csv'])
        self.assertEqual(f, 'file1.csv')
        dct = vars(d)
        self.assertEqual(dct['delimiter'], ',')
        self.assertEqual(dct['quotechar'], '"')
        self.assertEqual(dct['escapechar'], None)
        self.assertEqual(dct['doublequote'], True)
        self.assertEqual(dct['skipinitialspace'], False)
        self.assertEqual(dct['quoting'], 0)

        (f, d) = csv_tool.parse_args(['-d', 'A', '-q', 'B', '-e', 'C', '-c', '-s', '-b', 'D', 'file2.csv'])
        self.assertEqual(f, 'file2.csv')
        dct = vars(d)
        self.assertEqual(dct['delimiter'], 'A')
        self.assertEqual(dct['quotechar'], 'B')
        self.assertEqual(dct['escapechar'], 'C')
        self.assertEqual(dct['doublequote'], False)
        self.assertEqual(dct['skipinitialspace'], True)
        self.assertEqual(dct['quoting'], 'D')

    def test_csv_tool(self):
        self.assertEqual(csv_tool.csv_tool('data/empty.csv', csv_tool.csv.excel), 0)
        self.assertEqual(csv_tool.csv_tool('data/tmp.csv', csv_tool.csv.excel), 6)
        self.assertEqual(csv_tool.csv_tool('data/bogus.csv', csv_tool.csv.excel_tab), -1)

if __name__ == '__main__':
    unittest.main()