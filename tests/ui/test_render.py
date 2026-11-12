"""Tests für die Zerlegung von Lektionstext (ohne Browser)."""

from __future__ import annotations

import pytest

from ap_trainer.ui.render import link_glossary, parse_blocks

TEXT = """Einleitung.

```mermaid
flowchart LR
  A --> B
```

<details>
<summary>Warum?</summary>

Weil A.

<details>
<summary>Und warum das?</summary>

Weil B.
</details>
</details>

Schluss."""


def test_blocks_with_nested_details_and_mermaid() -> None:
    blocks = parse_blocks(TEXT)
    assert [b.kind for b in blocks] == ["markdown", "mermaid", "details", "markdown"]
    assert blocks[1].text.startswith("flowchart LR")
    outer = blocks[2]
    assert outer.summary == "Warum?"
    assert [c.kind for c in outer.children] == ["markdown", "details"]
    assert outer.children[1].children[0].text == "Weil B."
    assert blocks[3].text == "Schluss."


def test_unclosed_details_raises() -> None:
    with pytest.raises(ValueError):
        parse_blocks("<details><summary>x</summary> offen")


def test_glossary_links_get_tooltip_and_escape() -> None:
    text = "Das [Bit](glossar:bit) und [X](glossar:fehlt)."
    result = link_glossary(text, {"bit": 'Kleinste "Einheit"'}.get)
    assert '<a href="/glossar?begriff=bit" title="Kleinste &quot;Einheit&quot;"' in result
    assert 'href="/glossar?begriff=fehlt" title=""' in result
