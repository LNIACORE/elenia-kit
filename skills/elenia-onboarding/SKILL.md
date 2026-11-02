---
name: elenia-onboarding
description: Configurar un asistente periodístico con perfil del periodista y del medio, investigación pública de estilo y preparación técnica guiada; usar al comenzar o al actualizar ese perfil.
---
# Conocer a la persona, al medio y al equipo

> **Reglas comunes y ubicación del kit.** Antes de actuar, leer `AGENTS.md` del kit: en el kit fuente está en la raíz; instalado en un proyecto, en `.elenia-kit/AGENTS.md`; instalado de forma global, en `~/.elenia-kit/AGENTS.md` (Windows: `%USERPROFILE%\.elenia-kit\AGENTS.md`). Los comandos `python3 scripts/elenia.py` de esta skill se ejecutan desde esa misma ubicación del kit.

## Conversación inicial

Pedir en un solo mensaje breve lo que no conste ya: **nombre y firma habitual; medio y URL; rol o perfil profesional; sección o temas; tono y formatos frecuentes**. Preguntar también el país si no puede deducirse de forma fiable. No pedir RAM, arquitectura, rutas de binarios, modelos ni claves API al periodista.

Ejemplo: «¿Cómo firmás, en qué medio y sección trabajás y qué producís más: notas, entrevistas, explicadores, newsletters u otro formato? Si tenés una preferencia de tono, contámela. Yo busco las pautas públicas y preparo el equipo». Adaptar voseo/tuteo a la persona, no al país supuesto.

No deducir identidad, género, nacionalidad ni cargo a partir del nombre. Si el usuario trabaja en varios medios, separar perfiles o señalar la prioridad para este encargo.

## Reconocer el medio sin encasillar al periodista

Leer [medios.md](references/medios.md) y el registro `config/medios.json` (en un proyecto instalado: `.elenia-kit/config/medios.json`). Hoy contiene sólo LA NACION (Argentina), el medio donde se desarrolló el kit. Usarlo para proponer y verificar dominio, país e idioma, no para atribuir afiliación por el nombre de la persona. Desambiguar homónimos mediante URL o país: «La Nación» también es un diario de Costa Rica.

El catálogo no contiene políticas de estilo. Las rutas de fuentes curadas cubren **Argentina, México, Perú, Colombia y Costa Rica** según la jurisdicción del hecho. Si el encargo es en otro idioma, comprobar idioma/modelos: no prometer OCR listo porque el perfil admita ese código de idioma.

Aceptar cualquier medio y periodistas independientes. El registro orienta, no restringe el perfil. Para cualquier medio, continuar con la búsqueda editorial y de firmas que sigue.

## Investigar antes de pedir una bibliografía

1. En el dominio oficial del medio, buscar manual de estilo, principios editoriales, correcciones, ética y políticas de IA o uso de fuentes. Verificar autoría institucional, alcance y vigencia. Una nota de opinión sobre el estilo no es un manual oficial. Si no se encuentra nada público, escribir «no encontrado en la búsqueda realizada», no «el medio no tiene reglas».
2. Leer piezas recientes de la **sección y género** relevantes: empezar por una muestra manejable de 3–5 textos completos; ampliar sólo si el estilo es heterogéneo. Registrar fechas, URLs y el criterio de selección. Separar noticia, columna, agencia, publicidad y contenido de servicio. Si sólo se accede a fragmentos o titulares, limitar la inferencia a eso.
3. Buscar por iniciativa propia las firmas de la persona dentro del medio y su página de autor. Comparar firma, sección, biografía profesional pública y medio para descartar homónimos; no usar datos privados. Preferir una página de autor enlazada desde las propias notas. Ante una coincidencia dudosa, pedir confirmación antes de atribuirla.
4. Examinar sus notas verificadas para detectar estructura, ritmo, uso de citas, explicaciones y formatos. No copiar frases distintivas ni inferir creencias personales. No encontrar notas propias **no bloquea**: avanzar con reglas oficiales, muestra de sección y preferencias declaradas; marcar «voz personal aún no validada».

La búsqueda inicial de políticas y firmas públicas forma parte del onboarding. Nunca usar como consulta el contenido reservado de un borrador ni el nombre de una fuente protegida. Si el medio o la relación laboral son confidenciales, consultar primero el alcance autorizado.

## Construir y confirmar el perfil

Leer [perfil-editorial.md](references/perfil-editorial.md). Separar siempre:
- `explicit`: regla atribuible a una política oficial del medio, con fuente;
- `inferred`: patrón observado en la muestra, con límites y confianza descritos;
- `preference`: elección expresada por el usuario, no una política institucional.

Mostrar una síntesis corta de las tres capas y pedir correcciones/confirmación. Una regla pendiente no se guarda como aprobada. Registrar fecha de consulta, URLs, corpus y excepciones. Una preferencia que contradice una regla pública requiere señalar el conflicto, no ocultarlo. Ninguna capa autoriza alterar hechos, citas o incertidumbre.

La preparación técnica puede avanzar mientras la confirmación editorial está pendiente. El usuario no necesita redactar JSON: el agente lo prepara y valida. No guardar datos de contactos, entrevistas, contraseñas o tokens en el perfil.

## Preparar la máquina sin delegar el trabajo técnico

Leer [preparacion-tecnica.md](references/preparacion-tecnica.md) antes de ejecutar. Inspeccionar capacidades locales con comandos de lectura, proponer la opción proporcional al equipo y pedir aprobación **antes** de instalar o descargar. La persona elige entre una explicación simple («más rápido» / «mejor calidad»), no entre flags.

No afirmar que algo funciona porque existe un ejecutable: probarlo con el material ficticio del kit, conservar evidencia de la prueba y reportar qué quedó operativo y qué falta. Si faltan permisos o una capacidad, dejar utilizable el resto del kit; no subir archivos como alternativa silenciosa.

## Entrega

Perfil confirmado o claramente pendiente; fuentes que lo sustentan; capacidades disponibles; bloqueos concretos y una primera tarea sugerida. No publicar nada ni convertir la autorización de preparación en permiso para procesar material reservado en terceros.
