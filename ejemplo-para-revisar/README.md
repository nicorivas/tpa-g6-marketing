# Propuesta de ejemplo para revisar

Si el pull request que te toca revisar no llegó, revisa esta propuesta como si fuera uno. La escribió un autor que eligió **gasto completo primero**: no se excluye ningún día del CPL y las anomalías solo se marcan.

Son tres archivos:
- `descripcion_pr.md` es el texto completo del pull request, tal como lo escribió el autor.
- `reglas_cambio_ejemplo.md` es el cambio que el autor dice haber hecho en `reglas.md` (las reglas 4 y 5, antes y después).
- `reporte_propuesto_ejemplo.csv` es el reporte que armó.

En este ejemplo no hay cambio en `traspaso.md`: el texto del pull request lista los archivos que cambió, y ese no está.

Para revisarla, pide a Claude: *«Lee ejemplo-para-revisar/descripcion_pr.md y reglas_cambio_ejemplo.md, y corre `python3 verificar.py ejemplo-para-revisar/reporte_propuesto_ejemplo.csv`. Revisa la propuesta con REVIEW.md. Dime si cambia solo lo que se pidió, si hay información que no debería estar y si se entiende sin quien lo escribió, y qué problemas hay incluso si el verificador no los detecta.»*
