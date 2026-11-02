# Cambios de la v0.1

## Identidad Elenia y apertura · 1 de noviembre de 2026

- El kit pasa a llamarse **Elenia** y se publica como open source (MIT) desde una cuenta personal. Desarrollado en LA NACION; no es un producto oficial del diario.
- El catálogo de medios (`config/medios.json`) queda sólo con LA NACION; cualquier otro medio se configura desde el onboarding. Se conserva la advertencia de homonimia con La Nación de Costa Rica.
- Se retiran las referencias a otros medios y redes en skills, documentación y ejemplos. Las rutas de fuentes por país (AR, MX, PE, CO, CR) no cambian.

## Preparación para repositorio · 1 de noviembre de 2026

- Corregido: en Windows, el runtime rechazaba rutas con subcarpetas (instalación de skills, descargas, copia de originales). La validación ahora usa `as_posix()` y rechaza también rutas relativas a unidad.
- Corregido: lecturas de texto con codificación explícita UTF-8 en runtime y pruebas.
- Nuevos: `.gitattributes` (LF obligatorio para anclajes y checksums), `LICENSE` MIT, `CONTRIBUTING.md`, `SECURITY.md`, plantillas de issues e integración continua en Linux/Windows/macOS.
- 119 pruebas aprobadas en Windows 11 (2 omitidas por plataforma). Checksums regenerados.

## Ampliación regional · 1 de noviembre de 2026

- Rutas documentales añadidas: Perú, Colombia y Costa Rica. Cobertura inicial: AR, MX, PE, CO y CR.
- Catálogo de medios para desambiguar nombre/país/dominio en el onboarding (reducido luego a LA NACION).
- Onboarding consulta el catálogo para desambiguar nombre/país/dominio, sin convertir la membresía en reglas editoriales.
- Medios de otro idioma se señalan como tales; el catálogo no promete OCR ni evaluación de audio en otros idiomas.
- Accesos restringidos, tokens, CAPTCHA, portales dinámicos y consultas no probadas quedan señalados en cada ruta.
- 82 pruebas automatizadas aprobadas; no cambian los límites de verificación de motores de la entrega inicial.
- Sin Splash, sin publicación externa y sin nuevas instalaciones en el equipo del usuario.

Esta revisión actualiza el mismo paquete; no requiere configurar perfiles de periodistas desde cero. El instalador no sobrescribe archivos diferentes: para una instalación previa, comparar y aplicar cambios revisados con autorización, conservando los perfiles.

## Analista de discursos y entrevistas · nueva revisión de v0.1

- Nueva séptima skill `elenia-discursos`, plantillas de ingreso/inventario/evidencia/informe/revisión y esquema JSON.
- Ejemplo central: video de Milei en Universidad Torcuato Di Tella aportado por el usuario. Ficha real parcial documentada, sin trasplantar las frases de otro caso incluido en el prompt metodológico. Ejercicio sintético separado para pruebas.
- Inventario literal → selección humana → evidencia fechada/versionada → informe → revisión de versión concreta. Opiniones, proyecciones y promesas separadas del chequeo factual.
- Catálogo neutral de hipótesis contrastables, no etiquetas de engaño ni causalidades preestablecidas. Dato pertinente a la fecha, con revisiones posteriores explícitas.
- Validador offline `scripts/validate_discourse.py`: anclas, cortes, precisión temporal, consistencia de estados y hash de revisión. No comprueba la verdad, la exhaustividad ni la identidad humana, ni autoriza publicar.
- 118 pruebas aprobadas. Instalador existente incluye módulo y archivos de apoyo para los tres adaptadores; no sobrescribe instalaciones distintas.
- Sin app, video, conectores nuevos, instalaciones adicionales ni publicación externa. Continúa la versión v0.1 de evaluación, con nueva revisión del mismo paquete.
