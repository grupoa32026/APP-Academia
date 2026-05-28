import unittest
from controlador_clases import calculariva

class tests_calcularIVA(unittest.TestCase):
    def test_sumarar5(self):
        self.assertEqual(calculariva(100),21)
        self.assertEqual(calculariva(10),2.1)
        self.assertEqual(calculariva(200),42)
        self.assertEqual(calculariva(20),4.2)
        
if __name__ == '__main__':
    unittest.main()