# Medios con perfil de partida · referencia para el onboarding

**Consulta: 2026-11-01.** El kit se desarrolló en LA NACION (Argentina) y trae ese medio como único perfil de partida verificado. No es un manual de estilo ni una política oficial del diario: las pautas se investigan igual en cada onboarding.

| País | Medio | Sitio oficial |
|---|---|---|
| Argentina | LA NACION | [lanacion.com.ar](https://www.lanacion.com.ar/) |

## Uso en el perfil

El registro legible por máquina está en `config/medios.json` del kit; en una instalación dentro de otro proyecto, `.elenia-kit/config/medios.json`. Sus campos identifican medio, país, URL, idioma editorial y estado del paquete de fuentes. No guardar esta lista como preferencias personales ni como reglas oficiales del medio.

- Proponer la coincidencia usando medio **más dominio o país**, no el nombre solo. «La Nación» también es el nombre de un diario de Costa Rica (`nacion.com`): si el usuario no da URL ni país, preguntar; no elegir por su acento o nacionalidad supuesta.
- Buscar políticas públicas, muestra reciente de sección/género y firmas propias como indica la skill.
- Si el medio no está en el catálogo, continuar igualmente con el medio indicado y su URL oficial. No forzar un ID del registro ni cambiar el país de cobertura para hacerlo encajar.

## Alcance real del kit

Hay rutas de fuentes curadas para **AR, MX, PE, CO y CR**, seleccionadas por la jurisdicción del hecho, no por el medio. Incluso en un país cubierto hay que abrir y evaluar la fuente concreta: una lista de dominios no verifica una afirmación.

Para trabajo en otro idioma (por ejemplo portugués), confirmar idioma del encargo y probar por separado reconocimiento, modelos locales, diccionarios y revisión editorial. La preparación de OCR en español no acredita soporte en otro idioma. No descargar datos de idioma ni enviar texto a una nube para cubrir esa diferencia sin autorización.

Revisar el registro cuando envejezca o aparezca una discrepancia; conservar fecha y fuente de la nueva consulta. Los países de la persona, de su medio y de la noticia pueden ser distintos: el perfil y las rutas del encargo deben reflejar esa diferencia.
