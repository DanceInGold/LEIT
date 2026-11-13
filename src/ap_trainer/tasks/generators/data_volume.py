"""Generator „Datenmengen“: Bild-, Scan-, Audio- und Videogrößen, Übertragungszeiten (AU-03).

Stufen: 1 Bildgröße aus Auflösung und Farbtiefe, 2 Übertragungszeit, 3 Scan, Audio oder Video,
4 Handlungssituation (Nachtsicherung, Overhead, Fotos pro Minute). Gerechnet wird exakt mit
Brüchen nach den Formeln der Lektionen „Datenmengen berechnen“ und „Übertragungszeit“;
die Tests rechnen jede Variante unabhängig nach. Ohne Angabe gilt dezimal (1 MB = 10⁶ Byte).
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

from ap_trainer.content.aufgaben import Aufgabe, Rechenschritt, Rechnung, Stufe
from ap_trainer.content.models import Beleg
from ap_trainer.tasks.generators import Generator, register
from ap_trainer.tasks.generators._numbers import Number, de, number_step, rounded

type _Parts = tuple[list[Rechenschritt], str, str, str | None, list[str]]

RESOLUTIONS = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160), (4000, 3000), (6000, 4000)]
DEPTHS = [8, 16, 24, 32]
PAPER = {"A4": (210, 297), "A5": (148, 210), "ein Foto 10 × 15 cm": (100, 150)}
MM_PER_INCH = Fraction(254, 10)
# Übliche Leitungsstufen in Gbit/s für „Welche Leitung reicht?“
LINE_STEPS = [1, 10, 25, 40, 100]
MB = 10**6
GB = 10**9


def image_bytes(width: int, height: int, depth: int) -> int:
    """Unkomprimierte Bildgröße in Byte: Pixel × Farbtiefe ÷ 8."""
    return width * height * depth // 8


def scan_pixels(mm: int, dpi: int) -> int:
    """Pixel einer Kante: mm → Zoll (÷ 25,4) × dpi, kaufmännisch auf ganze Pixel gerundet."""
    return int(rounded(Fraction(mm) / MM_PER_INCH * dpi, 0))


def transfer_seconds(byte_count: Number, bits_per_second: Number) -> Fraction:
    """Übertragungszeit in Sekunden: Byte × 8 ÷ Datenrate in bit/s."""
    return Fraction(byte_count) * 8 / Fraction(bits_per_second)


def _rate_text(bits_per_second: int) -> str:
    if bits_per_second >= GB:
        return f"{de(Fraction(bits_per_second, GB))} Gbit/s"
    return f"{de(Fraction(bits_per_second, MB))} Mbit/s"


BELEGE = (
    Beleg(titel="Lektion „Datenmengen berechnen“ (Bild, Scan, Audio, Video)"),
    Beleg(titel="Lektion „Übertragungszeit“ (t = Datenmenge ÷ Datenrate)"),
    Beleg(
        titel="BIPM: SI-Broschüre, 9. Auflage 2019 (SI-Präfixe; 1 Zoll = 25,4 mm)",
        url="https://www.bipm.org/en/publications/si-brochure",
    ),
)


@register
class DataVolume(Generator):
    """Datenmengen und Übertragungszeiten in vier Stufen."""

    id = "datenmengen"
    titel = "Datenmengen und Übertragungszeit"
    stufen = (1, 2, 3, 4)
    status = "ungeprüft"
    quelle = "Generator „datenmengen“; jede Variante mit exakter Bruchrechnung unabhängig nachgerechnet."
    belege = BELEGE

    def generate(self, rng: random.Random, stufe: Stufe, task_id: str, thema: str) -> Aufgabe:
        """Erzeugt eine Datenmengen-Aufgabe der gewünschten Stufe."""
        builders = {1: self._image, 2: self._transfer, 3: self._media, 4: self._situation}
        steps, title, question, situation, hints = builders[stufe](rng)
        return Rechnung(
            typ="rechnung",
            id=task_id,
            thema=thema,
            stufe=stufe,
            titel=title,
            situation=situation,
            frage=question,
            hinweise=hints,
            loesungsweg="\n".join(f"{i + 1}. **{s.frage}:** {s.erklaerung}" for i, s in enumerate(steps)),
            schritte=steps,
            quelle=self.quelle,
            belege=list(self.belege),
            status=self.status,
        )

    # --- Stufe 1: Bild ----------------------------------------------------------
    def _image(self, rng: random.Random) -> _Parts:
        width, height = rng.choice(RESOLUTIONS)
        depth = rng.choice(DEPTHS)
        pixels = width * height
        size = image_bytes(width, height, depth)
        steps = [
            number_step("Anzahl Pixel", pixels, f"{de(width)} × {de(height)} = {de(pixels)}."),
            number_step(
                "Byte je Pixel",
                Fraction(depth, 8),
                f"{depth} Bit ÷ 8 = {de(Fraction(depth, 8))} Byte.",
                "Byte",
                [(depth, "Das sind Bit. Ein Byte hat 8 Bit, also durch 8 teilen.", "begriff")],
            ),
            number_step(
                "Datenmenge in MB",
                Fraction(size, MB),
                f"{de(pixels)} × {de(Fraction(depth, 8))} Byte = {de(size)} Byte ÷ 1.000.000 = "
                f"{de(Fraction(size, MB))} MB.",
                "MB",
                [
                    (
                        Fraction(size * 8, MB),
                        "Mit Bit statt Byte gerechnet – Farbtiefe erst durch 8 teilen.",
                        "begriff",
                    ),
                    (
                        Fraction(size, 2**20),
                        "Das ist MiB (÷ 1.048.576). Gefragt ist MB, also ÷ 1.000.000.",
                        "begriff",
                    ),
                ],
            ),
        ]
        question = (
            f"Wie groß ist ein unkomprimiertes Bild mit **{width} × {height} Pixeln** und **{depth} Bit** "
            "Farbtiefe? Rechne mit 1 MB = 1.000.000 Byte."
        )
        hints = [
            "Datenmenge = Anzahl Pixel × Byte je Pixel.",
            "Farbtiefe in Bit ÷ 8 = Byte je Pixel; am Ende durch 1.000.000 für MB.",
            f"Pixel: {width} × {height}.",
        ]
        return steps, "Bildgröße berechnen", question, None, hints

    # --- Stufe 2: Übertragungszeit ------------------------------------------------
    def _transfer(self, rng: random.Random) -> _Parts:
        amount_gb = rng.choice([1, 2, 4, 5, 10, 20, 25, 50, 100, 200])
        rate = rng.choice([50 * MB, 100 * MB, 250 * MB, 500 * MB, GB, 10 * GB])
        size = amount_gb * GB
        bits = size * 8
        seconds = transfer_seconds(size, rate)
        steps = [
            number_step(
                "Datenmenge in Bit",
                bits,
                f"{amount_gb} GB = {de(size)} Byte × 8 = {de(bits)} Bit.",
                "Bit",
                [(size, "Das sind Byte. Für die Übertragungszeit braucht man Bit: × 8.", "begriff")],
            ),
            number_step("Datenrate in bit/s", rate, f"{_rate_text(rate)} = {de(rate)} bit/s.", "bit/s"),
            number_step(
                "Übertragungszeit in Sekunden",
                seconds,
                f"{de(bits)} Bit ÷ {de(rate)} bit/s = {de(seconds)} s.",
                "s",
                [(seconds / 8, "Byte durch bit/s geteilt – das Ergebnis ist achtmal zu klein.", "begriff")],
            ),
        ]
        if seconds >= 120:
            steps.append(
                number_step(
                    "Übertragungszeit in Minuten",
                    seconds / 60,
                    f"{de(seconds)} s ÷ 60 = {de(seconds / 60)} min.",
                    "min",
                    [(seconds / 100, "Eine Minute hat 60 Sekunden, nicht 100.", "rechenfehler")],
                )
            )
        question = (
            f"Eine Datei mit **{amount_gb} GB** wird über eine Leitung mit **{_rate_text(rate)}** "
            "übertragen. "
            "Wie lange dauert das ohne Overhead?"
        )
        hints = [
            "Übertragungszeit = Datenmenge ÷ Datenrate – beides in Bit.",
            "Byte × 8 = Bit; Präfixe ausschreiben (1 GB = 10⁹ Byte, 1 Mbit/s = 10⁶ bit/s).",
            f"{amount_gb} GB = {de(size)} Byte.",
        ]
        return steps, "Übertragungszeit", question, None, hints

    # --- Stufe 3: Scan, Audio, Video ------------------------------------------------
    def _media(self, rng: random.Random) -> _Parts:
        return rng.choice([self._scan, self._audio, self._video])(rng)

    def _scan(self, rng: random.Random) -> _Parts:
        name, (width_mm, height_mm) = rng.choice(list(PAPER.items()))
        dpi = rng.choice([150, 200, 300, 600])
        width, height = scan_pixels(width_mm, dpi), scan_pixels(height_mm, dpi)
        size = image_bytes(width, height, 24)
        exact_w = Fraction(width_mm) / MM_PER_INCH * dpi
        steps = [
            number_step(
                "Breite in Pixel",
                width,
                f"{width_mm} mm ÷ 25,4 × {dpi} = {de(exact_w)} → {de(width)} Pixel.",
                "Pixel",
                [(width_mm * dpi, "dpi heißt Punkte pro **Zoll** – erst mm durch 25,4 teilen.", "konzept")],
            ),
            number_step(
                "Höhe in Pixel",
                height,
                f"{height_mm} mm ÷ 25,4 × {dpi} → {de(height)} Pixel.",
                "Pixel",
            ),
            number_step(
                "Datenmenge in MB",
                Fraction(size, MB),
                f"{de(width)} × {de(height)} × 3 Byte = {de(size)} Byte = {de(Fraction(size, MB))} MB.",
                "MB",
                [(Fraction(size * 8, MB), "24 Bit sind 3 Byte, nicht 24 Byte.", "begriff")],
            ),
        ]
        question = (
            f"Die ArchivTech scannt {name} ({width_mm} × {height_mm} mm) mit **{dpi} dpi** und **24 Bit** "
            "Farbtiefe. Wie groß ist der unkomprimierte Scan? Runde die Pixel auf ganze Zahlen; 1 "
            "Zoll = 25,4 mm."
        )
        hints = [
            "Erst die Kanten in Pixel umrechnen, dann wie bei einem Bild rechnen.",
            "Pixel = mm ÷ 25,4 × dpi; Datenmenge = Breite × Höhe × 3 Byte.",
            f"Breite: {width_mm} ÷ 25,4 × {dpi}.",
        ]
        return steps, "Scan berechnen", question, None, hints

    def _audio(self, rng: random.Random) -> _Parts:
        rate = rng.choice([44_100, 48_000, 96_000])
        depth = rng.choice([16, 24])
        channels = rng.choice([1, 2])
        minutes = rng.randint(1, 10)
        per_second = rate * depth * channels
        size = Fraction(per_second * minutes * 60, 8)
        channel_text = "Stereo (2 Kanäle)" if channels == 2 else "Mono (1 Kanal)"
        steps = [
            number_step(
                "Bit pro Sekunde",
                per_second,
                f"{de(rate)} × {depth} × {channels} = {de(per_second)} bit/s.",
                "bit/s",
                [(rate * depth, "Die Kanäle fehlen: Stereo heißt × 2.", "konzept")] if channels == 2 else [],
            ),
            number_step(
                "Datenmenge in Byte",
                size,
                f"{de(per_second)} × {minutes * 60} s ÷ 8 = {de(size)} Byte.",
                "Byte",
                [(size * 8, "Das sind Bit – noch durch 8 teilen.", "begriff")],
            ),
            number_step(
                "Datenmenge in MB",
                size / MB,
                f"{de(size)} Byte ÷ 1.000.000 = {de(size / MB)} MB.",
                "MB",
            ),
        ]
        question = (
            f"Wie groß ist eine unkomprimierte Audioaufnahme von **{minutes} Minuten** mit "
            f"**{de(rate)} Hz**, "
            f"**{depth} Bit** und {channel_text}? 1 MB = 1.000.000 Byte."
        )
        hints = [
            "Audio: Abtastrate × Bittiefe × Kanäle ergibt Bit pro Sekunde.",
            "Mal Sekunden, durch 8 für Byte, durch 1.000.000 für MB.",
            f"{minutes} Minuten = {minutes * 60} Sekunden.",
        ]
        return steps, "Audio berechnen", question, None, hints

    def _video(self, rng: random.Random) -> _Parts:
        width, height = rng.choice(RESOLUTIONS[:4])
        fps = rng.choice([24, 25, 30, 50, 60])
        seconds = rng.choice([5, 10, 20, 30, 60])
        frame = image_bytes(width, height, 24)
        frames = fps * seconds
        size = frame * frames
        steps = [
            number_step(
                "Byte je Bild", frame, f"{de(width)} × {de(height)} × 3 Byte = {de(frame)} Byte.", "Byte"
            ),
            number_step(
                "Anzahl Bilder",
                frames,
                f"{fps} Bilder/s × {seconds} s = {de(frames)}.",
                falsch=[(fps, "Die Bildrate gilt pro Sekunde – mal Dauer nehmen.", "konzept")],
            ),
            number_step(
                "Datenmenge in GB",
                Fraction(size, GB),
                f"{de(frame)} × {de(frames)} = {de(size)} Byte = {de(Fraction(size, GB))} GB.",
                "GB",
                [(Fraction(size, 2**30), "Das ist GiB. Gefragt ist GB = 10⁹ Byte.", "begriff")],
            ),
        ]
        question = (
            f"Wie groß ist ein unkomprimiertes Video mit **{width} × {height}** Pixeln, 24 Bit Farbtiefe, "
            f"**{fps} Bildern pro Sekunde** und **{seconds} Sekunden** Länge? 1 GB = 10⁹ Byte."
        )
        hints = [
            "Video = Einzelbild × Anzahl Bilder.",
            "Einzelbild = Pixel × 3 Byte; Anzahl Bilder = Bildrate × Sekunden.",
            f"Ein Bild hat {de(width * height)} Pixel.",
        ]
        return steps, "Video berechnen", question, None, hints

    # --- Stufe 4: Handlungssituationen --------------------------------------------
    def _situation(self, rng: random.Random) -> _Parts:
        return rng.choice([self._backup_window, self._overhead, self._photos_per_minute])(rng)

    def _backup_window(self, rng: random.Random) -> _Parts:
        terabytes = rng.choice([1, 2, 3, 5, 8, 10, 20])
        hours = rng.choice([2, 3, 4, 6, 8])
        bits = terabytes * 10**12 * 8
        seconds = hours * 3600
        needed = Fraction(bits, seconds)
        line = next(step for step in LINE_STEPS if step * GB >= needed)
        steps = [
            number_step(
                "Datenmenge in Bit",
                bits,
                f"{terabytes} TB = {terabytes} × 10¹² Byte × 8 = {de(bits)} Bit.",
                "Bit",
            ),
            number_step(
                "Zeitfenster in Sekunden",
                seconds,
                f"{hours} h × 3.600 = {de(seconds)} s.",
                "s",
                [(hours * 600, "Eine Stunde hat 3.600 Sekunden (60 × 60), nicht 600.", "rechenfehler")],
            ),
            number_step(
                "Benötigte Datenrate in Gbit/s",
                needed / GB,
                f"{de(bits)} ÷ {de(seconds)} = {de(needed)} bit/s = {de(needed / GB)} Gbit/s.",
                "Gbit/s",
                [(needed / GB / 8, "Byte statt Bit gerechnet – die Datenmenge × 8 nehmen.", "begriff")],
            ),
            number_step(
                "Kleinste ausreichende Leitung in Gbit/s",
                line,
                f"Stufen 1, 10, 25, 40, 100 Gbit/s: die erste ≥ {de(needed / GB)} Gbit/s ist {line} Gbit/s.",
                "Gbit/s",
            ),
        ]
        situation = (
            f"Die ArchivTech GmbH spiegelt jede Nacht **{terabytes} TB** Archivdaten in ein externes "
            f"Rechenzentrum. Dafür steht ein Zeitfenster von **{hours} Stunden** zur Verfügung."
        )
        question = (
            "Welche Datenrate ist ohne Overhead mindestens nötig, und welche der üblichen Leitungsstufen "
            "(1, 10, 25, 40 oder 100 Gbit/s) reicht gerade aus?"
        )
        hints = [
            "Datenrate = Datenmenge ÷ Zeit, beides in Bit und Sekunden.",
            "1 TB = 10¹² Byte; 1 h = 3.600 s; 1 Gbit/s = 10⁹ bit/s.",
            f"{terabytes} TB × 8 = {de(terabytes * 8)} × 10¹² Bit.",
        ]
        return steps, "Nachtsicherung planen", question, situation, hints

    def _overhead(self, rng: random.Random) -> _Parts:
        amount_gb = rng.choice([10, 20, 25, 50, 100, 200])
        rate = rng.choice([100 * MB, 500 * MB, GB, 10 * GB])
        share = rng.choice([70, 75, 80, 85, 90])
        usable = Fraction(rate * share, 100)
        bits = amount_gb * GB * 8
        seconds = bits / usable
        steps = [
            number_step(
                "Nutzbare Datenrate in Mbit/s",
                usable / MB,
                f"{_rate_text(rate)} × {share} % = {de(usable / MB)} Mbit/s.",
                "Mbit/s",
                [
                    (
                        Fraction(rate * (100 - share), 100) / MB,
                        "Das ist der Overhead-Anteil, nicht die Nutzrate.",
                        "konzept",
                    )
                ],
            ),
            number_step("Datenmenge in Bit", bits, f"{amount_gb} GB × 10⁹ × 8 = {de(bits)} Bit.", "Bit"),
            number_step(
                "Übertragungszeit in Sekunden",
                seconds,
                f"{de(bits)} ÷ {de(usable)} bit/s = {de(seconds)} s.",
                "s",
                [
                    (
                        Fraction(bits, rate),
                        "Mit der vollen Datenrate gerechnet – der Overhead fehlt.",
                        "konzept",
                    )
                ],
            ),
            number_step(
                "Übertragungszeit in Minuten",
                seconds / 60,
                f"{de(seconds)} s ÷ 60 = {de(seconds / 60)} min.",
                "min",
            ),
        ]
        situation = (
            f"Ein Archivpaket der ArchivTech GmbH mit **{amount_gb} GB** soll über eine Leitung mit "
            f"**{_rate_text(rate)}** übertragen werden. Wegen Protokoll-Overhead stehen nur **{share} %** "
            "der Datenrate für Nutzdaten zur Verfügung."
        )
        question = "Wie lange dauert die Übertragung?"
        hints = [
            "Erst die nutzbare Datenrate bestimmen, dann wie gewohnt Datenmenge ÷ Datenrate.",
            f"Nutzbare Rate = Datenrate × {share} %.",
            f"{amount_gb} GB = {de(amount_gb * GB)} Byte = {de(bits)} Bit.",
        ]
        return steps, "Übertragung mit Overhead", question, situation, hints

    def _photos_per_minute(self, rng: random.Random) -> _Parts:
        width, height = rng.choice(RESOLUTIONS[3:])
        rate = rng.choice([100 * MB, 250 * MB, 500 * MB, GB])
        minutes = rng.choice([1, 2, 5])
        photo = image_bytes(width, height, 24)
        transferable = Fraction(rate * minutes * 60, 8)
        count = math.floor(transferable / photo)
        steps = [
            number_step(
                "Datenmenge eines Fotos in MB",
                Fraction(photo, MB),
                f"{de(width)} × {de(height)} × 3 Byte = {de(photo)} Byte = {de(Fraction(photo, MB))} MB.",
                "MB",
            ),
            number_step(
                "Übertragbare Datenmenge in MB",
                transferable / MB,
                f"{_rate_text(rate)} × {minutes * 60} s ÷ 8 = {de(transferable)} Byte = "
                f"{de(transferable / MB)} MB.",
                "MB",
                [
                    (
                        transferable * 8 / MB,
                        "Bit nicht durch 8 geteilt – die Leitung liefert Bit pro Sekunde.",
                        "begriff",
                    )
                ],
            ),
            number_step(
                "Vollständig übertragene Fotos",
                count,
                f"{de(transferable / MB)} ÷ {de(Fraction(photo, MB))} = {de(transferable / photo)} → "
                f"{count} vollständige Fotos.",
                falsch=[
                    (
                        count + 1,
                        "Aufgerundet – ein angefangenes Foto ist noch nicht übertragen.",
                        "rechenfehler",
                    )
                ],
            ),
        ]
        situation = (
            f"Eine Kamera an der Scanstraße der ArchivTech GmbH liefert unkomprimierte Fotos mit "
            f"**{width} × {height} Pixeln** und 24 Bit Farbtiefe. Die Leitung zum Archiv hat "
            f"**{_rate_text(rate)}**."
        )
        question = f"Wie viele Fotos lassen sich in **{minutes} Minute{'n' if minutes > 1 else ''}** "
        "vollständig übertragen?"
        hints = [
            "Rechne aus, wie viele Byte in der Zeit über die Leitung gehen, und teile durch die Fotogröße.",
            "Übertragbare Byte = Datenrate × Sekunden ÷ 8.",
            "Am Ende abrunden: nur vollständige Fotos zählen.",
        ]
        return steps, "Fotos pro Minute", question, situation, hints
