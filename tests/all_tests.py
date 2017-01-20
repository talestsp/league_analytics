import unittest


if __name__ == "__main__":
	loader = unittest.TestLoader()

	suite1 = loader.discover('tests', pattern = "*_test.py") 
	alltests = unittest.TestSuite(suite1)
	unittest.TextTestRunner(verbosity=2).run(alltests)
