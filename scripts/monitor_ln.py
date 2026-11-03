#!/usr/bin/env python3
"""Lector del Monitor de Economía Real de LA NACION (Python estándar, >=3.10).

Descarga el índice público y las series JSON que alimentan el monitor, normaliza
fechas y números con formato argentino y conserva la procedencia. Sólo lee de
especialess3.lanacion.com.ar por HTTPS: no envía datos, no instala nada y no
escribe salvo en un archivo nuevo pedido con --salida.

El monitor es una fuente secundaria: compila datos de INDEC, BCRA y otros
organismos. Para publicar, citar y comprobar el organismo de origen.
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://especialess3.lanacion.com.ar/monitor-economia-real/data/"
INDEX = BASE + "index-mer.json"
PAGE = "https://www.lanacion.com.ar/economia/datos-economia-argentina-segui-monitor-la-nacion-nid2284152/"
MAX_BYTES = 10 * 1024 * 1024
DATE_KEYS = ("Fecha", "fecha")
NUMBER = re.compile(r"^-?\d{1,3}(\.\d{3})*(,\d+)?%?$|^-?\d+(,\d+)?%?$")


class MonitorError(Exception):
    pass


def fetch(url, opener=None):
    """GET with host allowlist, size limit and SHA256 of the exact bytes received."""
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "especialess3.lanacion.com.ar" or not parsed.path.startswith("/monitor-economia-real/data/"):
        raise MonitorError("URL no permitida: sólo se lee el monitor de LA NACION.")
    request = urllib.request.Request(url, headers={"User-Agent": "Elenia-Kit/0.1 (+monitor_ln)"})
    try:
        with (opener or urllib.request.urlopen)(request, timeout=30) as response:
            data = response.read(MAX_BYTES + 1)
            modified = response.headers.get("Last-Modified") if hasattr(response, "headers") else None
    except OSError as exc:
        raise MonitorError(f"No se pudo leer {url}: {exc}") from None
    if len(data) > MAX_BYTES:
        raise MonitorError("Respuesta mayor que 10 MB; se detuvo la lectura.")
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise MonitorError(f"{url} no devolvió JSON válido.") from None
    return payload, {"url": url, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                     "last_modified": modified,
                     "retrieved_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()}


def series_url(series_id):
    if not series_id or "/" in series_id or "\\" in series_id or series_id.startswith("."):
        raise MonitorError("Identificador de serie no válido.")
    return BASE + urllib.parse.quote(series_id + ".json")


def parse_number(raw):
    """Argentine format: '.' thousands, ',' decimal, optional '%'. Never guesses another convention."""
    if raw is None:
        return None
    text = str(raw).strip()
    if text in ("", "-", "s/d", "N/D"):
        return None
    if not NUMBER.match(text):
        raise MonitorError(f"Número con formato inesperado: {text!r}. No se interpretó.")
    return float(text.rstrip("%").replace(".", "").replace(",", "."))


def parse_date(raw):
    """dd/mm/yyyy, d/m/yyyy or dd/mm/yyyy hh:mm:ss -> ISO date. Rejects anything else."""
    if raw is None:
        return None
    match = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})(?: \d{1,2}:\d{2}(?::\d{2})?)?", str(raw).strip())
    if not match:
        return None
    day, month, year = map(int, match.groups())
    try:
        return dt.date(year, month, day).isoformat()
    except ValueError:
        return None


def parse_filter(text):
    """'tipo: Venta' -> ('tipo', 'Venta'). Empty -> None."""
    if not text or ":" not in text:
        return None
    key, value = text.split(":", 1)
    return key.strip(), value.strip()


def find_indicator(index, series_id):
    for item in index:
        if item.get("id") == series_id:
            return item
    raise MonitorError(f"No existe la serie {series_id!r} en el índice. Use 'indicadores --buscar'.")


def normalize(rows, indicator, column=None):
    """Keep dated rows, apply the monitor's own FILTER and parse the requested column."""
    column = column or indicator.get("EJE_Y")
    wanted = parse_filter(indicator.get("FILTER"))
    out, skipped = [], 0
    for row in rows:
        if not isinstance(row, dict):
            skipped += 1; continue
        date = next((parse_date(row[k]) for k in DATE_KEYS if k in row), None)
        if date is None:
            skipped += 1; continue  # first row is often the update stamp, e.g. {"Tipo": "3/11/2026"}
        if wanted:
            key = next((k for k in row if k.lower() == wanted[0].lower()), None)
            if key is None or str(row[key]).strip().lower() != wanted[1].lower():
                skipped += 1; continue
        if column not in row:
            skipped += 1; continue
        out.append({"fecha": date, "valor": parse_number(row[column]), "valor_original": row[column]})
    out.sort(key=lambda r: r["fecha"])
    return out, column, skipped


def describe(item):
    return {"id": item.get("id"), "nombre": item.get("NOMBRE"), "periodicidad": item.get("PERIODICIDAD"),
            "fuente": item.get("FUENTE"), "url_fuente": item.get("urlFuente"),
            "ultima_actualizacion": item.get("ÚLTIMA ACTUALIZACION"), "datos_desde": item.get("DATOS DESDE"),
            "variacion_mostrada": item.get("VARIACION"), "columna": item.get("EJE_Y"), "filtro": item.get("FILTER") or None,
            "descripcion": item.get("DESCRIPCIÓN"), "estado": item.get("STATUS")}


def list_indicators(search=None, opener=None):
    index, provenance = fetch(INDEX, opener)
    items = [describe(x) for x in index]
    if search:
        needle = search.lower()
        items = [x for x in items if needle in " ".join(str(v) for v in x.values() if v).lower()]
    return {"monitor": PAGE, "procedencia": provenance, "cantidad": len(items), "indicadores": items}


def get_series(series_id, column=None, since=None, until=None, opener=None):
    index, index_prov = fetch(INDEX, opener)
    indicator = find_indicator(index, series_id)
    rows, prov = fetch(series_url(series_id), opener)
    if not isinstance(rows, list):
        raise MonitorError("La serie no tiene el formato de lista esperado.")
    data, used, skipped = normalize(rows, indicator, column)
    if not data:
        available = sorted({k for r in rows if isinstance(r, dict) for k in r} - set(DATE_KEYS))
        raise MonitorError(f"La columna {used!r} no tiene datos en esta serie. Columnas disponibles: "
                           + ", ".join(available) + ". Elija una con --columna.")
    if since:
        data = [r for r in data if r["fecha"] >= since]
    if until:
        data = [r for r in data if r["fecha"] <= until]
    return {"indicador": describe(indicator), "columna_usada": used, "filas": len(data), "filas_descartadas": skipped,
            "primera": data[0] if data else None, "ultima": data[-1] if data else None,
            "procedencia": prov, "indice": index_prov, "datos": data,
            "advertencia": "Fuente secundaria (LA NACION). Verificar y citar el organismo de origen indicado en 'fuente'."}


def iso_date(value):
    try:
        return dt.date.fromisoformat(value).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError("Use AAAA-MM-DD.") from None


def write_output(path, result):
    path = Path(path)
    if path.exists():
        raise MonitorError(f"{path} ya existe; no se sobrescribió. Elija otro nombre.")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".csv":
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["fecha", "valor", "valor_original"])
        for row in result["datos"]:
            writer.writerow([row["fecha"], "" if row["valor"] is None else repr(row["valor"]), row["valor_original"]])
        meta = path.with_suffix(".procedencia.json")
        if meta.exists():
            raise MonitorError(f"{meta} ya existe; no se sobrescribió.")
        content = buffer.getvalue()
        with path.open("x", encoding="utf-8", newline="") as f:
            f.write(content)
        with meta.open("x", encoding="utf-8") as f:
            json.dump({k: v for k, v in result.items() if k != "datos"}, f, ensure_ascii=False, indent=2)
    elif path.suffix.lower() == ".json":
        with path.open("x", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        raise MonitorError("--salida debe terminar en .csv o .json.")


def parser():
    p = argparse.ArgumentParser(description="Monitor de Economía Real de LA NACION: listar indicadores y descargar series normalizadas.")
    commands = p.add_subparsers(dest="command", required=True)
    c = commands.add_parser("indicadores", help="Listar los indicadores del monitor")
    c.add_argument("--buscar", help="Filtrar por texto (nombre, fuente, descripción)")
    c = commands.add_parser("serie", help="Descargar una serie normalizada")
    c.add_argument("--id", required=True, help="id del indicador, tal como aparece en 'indicadores'")
    c.add_argument("--columna", help="Columna a leer; por defecto la que grafica el monitor")
    c.add_argument("--desde", type=iso_date)
    c.add_argument("--hasta", type=iso_date)
    c.add_argument("--salida", help="Archivo nuevo .csv (con .procedencia.json) o .json con la serie completa")
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "indicadores":
            result = list_indicators(args.buscar)
        else:
            result = get_series(args.id, args.columna, args.desde, args.hasta)
            if args.salida:
                write_output(args.salida, result)
                result["salida"] = str(Path(args.salida).resolve())
            # Keep the chat short: the full series goes to --salida, not to the model.
            result["ultimos_12"] = result.pop("datos")[-12:]
        sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except MonitorError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
