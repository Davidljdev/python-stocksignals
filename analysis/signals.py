from config import THRESHOLDS

def detect_signals(changes: dict) -> list:
    """
    Aplica reglas simples para detectar señales relevantes.
    """
    signals = []

    if changes["12m"] <= THRESHOLDS["drop_long"]:
        signals.append({
            "code": "PRICE_DROP_LONG_TERM",
            "severity": "medium",
            "message": f"Caída de {changes['12m']}% en 12 meses."
        })

    if changes["6m"] <= THRESHOLDS["drop_mid"]:
        signals.append({
            "code": "PRICE_DROP_MID_TERM",
            "severity": "low",
            "message": f"Caída de {changes['6m']}% en 6 meses."
        })

    if changes["3m"] <= THRESHOLDS["drop_short"]:
        signals.append({
            "code": "PRICE_DROP_SHORT_TERM",
            "severity": "low",
            "message": f"Caída reciente de {changes['3m']}% en 3 meses."
        })

    if changes["12m"] >= THRESHOLDS["surge_long"]:
        signals.append({
            "code": "PRICE_SURGE_LONG_TERM",
            "severity": "medium",
            "message": f"Subida de {changes['12m']}% en 12 meses."
        })

    return signals
