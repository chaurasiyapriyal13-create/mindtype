import unittest
from src.analytics import analyse, compare
class AnalyticsTests(unittest.TestCase):
    def test_known_measurements(self):
        events=[dict(interval=200,dwell=80,backspace=int(i%10==0),error=0) for i in range(100)]
        result=analyse(events)
        self.assertEqual(result['median_interval_ms'],200)
        self.assertEqual(result['backspace_rate'],.1)
        self.assertEqual(result['pause_rate'],0)
        self.assertTrue(all(x==0 for x in compare(result,result).values()))
    def test_invalid_capture(self):
        with self.assertRaises(ValueError):analyse([])
        with self.assertRaises(ValueError):analyse([dict(interval=float('nan'))]*40)
    def test_pause_denominator(self):
        rows=[dict(interval=200,dwell=80) for _ in range(100)]
        rows[0]['interval']=0;rows[1]['interval']=1500
        self.assertAlmostEqual(analyse(rows)['pause_rate'],1/99,places=4)
if __name__=='__main__':unittest.main()
