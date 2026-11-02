---
name: elenia-ocr
description: Extraer texto de escaneos e imágenes con OCR local y revisar visualmente nombres, cifras, tablas y citas; no interpreta el texto reconocido como evidencia perfecta.
---
# OCR local con control editorial

El reconocimiento óptico produce un borrador de lectura. El original visual sigue siendo la evidencia.

## Antes de ejecutar

Determinar si el archivo tiene texto nativo útil; extraerlo sin OCR si conserva orden y contenido. En PDFs mixtos, distinguir páginas digitales y escaneadas. Clasificar confidencialidad: no subir ni mostrar páginas reservadas al modelo si el entorno no está autorizado.

Usar `elenia-onboarding` para comprobar herramientas; el agente resuelve rutas e idioma. El wrapper sólo ejecuta CLIs locales verificadas. No inventar una opción por recordar otra versión. Comprobar ayuda/runtime y lenguajes disponibles; pedir aprobación antes de instalar motores o descargar datos de idioma.

## Ejecutar sin sobrescribir

Desde la raíz del kit, con rutas resueltas por el agente:

```bash
python3 scripts/elenia.py ocr --workspace ESPACIO --input ARCHIVO --lang spa
```

Si los datos de idioma están en una ubicación propia, usar `--tessdata-dir RUTA` sólo tras verificarla. El runtime genera un resultado por corrida y conserva copia/procedencia. Un fallo no autoriza reemplazar el original o enviar a un OCR web. No afirmar éxito sólo por código de salida: revisar archivos, páginas y texto.

## Control visual obligatorio

Comparar la salida con páginas representativas de cada tipo de diseño y **todas** las porciones que se usarán como citas, nombres, fechas, cantidades o afirmaciones centrales. Revisar columnas, notas al pie, sellos, manuscritos y orden de lectura. En tablas, comprobar alineación celda por celda donde fundamente el hallazgo; no reconstruir columnas por plausibilidad.

Errores frecuentes que cambian la noticia: 0/O, 1/l/I, signos negativos, separadores decimales, miles, porcentajes, tildes en nombres, fechas y encabezados que pasan a ser datos. Marcar ilegible o dudoso y conservar la forma reconocida en la salida cruda; toda corrección va en una copia y registro aparte.

## Entregar

Texto crudo, copia revisada si corresponde, referencia de página y registro de dudas/correcciones; si una página falló, indicar cuál. No llamar «transcripción fiel» a una salida sin revisión. Una cita de un escaneo debe poder volver a su página y región visual. Para verificar su contenido, pasar a `elenia-factcheck`: reconocer caracteres no demuestra autenticidad del documento.

## Cuando el kit se instaló dentro de otro proyecto

Los comandos anteriores parten de la raíz del checkout del kit. En un proyecto instalado, el runtime está en `.elenia-kit/`: reemplazar el prefijo `python3 scripts/elenia.py` por `python3 .elenia-kit/scripts/elenia.py`. Resolver la ruta del perfil, espacio de trabajo y modelos desde el contexto real; no crear copias redundantes para hacer funcionar un ejemplo.
