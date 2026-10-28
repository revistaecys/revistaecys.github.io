"""Pruebas sin internet de la actualización local y CI de ECYS."""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

BASE = pathlib.Path(__file__).resolve().parent.parent
GENERADOR = BASE / "scripts" / "generar_catalogo.py"


class CatalogoTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        (self.root / "scripts").mkdir()
        shutil.copy(BASE / "index.html", self.root / "index.html")
        shutil.copy(BASE / "scripts" / "ediciones_base.json",
                    self.root / "scripts" / "ediciones_base.json")
        self.edition("29Edicion", pdf="Revista_ECYS_XXIX.pdf")

    def edition(self, name, pdf=None, with_index=True):
        folder = self.root / name
        folder.mkdir(exist_ok=True)
        if with_index:
            (folder / "index.html").write_text("<!doctype html><title>prueba</title>", encoding="utf-8")
        if pdf:
            (folder / pdf).write_bytes(b"%PDF-1.4\n")

    def run_generator(self, *args, expected=0):
        call = subprocess.run([sys.executable, str(GENERADOR), "--root", str(self.root), *args],
                              text=True, capture_output=True)
        self.assertEqual(call.returncode, expected, call.stdout + call.stderr)
        return call

    def data(self):
        catalog = json.loads((self.root / "ediciones.json").read_text(encoding="utf-8"))
        html = (self.root / "index.html").read_text(encoding="utf-8")
        match = re.search(r"const editions = (\[[\s\S]*?\]);", html)
        self.assertIsNotNone(match)
        self.assertEqual(catalog["editions"], json.loads(match.group(1)))
        return catalog["editions"], html

    def test_incial_y_offline(self):
        self.run_generator()
        editions, html = self.data()
        self.assertEqual(len(editions), 22)
        self.assertEqual(editions[0]["url"], "29Edicion/index.html")
        self.assertEqual(editions[0]["pdf"], "29Edicion/Revista_ECYS_XXIX.pdf")
        self.assertIn("https://revistaecys.github.io/28Edicion/", html)
        self.assertNotIn("probeOwnSite", html)
        self.assertNotIn("fetch(", html)
        self.assertNotIn("localhost", html)
        self.assertNotIn('id="refreshEditions"', html)
        self.assertIn('G-V6HS3KRG7S', html)
        self.run_generator("--check")

    def test_nuevas_ediciones_y_orden(self):
        self.edition("30Edicion", pdf="edicion_30.pdf")
        self.edition("31Edision")
        self.edition("40edicion", pdf="PRESUPUESTO.PDF")
        self.edition("33Edicion", with_index=False)
        self.run_generator()
        editions, html = self.data()
        self.assertEqual([d["edition"] for d in editions[:4]], [40, 31, 30, 29])
        self.assertEqual(editions[1]["name"], "Trigésima Primera Edición")
        self.assertEqual(editions[2]["pdf"], "30Edicion/edicion_30.pdf")
        self.assertNotIn(33, [d["edition"] for d in editions])
        self.assertEqual(editions[0]["url"], "40edicion/index.html")
        self.assertIn("selectEdition(editions.some(e=>e.edition===requested)?requested:newest)", html)
        self.run_generator("--check")

    def test_no_duplicar_y_priorizar_grafia_correcta(self):
        self.edition("30Edision")
        self.edition("30Edicion")
        self.edition("02Edicion")
        self.run_generator()
        editions, _ = self.data()
        self.assertEqual(sum(e["edition"] == 30 for e in editions), 1)
        self.assertEqual(editions[0]["url"], "30Edicion/index.html")
        self.assertEqual(next(e for e in editions if e["edition"] == 2)["url"],
                         "02Edicion/index.html")

    def test_borrado_y_ejecucion_repetida(self):
        self.edition("30Edicion")
        self.run_generator()
        self.assertEqual(self.run_generator("--check").returncode, 0)
        (self.root / "30Edicion" / "index.html").unlink()
        self.run_generator("--check", expected=1)
        self.run_generator()
        editions, _ = self.data()
        self.assertNotIn(30, [e["edition"] for e in editions])
        self.run_generator("--check")

    def test_escapa_rutas_y_no_reescribe_fuera_de_cambios(self):
        self.edition("32Edicion", pdf="Revista ECYS XXII (nueva).pdf")
        self.run_generator()
        editions, _ = self.data()
        self.assertIn("%20", editions[0]["pdf"])
        before = (self.root / "index.html").read_bytes()
        self.run_generator()
        self.assertEqual(before, (self.root / "index.html").read_bytes())
        self.run_generator("--check")


if __name__ == "__main__":
    unittest.main()
