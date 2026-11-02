---
name: elenia-transcripcion
description: Transcribir grabaciones con procesamiento local, marcas de tiempo y revisión de citas sin inventar palabras ni hablantes; usar para entrevistas y audios periodísticos autorizados.
---
# Transcripción local, no reconstrucción de lo dicho

## Proteger y preparar

Confirmar que el usuario tiene autorización editorial para trabajar con la grabación y clasificar su sensibilidad. No subir audio a servicios externos ni mostrar texto reservado a un modelo remoto sin aprobación del flujo por el medio. No confundir disponer del archivo con permiso para difundirlo.

El agente identifica formato, duración y canales mediante herramientas disponibles; no pide flags al periodista. Usar `elenia-onboarding` para el diagnóstico y modelos. Comprobar el ejecutable local y su ayuda antes de usar opciones; resolver dependencias con aprobación, no con instaladores silenciosos.

## Ejecutar

Desde la raíz del kit:

```bash
python3 scripts/elenia.py transcribe --workspace ESPACIO --input AUDIO --model MODELO_LOCAL --quality base --language es
```

`--model` es un archivo verificado, no un nombre para que el motor descargue automáticamente. `base` no garantiza precisión suficiente; revisar muestra y material publicable. Si el equipo permite `small`, el agente puede proponerlo. `tiny` requiere aceptación explícita de un modo restringido y `--allow-restricted-tiny`; no elegirlo en secreto por velocidad. El runtime busca por defecto el VAD local aprobado `models/ggml-silero-v6.2.0.bin` dentro del espacio y verifica su hash. Si falta, se detiene sin descargar: el agente prepara la descarga autorizada desde el lock. `--vad-model` permite una ruta local compatible y verificada; no se le pide al periodista que la elija. VAD reduce el riesgo de texto alucinado durante silencios, pero no lo elimina ni identifica personas. `--allow-no-vad` sólo se usa con aceptación explícita del mayor riesgo y revisión reforzada, nunca como atajo silencioso ante un bloqueo.

El runtime produce una corrida nueva, conserva original y procedencia y no publica. Verificar duración procesada, archivos de salida y segmentos omitidos. La ausencia de palabras en un silencio o ruido no demuestra ausencia de una declaración.

## Fidelidad y límites

- Conservar una salida cruda separada de la versión revisada. No sustituir negaciones, nombres, cifras ni tecnicismos por lo que «tendría sentido».
- Marcar `[inaudible HH:MM:SS]`, `[palabra dudosa: …]` o solapamientos. No rellenar huecos por contexto.
- Las marcas de tiempo ubican segmentos; **no son diarización**. No inventar hablantes. Usar `Voz 1`/`Voz 2` sólo tras diferenciarlos de manera fiable; identidad real sólo con evidencia o confirmación del usuario.
- No eliminar muletillas o corregir gramática dentro de una cita como si fuera literal. Si se pide lectura limpia, separarla y rotularla como edición no literal; mantener negaciones, reservas y sentido. Omitir con puntos suspensivos sólo cuando no se altera contexto y la norma editorial lo admite.
- Revisar en el audio todos los tramos citables y sus segundos previos/posteriores, además de nombres, cifras y afirmaciones centrales. Una confianza del motor no reemplaza escuchar.
- Detectar falsos textos repetidos en silencio, música o ruido. No convertir una hipótesis acústica en una declaración atribuida.

## Entrega

Transcripción cruda, versión revisada si se pidió, timestamps, segmentos dudosos y límite de identificación de voces. Indicar qué se escuchó efectivamente y qué sigue pendiente. Para usar una frase en una nota, entregar también el timestamp y estado de revisión de la cita. Si no hay audio accesible, trabajar con el texto como **transcripción aportada no cotejada**, nunca afirmar que se escuchó.

## Cuando el kit se instaló dentro de otro proyecto

Los comandos anteriores parten de la raíz del checkout del kit. En un proyecto instalado, el runtime está en `.elenia-kit/`: reemplazar el prefijo `python3 scripts/elenia.py` por `python3 .elenia-kit/scripts/elenia.py`. Resolver la ruta del perfil, espacio de trabajo y modelos desde el contexto real; no crear copias redundantes para hacer funcionar un ejemplo.
