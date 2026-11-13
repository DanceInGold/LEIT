"""Tests für das Lesen und Vergleichen von Eingaben."""

from __future__ import annotations

import pytest

from ap_trainer.tasks.answers import (
    is_valid,
    normalize_text,
    number_candidates,
    parse_dual,
    parse_hex,
    parse_ipv4,
    same_answer,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("62", [62.0]),
        ("62 Hosts", [62.0]),
        ("4,5 s", [4.5]),
        ("4.5", [4.5]),
        ("1.500", [1.5, 1500.0]),
        ("1.234,56 €", [1234.56]),
        ("1,234.56", [1234.56]),
        ("−3", [-3.0]),
        ("1 500", [1500.0]),
        ("abc", []),
    ],
)
def test_number_candidates(raw: str, expected: list[float]) -> None:
    assert number_candidates(raw) == expected


def test_number_comparison_with_tolerance() -> None:
    assert same_answer("zahl", "1.500", "1500")
    assert same_answer("zahl", "1500,0", "1500")
    assert not same_answer("zahl", "1501", "1500")
    assert same_answer("zahl", "33,3", "33.33", tolerance=0.01)
    assert not same_answer("zahl", "", "0")


def test_dual_hex_ipv4() -> None:
    assert parse_dual("1011 0111") == 183
    assert parse_dual("0b10110111") == 183
    assert parse_dual("1012") is None
    assert parse_hex("0xB7") == 183
    assert parse_hex("b7h") == 183
    assert parse_hex("G1") is None
    assert parse_ipv4("192.168.0.1") == (192 << 24) | (168 << 16) | 1
    assert parse_ipv4("256.0.0.1") is None
    assert parse_ipv4("10.0.0") is None
    assert same_answer("dual", "10110111", "1011 0111")
    assert same_answer("ipv4", " 10.0.0.1 ", "10.0.0.1")


def test_text_and_validity() -> None:
    assert normalize_text("  Vier   Bit. ") == "vier bit"
    assert same_answer("text", "TCP", "tcp")
    assert is_valid("hex", "FF")
    assert not is_valid("ipv4", "1.2.3")
    assert not is_valid("zahl", "keine")
