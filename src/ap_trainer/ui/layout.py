"""Gemeinsamer Seitenrahmen: Seitenleiste mit Countdown und Navigation, Hell/Dunkel, Smartphone.

Alle Seiten rufen :func:`frame` auf. Auf großen Bildschirmen steht die Navigation dauerhaft links,
auf dem Smartphone klappt sie über die Menütaste in der Kopfzeile auf (NF-01, NF-05). Farben und
Schrift kommen aus den CSS-Variablen in ``_CSS`` (Design E-43: Nachtblau und Schiefergrau).
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from nicegui import ui


@dataclass(frozen=True)
class NavItem:
    """Ein Eintrag der Seitenleiste; ``also`` sind weitere Pfade, bei denen er aktiv ist."""

    label: str
    target: str
    icon: str
    also: tuple[str, ...] = ()

    def matches(self, path: str) -> bool:
        """True, wenn ``path`` (Seitenmuster wie ``/ueben/{topic_id}``) zu diesem Eintrag gehört."""
        if self.target == "/":
            return path == "/"
        return any(path == p or path.startswith(p + "/") for p in (self.target, *self.also))


# Navigation in drei Gruppen: lernen, üben, Überblick behalten; Einstellungen unten
NAV: list[tuple[str, list[NavItem]]] = [
    (
        "Lernen",
        [
            NavItem("Heute", "/", "wb_sunny"),
            NavItem("Lernplan", "/plan", "event_note"),
            NavItem("Themen", "/themen", "account_tree", ("/thema", "/lektion")),
            NavItem("Glossar", "/glossar", "menu_book"),
        ],
    ),
    (
        "Üben",
        [
            NavItem("Aufgaben", "/ueben", "edit_note", ("/mischtest", "/fehler", "/operatoren")),
            NavItem("Lernkarten", "/lernkarten", "style"),
            NavItem("Prüfungssimulation", "/simulation", "timer"),
        ],
    ),
    ("Überblick", [NavItem("Fortschritt", "/fortschritt", "insights")]),
]
SETTINGS = NavItem("Einstellungen", "/einstellungen", "tune")

AMPEL_COLORS = {"im Plan": "positive", "knapp": "warning", "im Verzug": "negative"}

# Quasar-Markenfarben (Knöpfe, Fortschrittsbalken, Hinweise)
PALETTE = {
    "primary": "#3a66d6",
    "secondary": "#2a3446",
    "accent": "#6d97f2",
    "dark": "#19212f",
    "positive": "#3fa774",
    "negative": "#d65c5c",
    "warning": "#d9a640",
    "info": "#6d97f2",
}

# IBM Plex Sans; ohne Internet greift die Systemschrift
_FONT = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700'
    '&display=swap" rel="stylesheet">'
)

_CSS = """
:root {
  --leit-bg: #edf0f5; --leit-surface: #ffffff; --leit-surface-2: #f4f6fa; --leit-line: #d7dde7;
  --leit-text: #18233a; --leit-muted: #5b6678; --leit-accent: #2a56c6;
  --leit-rail: #0b1322; --leit-rail-text: #c9d3e3; --leit-rail-muted: #7d8aa1; --leit-rail-hover: #16223a;
  --q-dark-page: #0d1626;
}
.body--dark {
  --leit-bg: #0d1626; --leit-surface: #19212f; --leit-surface-2: #222b3b; --leit-line: #2c3749;
  --leit-text: #e4e9f1; --leit-muted: #95a1b4; --leit-accent: #6d97f2;
}
body {
  font-family: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  background: var(--leit-bg); color: var(--leit-text); font-feature-settings: "tnum" 1;
}
.body--dark { background: var(--leit-bg) !important; }
.nicegui-markdown a, .q-page a:not(.q-btn) { color: var(--leit-accent); }
:focus-visible { outline: 2px solid var(--leit-accent); outline-offset: 2px; }

/* Flächen: Linien statt Schatten, Radius nach Hierarchie (Karte 14 px, Elemente darin 10 px) */
.q-card { background: var(--leit-surface); border: 1px solid var(--leit-line); box-shadow: none;
          border-radius: 14px; color: var(--leit-text); }
.q-card--dark { background: var(--leit-surface); }
.q-expansion-item { border: 1px solid var(--leit-line); border-radius: 10px;
                    background: var(--leit-surface); }
.q-expansion-item + .q-expansion-item { margin-top: 0.4rem; }
.q-btn { text-transform: none; font-weight: 600; letter-spacing: 0; border-radius: 10px; }
.q-field--outlined .q-field__control { border-radius: 10px; }
.q-linear-progress { border-radius: 99px; overflow: hidden; }
.q-dialog .q-card { border-radius: 16px; }

/* Typografie */
.leit-title { font-size: 1.75rem; line-height: 1.2; font-weight: 600; letter-spacing: -0.01em; margin: 0; }
.leit-section { font-size: 1.125rem; font-weight: 600; margin-top: 0.75rem; }
.leit-meta { font-size: 0.8rem; color: var(--leit-muted); }
.opacity-60, .opacity-70, .opacity-80 { opacity: 1 !important; color: var(--leit-muted); }

/* Seitenleiste */
.leit-rail { background: var(--leit-rail) !important; color: var(--leit-rail-text); }
.leit-rail .q-drawer__content { display: flex; flex-direction: column; }
.leit-brand { font-weight: 700; font-size: 1.05rem; letter-spacing: 0.04em; color: #ffffff; }
.leit-brand-sub { font-size: 0.8rem; color: var(--leit-rail-muted); }
.leit-countdown { padding: 0.9rem 1rem; border-radius: 12px; background: #13203a; }
.leit-countdown-days { font-size: 2.6rem; font-weight: 600; line-height: 1; color: #ffffff; }
.leit-countdown-label { font-size: 0.85rem; color: var(--leit-rail-text); }
.leit-countdown-track { height: 4px; border-radius: 99px; background: #23324f; margin-top: 0.7rem; }
.leit-countdown-fill { height: 4px; border-radius: 99px; background: #6d97f2; }
.leit-group { font-size: 0.78rem; color: var(--leit-rail-muted); margin: 1.1rem 0 0.25rem 0.75rem; }
.leit-nav { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; border-radius: 10px;
            color: var(--leit-rail-text) !important; text-decoration: none; font-weight: 500; }
.leit-nav:hover { background: var(--leit-rail-hover); color: #ffffff !important; }
.leit-nav.aktiv { background: #1d3157; color: #ffffff !important; box-shadow: inset 3px 0 0 #6d97f2; }
.leit-nav .q-icon { font-size: 1.25rem; }
.leit-topbar { background: var(--leit-rail) !important; color: #ffffff; }

/* Inhalt */
.leit-content { width: 100%; max-width: 960px; padding: 2rem 2rem 4rem; gap: 1rem; }
@media (max-width: 1023px) { .leit-content { padding: 1rem 1rem 3rem; } }
.leit-sticky { position: sticky; top: 0; z-index: 10; background: var(--leit-bg); }
@media (max-width: 1023px) { .leit-sticky { top: 50px; } }

/* Lektionen und Markdown */
.glossar-link { text-decoration: underline dotted; cursor: help; }
.lesson .nicegui-markdown { line-height: 1.65; font-size: 1.02rem; max-width: 72ch; }
.lesson .nicegui-markdown p { margin: 0.6rem 0; }
.lesson .nicegui-markdown li { margin: 0.25rem 0; }
.nicegui-markdown table { border-collapse: collapse; margin: 0.75rem 0; font-size: 0.95rem; }
.nicegui-markdown th, .nicegui-markdown td { border: 1px solid var(--leit-line); padding: 0.35rem 0.65rem; }
.nicegui-markdown th { background: var(--leit-surface-2); font-weight: 600; }
.nicegui-markdown code { background: var(--leit-surface-2); border-radius: 6px; padding: 0.05rem 0.3rem; }
.nicegui-markdown pre { background: var(--leit-surface-2); border: 1px solid var(--leit-line);
                        border-radius: 10px; padding: 0.75rem 1rem; }
/* Zwischenfazit „Halten wir kurz fest“ als Merkkasten */
.nicegui-markdown blockquote {
  margin: 1rem 0; padding: 0.6rem 1rem; border-left: 4px solid var(--leit-accent);
  background: color-mix(in srgb, var(--leit-accent) 10%, transparent); border-radius: 0 10px 10px 0;
}
.nicegui-markdown blockquote p:first-child { margin-top: 0; }
.kpi-value { font-size: 1.8rem; font-weight: 600; line-height: 1.1; }

/* Ampelfarben der Themenkarte (FT-02): Fläche getönt, Rand kräftig; Symbole tragen die Bedeutung mit */
.ampel-gruen { background: #3fa7741a; border-left: 4px solid #3fa774 !important; }
.ampel-gelb { background: #d9a6401f; border-left: 4px solid #d9a640 !important; }
.ampel-rot { background: #d65c5c1a; border-left: 4px solid #d65c5c !important; }
.ampel-grau { border-left: 4px solid #7d8aa1 !important; }

/* Flächen mit Sonderfarbe – eigene Klassen statt Tailwinds dark:-Varianten */
.seiten-hintergrund { background: var(--leit-bg); }
.body--dark .seiten-hintergrund { background: var(--leit-bg); }
.hinweis-karte { background: #fdf3d7; border-color: #ecd59a !important; }
.body--dark .hinweis-karte { background: #2c2716; border-color: #5c4b1f !important; }
"""


@dataclass
class _Context:
    """Was der Rahmen aus der Anwendung braucht; wird einmal in ``ui.app.build`` gesetzt."""

    # (Prüfungsdatum, Lernbeginn) aus den Plan-Einstellungen
    exam_dates: Callable[[], tuple[dt.date, dt.date]] | None = None
    # Hell/Dunkel als gespeicherte Einstellung (gilt auf allen Seiten); Vorgabe dunkel
    get_light: Callable[[], bool] = lambda: False
    set_light: Callable[[bool], None] = lambda _value: None


_context = _Context()


def configure(
    exam_dates: Callable[[], tuple[dt.date, dt.date]],
    get_light: Callable[[], bool],
    set_light: Callable[[bool], None],
) -> None:
    """Verbindet den Rahmen mit dem Lernstand (Countdown, Hell/Dunkel)."""
    _context.exam_dates = exam_dates
    _context.get_light = get_light
    _context.set_light = set_light


def countdown(exam: dt.date, start: dt.date, today: dt.date) -> tuple[str, str, float]:
    """Zahl, Beschriftung und abgelaufener Anteil der Lernzeit (0–1) für die Seitenleiste."""
    days = (exam - today).days
    total = max((exam - start).days, 1)
    share = min(max((today - start).days / total, 0.0), 1.0)
    if days > 1:
        return str(days), "Tage bis zur AP1", share
    if days == 1:
        return "1", "Tag bis zur AP1 – morgen ist es so weit", share
    if days == 0:
        return "0", "Heute ist Prüfung. Viel Erfolg!", 1.0
    return "✓", "Die AP1 liegt hinter dir", 1.0


WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
MONTHS = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
]  # fmt: skip


def german_date(day: dt.date) -> str:
    """Datum unabhängig von der Systemsprache, z. B. „Samstag, 14. November 2026“."""
    return f"{WEEKDAYS[day.weekday()]}, {day.day}. {MONTHS[day.month - 1]} {day.year}"


def _current_path() -> str:
    """Seitenmuster der aktuellen Seite, z. B. ``/ueben/{topic_id}``; leer, wenn unbekannt."""
    try:
        return str(ui.context.client.page.path)
    except (AttributeError, RuntimeError):
        return ""


def _nav_link(item: NavItem, path: str) -> None:
    active = " aktiv" if item.matches(path) else ""
    with ui.link(target=item.target).classes(f"leit-nav{active}"):
        ui.icon(item.icon)
        ui.label(item.label)


def _countdown_block() -> None:
    if _context.exam_dates is None:
        return
    exam, start = _context.exam_dates()
    number, text, share = countdown(exam, start, dt.date.today())
    with ui.column().classes("leit-countdown gap-1 w-full"):
        ui.label(number).classes("leit-countdown-days")
        ui.label(text).classes("leit-countdown-label")
        with ui.element("div").classes("leit-countdown-track w-full"):
            ui.element("div").classes("leit-countdown-fill").style(f"width: {share * 100:.0f}%")
        ui.label(f"Prüfung am {exam:%d.%m.%Y}").classes("leit-brand-sub mt-1")


def _rail(dark: ui.dark_mode) -> None:
    """Seitenleiste: Marke, Countdown, Navigation, unten Einstellungen und Hell/Dunkel."""
    path = _current_path()
    with ui.column().classes("w-full gap-0 px-3 pt-5 pb-3 grow"):
        with ui.column().classes("gap-0 px-3 mb-4"):
            ui.label("LEIT").classes("leit-brand")
            ui.label("AP1-Lernbegleiter").classes("leit-brand-sub")
        _countdown_block()
        for group, items in NAV:
            ui.label(group).classes("leit-group")
            for item in items:
                _nav_link(item, path)
        ui.space()
        with ui.row().classes("w-full items-center gap-1 mt-4 no-wrap"):
            with ui.element("div").classes("grow"):
                _nav_link(SETTINGS, path)

            def toggle() -> None:
                dark.set_value(not dark.value)
                _context.set_light(not dark.value)

            ui.button(icon="contrast", on_click=toggle).props(
                'flat round color=grey-5 aria-label="Hell oder dunkel"'
            ).tooltip("Hell/Dunkel umschalten")


@contextmanager
def frame(title: str, subtitle: str | None = None) -> Iterator[None]:
    """Seitenrahmen mit Navigation; der ``with``-Block füllt den Inhalt."""
    ui.add_head_html(_FONT)
    ui.add_css(_CSS)
    ui.colors(**PALETTE)
    dark = ui.dark_mode(not _context.get_light())
    with ui.left_drawer(fixed=True).classes("leit-rail").props("width=264 breakpoint=1023") as drawer:
        _rail(dark)
    # Kopfzeile nur auf schmalen Bildschirmen (Quasar-Klasse lt-md = unter 1024 px)
    with ui.header().classes("leit-topbar lt-md items-center gap-2 py-1 px-2"):
        ui.button(icon="menu", on_click=drawer.toggle).props('flat round color=white aria-label="Menü"')
        ui.label("LEIT").classes("leit-brand")
    with ui.column().classes("leit-content"):
        with ui.column().classes("gap-1"):
            with ui.element("h1").classes("leit-title"):
                ui.label(title)
            if subtitle:
                ui.label(subtitle).classes("leit-meta text-sm")
        yield
