import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("monitor_ln", ROOT / "scripts/monitor_ln.py")
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

INDEX = [
    {"id": "dólar_blue", "NOMBRE": "Dólar blue", "PERIODICIDAD": "Diario", "FUENTE": "Rava Bursátil", "EJE_Y": "cotizacion",
     "FILTER": "tipo: Venta", "ÚLTIMA ACTUALIZACION": "02/11/2026", "STATUS": "ok"},
    {"id": "inflación_(ipc)", "NOMBRE": "Inflación (IPC)", "PERIODICIDAD": "Mensual", "FUENTE": "INDEC", "EJE_Y": "Indice",
     "FILTER": "Tipo: IPC", "ÚLTIMA ACTUALIZACION": "01/09/2026", "STATUS": "ok"},
    {"id": "venta_de_autos_usados", "NOMBRE": "Venta de autos usados", "FUENTE": "CCA", "EJE_Y": "total", "FILTER": "", "STATUS": "ok"},
]
SERIES = {
    "dólar_blue": [{"tipo": "02/11/2026 17:50:55"},
                   {"tipo": "Compra", "cotizacion": "1.545", "Fecha": "02/11/2026"},
                   {"tipo": "Venta", "cotizacion": "1.565", "Fecha": "02/11/2026"},
                   {"tipo": "Venta", "cotizacion": "1.560,50", "Fecha": "30/10/2026"}],
    "inflación_(ipc)": [{"Tipo": "3/11/2026"}, {"Tipo": "IPC", "Indice": "2,10", "Fecha": "1/8/2026"},
                        {"Tipo": "IPC", "Indice": "1,90", "Fecha": "01/09/2026"}],
    "venta_de_autos_usados": [{"Categoria": "6/09/2026 6:00:45"}, {"Categoria": "Autos usados", "Cantidad": "127.062", "Fecha": "01/01/2016"}],
}


class FakeResponse(io.BytesIO):
    headers = {"Last-Modified": "Tue, 03 Nov 2026 11:46:01 GMT"}
    def __enter__(self): return self
    def __exit__(self, *a): self.close()


def opener(request, timeout):
    name = request.full_url.rsplit("/", 1)[1]
    if name == "index-mer.json":
        return FakeResponse(json.dumps(INDEX).encode("utf-8"))
    key = M.urllib.parse.unquote(name)[:-5]
    return FakeResponse(json.dumps(SERIES[key]).encode("utf-8"))


class MonitorTests(unittest.TestCase):
    def test_argentine_numbers(self):
        self.assertEqual(M.parse_number("1.991.316,00"), 1991316.0)
        self.assertEqual(M.parse_number("-2,59%"), -2.59)
        self.assertEqual(M.parse_number("1.046"), 1046.0)
        self.assertEqual(M.parse_number("803"), 803.0)
        self.assertIsNone(M.parse_number(""))
        for bad in ("1.5", "1,234.5", "12a"):
            with self.subTest(bad=bad), self.assertRaises(M.MonitorError):
                M.parse_number(bad)

    def test_dates(self):
        self.assertEqual(M.parse_date("1/8/2026"), "2026-08-01")
        self.assertEqual(M.parse_date("02/11/2026 17:50:55"), "2026-11-02")
        self.assertIsNone(M.parse_date("31/02/2026"))
        self.assertIsNone(M.parse_date("Venta"))

    def test_series_skips_stamp_applies_monitor_filter_and_sorts(self):
        result = M.get_series("dólar_blue", opener=opener)
        self.assertEqual([r["fecha"] for r in result["datos"]], ["2026-10-30", "2026-11-02"])
        self.assertEqual(result["ultima"]["valor"], 1565.0)
        self.assertEqual(result["filas_descartadas"], 2)  # update stamp + "Compra"
        self.assertEqual(len(result["procedencia"]["sha256"]), 64)
        self.assertIn("organismo de origen", result["advertencia"])

    def test_date_window(self):
        result = M.get_series("inflación_(ipc)", since="2026-09-01", opener=opener)
        self.assertEqual(result["filas"], 1)
        self.assertEqual(result["ultima"], {"fecha": "2026-09-01", "valor": 1.9, "valor_original": "1,90"})

    def test_declared_column_missing_is_reported_not_silently_empty(self):
        with self.assertRaisesRegex(M.MonitorError, "Cantidad"):
            M.get_series("venta_de_autos_usados", opener=opener)
        self.assertEqual(M.get_series("venta_de_autos_usados", column="Cantidad", opener=opener)["ultima"]["valor"], 127062.0)

    def test_unknown_series_and_host_allowlist(self):
        with self.assertRaises(M.MonitorError):
            M.get_series("no_existe", opener=opener)
        for url in ("http://especialess3.lanacion.com.ar/monitor-economia-real/data/x.json",
                    "https://evil.example/monitor-economia-real/data/x.json",
                    "https://especialess3.lanacion.com.ar/otra-cosa/x.json"):
            with self.subTest(url=url), self.assertRaises(M.MonitorError):
                M.fetch(url, opener)
        with self.assertRaises(M.MonitorError):
            M.series_url("../index-mer")

    def test_search(self):
        result = M.list_indicators("indec", opener=opener)
        self.assertEqual([x["id"] for x in result["indicadores"]], ["inflación_(ipc)"])

    def test_csv_output_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "blue.csv"
            result = M.get_series("dólar_blue", opener=opener)
            M.write_output(out, result)
            self.assertEqual(out.read_text(encoding="utf-8").splitlines()[1], "2026-10-30,1560.5,\"1.560,50\"")
            self.assertTrue((Path(tmp) / "blue.procedencia.json").is_file())
            with self.assertRaises(M.MonitorError):
                M.write_output(out, result)


if __name__ == "__main__":
    unittest.main()
