from atomicplot2.data import XYDataObject
import unittest
import numpy as np


class DataObjectTest(unittest.TestCase):
    def test_inputtype(self):
        with self.assertRaises(TypeError):
            x = 'test_string'
            y = [1, 2, 3, 4]
            XYDataObject(x, y)

        with self.assertRaises(ValueError):
            x = [1, 2, 3, 4, 5]
            y = [1, 2, 3, 4]
            XYDataObject(x, y)

        with self.assertRaises(ValueError):
            x = np.arange(10).reshape(5)
            y = np.arange(5)
            XYDataObject(x, y)

    def test_add(self):
        x = np.arange(4)
        y = np.arange(4) + 5
        d = XYDataObject(x, y)

        d_out = d + 10  # Test adding scalar
        self.assertTrue(np.array_equal(d.y + 10, d_out.y))

        d_out = d + y[::-1]  # Test adding array
        self.assertTrue(np.array_equal(d.y + y[::-1], d_out.y))

        d_out = d + XYDataObject(x, y ** 2)  # Test subtracting another DataObject
        self.assertTrue(np.array_equal(d.y + y**2, d_out.y))

    def test_sub(self):
        x = np.arange(4)
        y = np.arange(4) + 5
        d = XYDataObject(x, y)

        d_out = d - 10  # Test subtracting scalar
        self.assertTrue(np.array_equal(d.y - 10, d_out.y))

        d_out = d - y[::-1]  # Test subtracting array
        self.assertTrue(np.array_equal(d.y - y[::-1], d_out.y))

        d_out = d - XYDataObject(x, y ** 2)  # Test adding another DataObject
        self.assertTrue(np.array_equal(d.y - y**2, d_out.y))

    def test_mul(self):
        x = np.arange(4)
        y = np.arange(4) + 5
        d = XYDataObject(x, y)

        d_out = d * 10  # Test multiplying scalar
        self.assertTrue(np.array_equal(d.y * 10, d_out.y))

        d_out = d * y[::-1]  # Test multiplying array
        self.assertTrue(np.array_equal(d.y * y[::-1], d_out.y))

        d_out = d * XYDataObject(x, y ** 2)  # Test multiplying another DataObject
        self.assertTrue(np.array_equal(d.y * y**2, d_out.y))

    def test_truediv(self):
        x = np.arange(4)
        y = np.arange(4) + 5
        d = XYDataObject(x, y)

        d_out = d / 10
        self.assertTrue(np.array_equal(d.y / 10, d_out.y))

        d_out = d / y[::-1]
        self.assertTrue(np.array_equal(d.y / y[::-1], d_out.y))

        d_out = d / XYDataObject(x, y ** 2)
        self.assertTrue(np.array_equal(d.y / y**2, d_out.y))

    def test_floordiv(self):
        x = np.arange(4)
        y = np.arange(4) + 5
        d = XYDataObject(x, y)

        d_out = d // 10
        self.assertTrue(np.array_equal(d.y // 10, d_out.y))

        d_out = d // y[::-1]
        self.assertTrue(np.array_equal(d.y // y[::-1], d_out.y))

        d_out = d // XYDataObject(x, y ** 2)
        self.assertTrue(np.array_equal(d.y // y**2, d_out.y))

    def test_pow(self):
        x = np.arange(4)
        y = np.arange(4) + 5
        d = XYDataObject(x, y)

        d_out = d ** 10  # Test multiplying scalar
        self.assertTrue(np.array_equal(d.y ** 10, d_out.y))

        d_out = d ** y[::-1]  # Test multiplying array
        self.assertTrue(np.array_equal(d.y ** y[::-1], d_out.y))

        d_out = d ** XYDataObject(x, y ** 2)  # Test multiplying another DataObject
        self.assertTrue(np.array_equal(d.y ** (y**2), d_out.y))

    def test_neg(self):
        x = np.arange(4)
        y = np.arange(4) + 5
        d = XYDataObject(x, y)
        d_out = -d
        self.assertTrue(np.array_equal(-1*d.y, d_out.y))

    def test_abs(self):
        x = np.arange(4)
        y = np.arange(4) - 3
        d = XYDataObject(x, y)
        d_out = abs(d)
        self.assertTrue(np.array_equal(np.absolute(d.y), d_out.y))

    def test_isub(self):
        x = np.arange(4)
        y = (np.arange(4) + 5)
        d = XYDataObject(x, y)
        d -= 3

        self.assertTrue(np.array_equal(d.y, y - 3))

    def test_iadd(self):
        x = np.arange(4)
        y = (np.arange(4) + 5)
        d = XYDataObject(x, y)
        d += 3

        self.assertTrue(np.array_equal(d.y, y + 3))

    def test_imul(self):
        x = np.arange(4)
        y = (np.arange(4) + 5)
        d = XYDataObject(x, y)
        d *= 3

        self.assertTrue(np.array_equal(d.y, y * 3))

    def test_itruediv(self):
        x = np.arange(4)
        y = (np.arange(4) + 5).astype('float')
        d = XYDataObject(x, y)
        d /= 3

        self.assertTrue(np.array_equal(d.y, y/3))

    def test_ifloordiv(self):
        x = np.arange(4)
        y = (np.arange(4) + 5).astype('float')
        d = XYDataObject(x, y)
        d //= 3

        self.assertTrue(np.array_equal(d.y, y // 3))

    def test_ipow(self):
        x = np.arange(4)
        y = (np.arange(4) + 5)
        d = XYDataObject(x, y)
        d **= 3

        self.assertTrue(np.array_equal(d.y, y**3))


if __name__ == '__main__':
    unittest.main()