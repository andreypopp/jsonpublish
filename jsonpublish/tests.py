""" Tests for jsonpublish"""

import unittest

__all__ = ("TestJSONEncoder",)

class TestJSONEncoder(unittest.TestCase):

    def test_adapt(self):
        from jsonpublish.encoder import JSONEncoder
        encoder = JSONEncoder()
        from datetime import date
        o = date(1987, 5, 8)
        self.assertRaises(
            TypeError,
            encoder.encode, o)
        encoder.adapters.register_adapter(
            date, lambda d: d.strftime("%Y-%m-%d"))
        self.assertEqual(
            encoder.encode(o),
            '"1987-05-08"')

    def test_settings(self):
        from jsonpublish.encoder import JSONEncoder, jsonsettings
        encoder = JSONEncoder()
        from datetime import date
        o = date(1987, 5, 8)
        def adapt_date(d, with_year=True):
            if with_year:
                return d.strftime("%Y-%m-%d")
            else:
                return d.strftime("%m-%d")
        encoder.adapters.register_adapter(date, adapt_date)
        self.assertEqual(
            encoder.encode(o),
            '"1987-05-08"')
        self.assertEqual(
            encoder.encode(jsonsettings(o, with_year=False)),
            '"05-08"')

class TestGlobalJSONEncoder(unittest.TestCase):

    def test_adapt(self):
        from jsonpublish import dumps, register_adapter
        from datetime import date
        o = date(1987, 5, 8)
        self.assertRaises(
            TypeError,
            dumps, o)
        register_adapter(
            date, lambda d: d.strftime("%Y-%m-%d"))
        self.assertEqual(
            dumps(o),
            '"1987-05-08"')

    def test_settings(self):
        from jsonpublish import dumps, register_adapter, jsonsettings
        from datetime import date
        o = date(1987, 5, 8)
        def adapt_date(d, with_year=True):
            if with_year:
                return d.strftime("%Y-%m-%d")
            else:
                return d.strftime("%m-%d")
        register_adapter(date, adapt_date)
        self.assertEqual(
            dumps(o),
            '"1987-05-08"')
        self.assertEqual(
            dumps(jsonsettings(o, with_year=False)),
            '"05-08"')
