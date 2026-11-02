# Rutas de fuentes · Argentina, México, Perú, Colombia y Costa Rica

Registro de consulta: **2026-11-01**. Son rutas a fuentes, no conectores implementados ni garantía de disponibilidad. Abrir el registro/documento específico antes de emitir un resultado. Si cambian el sitio, las condiciones o la jurisdicción, actualizar la configuración y la fecha. No fijar la arquitectura del método a estos cinco países.

## Seleccionar la jurisdicción

El país del medio es un punto de partida, no el país de todos los hechos. Identificar la jurisdicción de cada afirmación y consultar su paquete: no comprobar un dato peruano con un registro colombiano porque el periodista trabaje allí. Un medio no se convierte en fuente independiente para cualquier afirmación por su prestigio o su red de alianzas.

- Argentina y México: rutas abajo.
- [Perú](fuentes-pe.md).
- [Colombia](fuentes-co.md).
- [Costa Rica](fuentes-cr.md).

El catálogo de medios con perfil de partida está en `config/medios.json`; las rutas son documentos, no conectores instalados.

## Argentina

| Necesidad | Ruta oficial verificada | Acceso y cuidado |
|---|---|---|
| Precios, empleo, población, cuentas nacionales | [INDEC](https://www.indec.gob.ar/) | Publicaciones, tablas y metodologías públicas. Comparar período, cobertura y revisión. |
| Catálogo de servicios estadísticos | [API-INDEC](https://api.indec.gob.ar/) | Catálogo público marcado beta al consultar. Abrir documentación de cada servicio; no suponer endpoint, credenciales ni cobertura. Usar publicación descargable si no hay ruta estable. |
| Tasas, moneda, reservas, series monetarias | [BCRA](https://www.bcra.gob.ar/) | Navegar a estadísticas/catálogo o la documentación de API enlazada desde el sitio. Distinguir tasas, instrumentos y tipos de cambio. No convertir una cotización en «el dólar» sin especificar mercado/fecha. |
| Normas y actos publicados | [Boletín Oficial](https://www.boletinoficial.gob.ar/) | El acceso automático a la portada agotó el tiempo en esta revisión; comprobar en navegador y leer el acto completo. No usar un extracto de buscador como norma vigente. |
| Justicia electoral, resoluciones y escrutinio definitivo | [Cámara Nacional Electoral](https://www.electoral.gob.ar/nuevo/) | Identificar competencia, elección y documento. No confundir resultados provisorios con definitivos. |

## México

| Necesidad | Ruta oficial verificada | Acceso y cuidado |
|---|---|---|
| Población, precios, economía, encuestas | [INEGI](https://www.inegi.org.mx/) | Publicaciones y metodologías públicas; precisar diseño muestral, período y geografía. |
| Extracción de indicadores por API | [Documentación INEGI](https://www.inegi.org.mx/servicios/api_indicadores.html) | La API requiere token válido obtenido mediante registro. No crear cuenta ni pedir token en el chat por defecto; usar publicación o descarga pública. |
| Tasas, tipo de cambio y series monetarias | [Banco de México](https://www.banxico.org.mx/) | Indicadores y publicaciones públicas. La [API SIE](https://www.banxico.org.mx/SieAPIRest/service/v1/) exige token y tiene límites de consultas; usar documentación vigente. No copiar tokens de ejemplo ni guardarlos en el perfil. |
| Normas publicadas | [Diario Oficial de la Federación](https://www.dof.gob.mx/) | La portada agotó el tiempo en esta revisión automática. Acceder en navegador autorizado, identificar edición/fecha y texto íntegro. Publicación no equivale necesariamente a entrada en vigor. |
| Elecciones, acuerdos y datos electorales | [INE](https://www.ine.mx/) | Distinguir PREP, cómputos y decisiones jurisdiccionales; acudir al órgano competente para la cuestión concreta. |
| Resoluciones judiciales constitucionales | [SCJN](https://www.scjn.gob.mx/) | Acceso automático devolvió 403 en esta revisión. Probar navegación autorizada; no deducir contenido de una sentencia por un titular o una ficha. |

## Comparación regional y nuevos países

[CEPALSTAT](https://statistics.cepal.org/portal/cepalstat/open-data.html?lang=es) ofrece una ruta pública a su sección Open Data; esta revisión no recuperó texto legible de esa página dinámica. Confirmar documentación, indicadores y metodología antes de automatizar. Una serie armonizada puede diferir de la última publicación nacional; explicarlo, no escoger la que favorece el título.

Para agregar un país, crear un paquete de configuración con código ISO, idioma, estadística nacional, banco central, diario oficial, justicia/elecciones y rutas temáticas. Cada entrada necesita URL oficial, qué acredita, documentación, requisitos de acceso, fecha de verificación, limitaciones y alternativa sin cuenta. **No inventar URLs de APIs, IDs de series ni llaves.** Las consultas deben minimizar el contenido inédito enviado al exterior.

Los registros pueden contener revisiones, subregistro, errores o incentivos institucionales. Evaluar metodología, cobertura y contradicciones con fuentes independientes. Esta lista orienta una investigación; no reemplaza conocer la jurisdicción ni el análisis de la fuente.
