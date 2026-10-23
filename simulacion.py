"""Ejercicio educativo de HipotecaNow. Modelo fijo ficticio, no cuadro bancario."""
from decimal import Decimal, InvalidOperation, localcontext, ROUND_HALF_UP
import argparse
import csv
import sys

CENT = Decimal('0.01')

def numero(texto):
    try:
        value = Decimal(str(texto))
    except (InvalidOperation, ValueError):
        raise ValueError('Importe o tipo no válido') from None
    if not value.is_finite():
        raise ValueError('No se admiten NaN o infinitos')
    return value

def dinero(x):
    return x.quantize(CENT, rounding=ROUND_HALF_UP)

def cuadro(capital, tin_anual, meses):
    """TIN anual en porcentaje; períodos iguales; primer pago al final del mes.

    Intereses redondeados por período a céntimos. Último pago ajustado al saldo.
    Sin comisiones, seguros, carencia ni pagos extraordinarios.
    """
    p, tin = numero(capital), numero(tin_anual)
    if p <= 0 or p > Decimal(1000000000) or p != dinero(p):
        raise ValueError('Capital entre 0,01 y 1000000000 euros, con un máximo de dos decimales')
    if tin < 0 or tin > 100:
        raise ValueError('TIN fuera del intervalo admitido por este ejercicio: 0..100')
    if isinstance(meses, bool) or not isinstance(meses, int) or not 1 <= meses <= 1200:
        raise ValueError('Meses enteros entre 1 y 1200')
    with localcontext() as ctx:
        ctx.prec = 40
        r = tin / Decimal(1200)
        nominal = p / meses if r == 0 else p * r / (1 - (1 + r) ** (-meses))
        pago_regular = dinero(nominal)
        saldo = p
        rows = []
        for k in range(1, meses + 1):
            interes = dinero(saldo * r)
            pago = saldo + interes if k == meses else min(pago_regular, saldo + interes)
            amortizado = pago - interes
            if amortizado < 0:
                raise ValueError('El redondeo del supuesto produce amortización negativa')
            saldo = dinero(saldo - amortizado)
            rows.append({'mes': k, 'cuota': pago, 'intereses': interes,
                         'capital_amortizado': amortizado, 'saldo_pendiente': saldo})
            if saldo == 0:
                break
        return rows

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('capital', help='Euros, punto decimal, sin separadores de miles')
    ap.add_argument('tin', help='TIN anual en porcentaje: 3 significa 3 por ciento')
    ap.add_argument('meses', type=int, help='Número de pagos mensuales restantes')
    args = ap.parse_args()
    try:
        rows = cuadro(args.capital, args.tin, args.meses)
    except ValueError as exc:
        ap.error(str(exc))
    writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]), delimiter=';', lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

if __name__ == '__main__':
    main()
