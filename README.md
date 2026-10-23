# Cuadro hipotecario didáctico en Python

Recurso original de **HipotecaNow**, preparado con asistencia de IA. Incluye un modelo de cuotas mensuales a tipo nominal fijo, salida CSV y pruebas de conservación del capital. No es el código de la calculadora de HipotecaNow ni un cuadro contractual.

## Para qué sirve

Permite observar, con datos ficticios, la separación de cada pago en intereses y devolución de capital. El saldo disminuye por el capital amortizado y el último pago se ajusta para cerrar los céntimos del modelo. El programa no envía datos a Internet, no conecta cuentas bancarias y no guarda información personal.

## Ejecutar

Python 3.10 o posterior; solo biblioteca estándar. Ejecuta desde la carpeta de los archivos:

```text
python simulacion.py 100000 3 120 > ejemplo.csv
python -m unittest -v
```

Los tres argumentos son **capital en euros**, **TIN anual en porcentaje** y **meses**. Escribe 3 para indicar un TIN del 3 %, no 0.03. Usa punto decimal y ningún separador de miles: 100000.50 es una cantidad válida; el formato 100.000 no representa cien mil en este contrato de entrada.

El CSV utiliza punto decimal, punto y coma como separador y las columnas mes, cuota, intereses, capital_amortizado y saldo_pendiente. Al importarlo en una hoja de cálculo, indica esos separadores explícitamente si tu configuración regional es diferente.

## Hipótesis y redondeo

- Sistema francés, tipo fijo del supuesto durante todo el cálculo.
- Períodos mensuales iguales y primer pago al final del primer período.
- Tipo mensual: TIN anual / 1200, dado que la entrada se expresa como porcentaje.
- Sin comisiones, seguros, carencia, impuestos ni pagos extraordinarios.
- Cuota regular redondeada a céntimos; intereses de cada período redondeados con ROUND_HALF_UP; último pago ajustado al saldo.
- Los rangos de entrada son límites deliberados de este ejercicio, no condiciones de aprobación bancaria.

El cuadro puede diferir del contrato o de otro simulador que aplique días reales, precisión interna distinta o ajuste de redondeo diferente. No calcula TAE ni predice tipos futuros. Con capitales muy pequeños, el redondeo puede agotar el saldo antes del número de períodos solicitado; el cuadro termina cuando el saldo llega a cero.

## Ejemplos y comprobaciones

Con capital ficticio de 100.000 euros, TIN anual del 3 % y 120 meses, la primera cuota mostrada es 965,61 euros: 250,00 de intereses y 715,61 de capital. La segunda fila se calcula sobre un saldo menor, no sobre el capital inicial.

Con 1.000 euros, tipo cero y tres meses, los pagos del modelo son 333,33; 333,33 y 333,34 euros. Esta frontera permite comprobar que el ajuste final no deja un céntimo pendiente.

Las pruebas comprueban el cierre del saldo, la suma de capital amortizado, la identidad entre cuota y sus componentes, la continuidad de saldos y el rechazo de entradas no finitas o fuera del contrato de entrada. No certifican un cálculo bancario real.

## Fuentes y contexto

El [simulador de amortización del Banco de España y sus hipótesis](https://clientebancario.bde.es/pcb/es/menu-horizontal/podemosayudarte/simuladores/simulador_amortizacion_anticipada_prestamo.html) describe un modelo francés con pagos mensuales y simplificaciones. La documentación de [decimal en Python](https://docs.python.org/3/library/decimal.html) explica la aritmética decimal y el redondeo utilizados. Fuentes consultadas el 23 de octubre de 2026.

Para continuar explorando escenarios desde una interfaz, puedes consultar el [simulador de hipoteca de HipotecaNow](https://hipotecanow.es/simulador-hipoteca/). Cada resultado debe conservar sus datos de entrada y sus hipótesis.

No introduzcas datos reales de terceros en ejemplos públicos. Este proyecto es educativo y no determina solvencia, elegibilidad ni una recomendación de contratación.
