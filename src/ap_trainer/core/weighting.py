"""Themengewichtung aus den Prüfungspunkten (LP-07, Regel aus Kap. 2 der Anforderungen).

Ergebnis ist ein Gewicht je Thema in Prozentpunkten (Summe 100 über alle geplanten Themen).
Das Gewicht steuert Reihenfolge, Übungszeit und Kürzungsvorschläge im Lernplan.
"""

from __future__ import annotations

from collections import defaultdict

from ap_trainer.content.models import Katalog, Thema


def _raw_points(katalog: Katalog) -> dict[str, float]:
    """Verteilt die Clusterpunkte auf die Themen (noch nicht normiert).

    1. Themen mit bekannten Einzelpunkten bekommen diese direkt.
    2. Der Rest des Clusters wird im Verhältnis des Lernaufwands auf die übrigen
       geplanten Themen des Clusters verteilt – ein umfangreiches Thema wie
       „Hardwareprodukte“ steht für mehr Prüfungsstoff als „Geräteklassen“. Gibt es
       keine weiteren Themen, verfällt der Rest; er stammt dann aus inzwischen
       entfallenen Themen (z. B. SQL im Cluster Datenbanken).
    """
    rule = katalog.gewichtung
    points: dict[str, float] = {}
    by_cluster: dict[str, list[Thema]] = defaultdict(list)
    for topic in katalog.themen:
        if topic.stand_2025 in ("aktiv", "neu") and topic.cluster:
            by_cluster[topic.cluster].append(topic)
    for cluster, topics in by_cluster.items():
        direct = {t.id: rule.einzelthemen_punkte[t.id] for t in topics if t.id in rule.einzelthemen_punkte}
        rest = max(rule.cluster_punkte.get(cluster, 0.0) - sum(direct.values()), 0.0)
        others = [t for t in topics if t.id not in direct]
        effort = sum(t.aufwand_h or 1.0 for t in others) or 1.0
        points.update(direct)
        points.update({t.id: rest * (t.aufwand_h or 1.0) / effort for t in others})
    return points


def compute_weights(katalog: Katalog) -> dict[str, float]:
    """Gewicht je Thema in Prozentpunkten.

    Entfallene Themen erhalten 0. Themen mit festem ``gewicht`` im Katalog (z. B.
    freiwillige Zusatzthemen) behalten es. Neue Themen erhalten mindestens das
    Mindestgewicht, damit sie trotz fehlender Prüfungshistorie geplant werden.
    """
    rule = katalog.gewichtung
    raw = _raw_points(katalog)
    total = sum(raw.values()) or 1.0
    weights: dict[str, float] = {}
    for topic in katalog.themen:
        if topic.stand_2025 == "entfallen":
            weights[topic.id] = 0.0
        elif topic.gewicht is not None:
            weights[topic.id] = topic.gewicht
        else:
            weight = raw.get(topic.id, 0.0) / total * 100
            if topic.stand_2025 == "neu":
                weight = max(weight, rule.mindestgewicht)
            weights[topic.id] = weight
    return _normalize(weights)


def _normalize(weights: dict[str, float]) -> dict[str, float]:
    """Skaliert alle Gewichte so, dass ihre Summe 100 ergibt (0 bleibt 0)."""
    total = sum(weights.values())
    if total <= 0:
        return weights
    return {key: round(value / total * 100, 3) for key, value in weights.items()}
