from decimal import Decimal
import unittest
from simulacion import cuadro

class PruebasEducativas(unittest.TestCase):
    def test_cero_interes_cierre_centimos(self):
        rows = cuadro('1000', '0', 3)
        self.assertEqual([r['cuota'] for r in rows], [Decimal('333.33'), Decimal('333.33'), Decimal('333.34')])
        self.assertEqual(rows[-1]['saldo_pendiente'], Decimal('0.00'))

    def test_conservacion_capital_y_cuotas(self):
        rows = cuadro('100000', '3', 120)
        self.assertEqual(len(rows), 120)
        self.assertEqual(rows[0]['cuota'], Decimal('965.61'))
        self.assertEqual(rows[0]['intereses'], Decimal('250.00'))
        self.assertEqual(sum(r['capital_amortizado'] for r in rows), Decimal('100000.00'))
        self.assertEqual(sum(r['cuota'] for r in rows), sum(r['intereses'] + r['capital_amortizado'] for r in rows))
        self.assertEqual(rows[-1]['saldo_pendiente'], Decimal('0.00'))
        before = Decimal('100000.00')
        for row in rows:
            self.assertGreaterEqual(row['saldo_pendiente'], 0)
            self.assertEqual(before - row['capital_amortizado'], row['saldo_pendiente'])
            before = row['saldo_pendiente']

    def test_entradas_invalidas(self):
        for capital, tin, meses in [('NaN','3',120), ('100','Infinity',12), ('-1','3',12), ('100','-1',12), ('100','3',0), ('100','3',True), ('100','3',1.5), ('100.001','3',12)]:
            with self.subTest(datos=(capital,tin,meses)), self.assertRaises(ValueError):
                cuadro(capital,tin,meses)

if __name__ == '__main__':
    unittest.main()
