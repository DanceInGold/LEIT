"""Üben: Aufgaben lösen mit gestuften Hilfen und Feedback je Teilantwort.

Übersicht ``/ueben`` mit allen Themen, zu denen es Aufgaben gibt, und ihrer aktuellen Stufe;
``/ueben/<thema>`` zeigt eine Aufgabe nach der anderen (AU-01 bis AU-06, HI-01 bis HI-03).
Mit ``?aufgabe=<id>`` lässt sich eine bestimmte Aufgabe öffnen (z. B. aus dem Fehlerprotokoll).
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field

from nicegui import ui

from ap_trainer.content.aufgaben import (
    STUFEN_NAMEN,
    TYP_NAMEN,
    Aufgabe,
    Freitext,
    Lueckentext,
    MultipleChoice,
    Rechnung,
    Reihenfolge,
    Zuordnung,
)
from ap_trainer.service import PracticeTopic, Submission, Trainer
from ap_trainer.tasks.check import Antwort, FreitextAntwort, missing_terms
from ap_trainer.tasks.hints import help_steps
from ap_trainer.ui.layout import frame
from ap_trainer.ui.lesson import MARKDOWN_EXTRAS, STATUS_COLORS
from ap_trainer.ui.render import Block, parse_blocks
from ap_trainer.ui.task_view import (
    PLATZHALTER,
    gap_markdown,
    initial_order,
    is_blank,
    percent,
    shuffled_indices,
)

type AnswerGetter = Callable[[], Antwort]


@dataclass
class ExerciseState:
    """Zustand der Übung im Browser: aktuelle Aufgabe, geöffnete Hilfen, Ergebnis."""

    task: Aufgabe | None
    opened: int = 0
    started: float = field(default_factory=time.monotonic)
    submission: Submission | None = None
    order: list[int] = field(default_factory=list)
    # Freitext: Musterlösung erst nach dem Schreiben zeigen, dann selbst bewerten (AU-05)
    freitext: str | None = None
    solved: int = 0


def _markdown(text: str) -> None:
    """Markdown mit Mermaid-Diagrammen und Vertiefungen, wie in der Lektionsansicht."""
    _render(parse_blocks(text))


def _render(blocks: list[Block]) -> None:
    for block in blocks:
        if block.kind == "mermaid":
            ui.mermaid(block.text).classes("w-full")
        elif block.kind == "details":
            with ui.expansion(block.summary, icon="psychology_alt").classes("w-full border rounded"):
                _render(block.children)
        else:
            ui.markdown(block.text, extras=MARKDOWN_EXTRAS).classes("w-full")


# --- Eingaben je Aufgabentyp ------------------------------------------------------
def _inputs_choice(task: MultipleChoice) -> AnswerGetter:
    order = shuffled_indices(task, len(task.optionen))
    if task.anzahl_richtig == 1:
        radio = ui.radio({i: task.optionen[i].text for i in order}, value=None)
        return lambda: frozenset() if radio.value is None else frozenset({int(radio.value)})
    ui.label(f"Kreuze {task.anzahl_richtig} Antworten an.").classes("text-sm opacity-70")
    boxes = {i: ui.checkbox(task.optionen[i].text) for i in order}
    return lambda: frozenset(i for i, box in boxes.items() if box.value)


def _inputs_assignment(task: Zuordnung) -> AnswerGetter:
    selects = []
    for index in shuffled_indices(task, len(task.paare)):
        with ui.row().classes("w-full items-center gap-3 flex-nowrap"):
            ui.label(task.paare[index].links).classes("w-1/3 font-medium")
            selects.append((index, ui.select(task.auswahl, label="gehört zu …").classes("grow")))
    return lambda: [dict((i, s.value) for i, s in selects).get(i) for i in range(len(task.paare))]


def _inputs_gaps(task: Lueckentext) -> AnswerGetter:
    _markdown(gap_markdown(task.text))
    fields = [ui.input(f"Lücke {i + 1}").classes("w-full") for i in range(len(task.luecken))]
    return lambda: [f.value for f in fields]


def _inputs_order(task: Reihenfolge, state: ExerciseState) -> AnswerGetter:
    if not state.order:
        state.order = initial_order(task, len(task.elemente))

    def move(position: int, delta: int) -> None:
        target = position + delta
        if 0 <= target < len(state.order):
            state.order[position], state.order[target] = state.order[target], state.order[position]
            items.refresh()

    @ui.refreshable
    def items() -> None:
        for position, element_index in enumerate(state.order):
            with ui.row().classes("w-full items-center gap-2 flex-nowrap border rounded p-1"):
                ui.label(f"{position + 1}.").classes("w-6 text-right opacity-60")
                ui.label(task.elemente[element_index]).classes("grow")
                ui.button(icon="arrow_upward", on_click=lambda p=position: move(p, -1)).props(
                    "flat dense round"
                )
                ui.button(icon="arrow_downward", on_click=lambda p=position: move(p, 1)).props(
                    "flat dense round"
                )

    ui.label("Mit den Pfeilen sortieren – oben steht der erste Schritt.").classes("text-sm opacity-70")
    items()
    return lambda: list(state.order)


def _inputs_calculation(task: Rechnung, submit: Callable[[], None]) -> AnswerGetter:
    fields = []
    for number, step in enumerate(task.schritte, start=1):
        field_ = ui.input(f"{number}. {step.frage}", placeholder=PLATZHALTER[step.format]).classes("w-full")
        if step.einheit:
            field_.props(f'suffix="{step.einheit}"')
        field_.on("keydown.enter", submit)
        fields.append(field_)
    return lambda: [f.value for f in fields]


def _inputs_free_text(task: Freitext, state: ExerciseState) -> AnswerGetter:
    if task.operator:
        ui.label(f"Operator: {task.operator}").classes("text-sm opacity-70")
    if state.freitext is None:
        area = ui.textarea("Deine Antwort").classes("w-full").props("autogrow")
        return lambda: FreitextAntwort(area.value or "", [])
    # Zweiter Schritt: Musterlösung zeigen und selbst abhaken (AU-05)
    with ui.card().classes("w-full bg-gray-500/10"):
        ui.label("Deine Antwort").classes("text-xs uppercase opacity-60")
        ui.label(state.freitext or "–").classes("whitespace-pre-wrap")
    text = state.freitext
    with ui.card().classes("w-full"):
        ui.label("Musterlösung").classes("text-xs uppercase opacity-60")
        _markdown(task.musterloesung)
    missing = {point for point, _ in missing_terms(task, text)}
    ui.label("Hake ehrlich ab, was in deiner Antwort steckt:").classes("font-medium")
    boxes = []
    for point in task.bewertungspunkte:
        suffix = f" ({point.punkte} P.)" if point.punkte > 1 else ""
        boxes.append(ui.checkbox(point.punkt + suffix))
        if point.punkt in missing:
            terms = ", ".join(point.kernbegriffe)
            ui.label(f"Kein Kernbegriff gefunden ({terms}).").classes("text-xs text-orange-700 ml-8 -mt-2")
    return lambda: FreitextAntwort(text, [box.value for box in boxes])


def render_inputs(task: Aufgabe, state: ExerciseState, submit: Callable[[], None]) -> AnswerGetter:
    """Zeichnet die Eingabefelder passend zum Aufgabentyp und liefert, wie die Antwort gelesen wird."""
    if isinstance(task, MultipleChoice):
        return _inputs_choice(task)
    if isinstance(task, Zuordnung):
        return _inputs_assignment(task)
    if isinstance(task, Lueckentext):
        return _inputs_gaps(task)
    if isinstance(task, Reihenfolge):
        return _inputs_order(task, state)
    if isinstance(task, Rechnung):
        return _inputs_calculation(task, submit)
    return _inputs_free_text(task, state)


# --- Anzeige ----------------------------------------------------------------------
def _task_header(task: Aufgabe, topic_title: str) -> None:
    with ui.row().classes("items-center gap-2 flex-wrap text-sm"):
        ui.label(topic_title).classes("opacity-70")
        ui.badge(f"Stufe {task.stufe} · {STUFEN_NAMEN[task.stufe]}")
        ui.badge(TYP_NAMEN[task.typ]).props("outline")
        ui.badge(task.status, color=STATUS_COLORS[task.status]).tooltip("Prüfstatus (LI-06)")


def _hints(task: Aufgabe, state: ExerciseState, refresh: Callable[[], None]) -> None:
    steps = help_steps(task)
    for step in steps[: state.opened]:
        with ui.card().classes("w-full bg-blue-500/10 gap-1"):
            ui.label(step.titel).classes("text-xs uppercase tracking-wide opacity-70")
            _markdown(step.text)
    if state.submission is None and state.opened < len(steps):

        def open_next() -> None:
            state.opened += 1
            refresh()

        upcoming = steps[state.opened].titel
        ui.button(f"Hilfe: {upcoming}", icon="lightbulb", on_click=open_next).props("flat")


def _feedback(task: Aufgabe, submission: Submission) -> None:
    result = submission.ergebnis
    color = "positive" if result.richtig else "negative"
    with ui.card().classes("w-full gap-2"):
        with ui.row().classes("items-center gap-2"):
            ui.icon("check_circle" if result.richtig else "error", color=color, size="md")
            title = "Richtig!" if result.richtig else "Noch nicht ganz."
            ui.label(f"{title} {percent(result.anteil)} der Punkte").classes("text-lg font-medium")
        if result.fehlerschritt is not None:
            ui.label(f"Der erste Fehler steckt in Schritt {result.fehlerschritt + 1}.").classes("font-medium")
        for item in result.rueckmeldungen:
            with ui.row().classes("w-full items-start gap-2 flex-nowrap"):
                ui.icon(
                    "check" if item.richtig else "close", color="positive" if item.richtig else "negative"
                )
                with ui.column().classes("gap-0 grow"):
                    ui.label(item.teil).classes("font-medium")
                    ui.label(item.text).classes("text-sm")
        if submission.stufe_nachher > submission.stufe_vorher:
            ui.label(f"Stufe {submission.stufe_nachher} erreicht – weiter so!").classes("text-positive")
        elif submission.stufe_nachher < submission.stufe_vorher:
            ui.label(f"Zurück auf Stufe {submission.stufe_nachher}, um die Grundlagen zu festigen.")
    with ui.expansion("Lösungsweg", icon="route", value=not result.richtig).classes("w-full border rounded"):
        _markdown(task.loesungsweg)


def _topic_card(item: PracticeTopic) -> None:
    quote = f"{item.richtig}/{item.versuche} richtig" if item.versuche else "noch nicht geübt"
    with (
        ui.card()
        .classes("w-full cursor-pointer hover:shadow-md")
        .on("click", lambda: ui.navigate.to(f"/ueben/{item.thema.id}")),
        ui.row().classes("items-center gap-3 w-full flex-nowrap"),
    ):
        with ui.column().classes("grow gap-0"):
            ui.label(item.thema.titel).classes("font-medium")
            ui.label(quote).classes("text-sm opacity-70")
        ui.badge(f"Stufe {item.stufe} · {STUFEN_NAMEN[item.stufe]}")
        ui.icon("chevron_right")


def register(trainer: Trainer) -> None:
    """Registriert Übersicht und Übungsseite."""

    @ui.page("/ueben")
    def overview_page() -> None:
        topics = trainer.practice_topics()
        with frame("Üben"):
            ui.label(
                "Die Stufe steigt nach drei sicher gelösten Aufgaben in Folge und sinkt nach zwei Fehlern. "
                "Mit mehr als dem ersten Hinweis gelöst zählt nicht als sicher."
            ).classes("text-sm opacity-80")
            if not topics:
                ui.label("Noch keine Aufgaben vorhanden.")
            for item in topics:
                _topic_card(item)

    @ui.page("/ueben/{topic_id}")
    def exercise_page(topic_id: str, aufgabe: str | None = None) -> None:
        topic = trainer.package.katalog.by_id().get(topic_id)
        if topic is None:
            with frame("Thema nicht gefunden"):
                ui.link("Zur Übersicht", "/ueben")
            return
        first = trainer.find_task(aufgabe, topic_id) if aufgabe else None
        state = ExerciseState(task=first or trainer.next_task(topic_id))
        getter: list[AnswerGetter] = []

        def submit() -> None:
            task = state.task
            if task is None or state.submission is not None:
                return
            answer = getter[0]()
            if is_blank(task, answer):
                ui.notify("Erst eine Antwort eingeben – oder eine Hilfe öffnen.", type="warning")
                return
            if isinstance(task, Freitext) and state.freitext is None:
                assert isinstance(answer, FreitextAntwort)
                state.freitext = answer.text
                body.refresh()
                return
            seconds = time.monotonic() - state.started
            state.submission = trainer.submit(task, answer, state.opened, seconds)
            state.solved += 1
            # Nur Hilfen und Ergebnis neu zeichnen – die Eingaben bleiben sichtbar
            hints.refresh()
            result.refresh()

        def next_task() -> None:
            state.task = trainer.next_task(topic_id)
            state.opened, state.submission, state.order, state.freitext = 0, None, [], None
            state.started = time.monotonic()
            body.refresh()

        @ui.refreshable
        def hints() -> None:
            if state.task is not None:
                _hints(state.task, state, hints.refresh)

        @ui.refreshable
        def result() -> None:
            task = state.task
            if task is None:
                return
            if state.submission is None:
                label = "Prüfen"
                if isinstance(task, Freitext):
                    label = "Musterlösung zeigen" if state.freitext is None else "Bewertung speichern"
                ui.button(label, icon="fact_check", on_click=submit).classes("w-full")
                return
            _feedback(task, state.submission)
            ui.button("Nächste Aufgabe", icon="arrow_forward", on_click=next_task).classes("w-full")

        @ui.refreshable
        def body() -> None:
            task = state.task
            if task is None:
                ui.label("Zu diesem Thema gibt es noch keine Aufgaben.")
                ui.link("Zur Übersicht", "/ueben")
                return
            _task_header(task, topic.titel)
            with ui.card().classes("w-full gap-2"):
                ui.label(task.titel).classes("text-xl font-semibold")
                if task.situation:
                    with ui.card().classes("w-full bg-gray-500/10"):
                        _markdown(task.situation)
                _markdown(task.frage)
                getter[:] = [render_inputs(task, state, submit)]
            hints()
            result()

        with frame(f"Üben: {topic.titel}"):
            with ui.row().classes("items-center gap-2 text-sm"):
                ui.link("← Alle Themen", "/ueben")
                ui.link("Kapitel zum Thema", f"/thema/{topic_id}")
            body()
