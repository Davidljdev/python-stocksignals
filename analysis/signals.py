from config import THRESHOLDS
import re

# valores para calibrar la generacion de señales.
LONG_TERM_MIN_GROWTH_24M = 20.0
MIN_PULLBACK_PERCENT = 5.0
OPPORTUNITY_PULLBACK_PERCENT = 10.0
STRONG_PULLBACK_PERCENT = 20.0


def detect_signals(changes: dict) -> list:
    """
    Analiza cambios porcentuales y genera señales según umbrales definidos.
    No depende del DataFrame, solo del dict 'changes'.
    Changes puede valer, por ejemplo:
        changes = {
            "3m": -12.5,
            "6m": -18.2,
            "12m": -35.7
        }
    """
    signals = []

    # Si no hay datos, no se puede analizar
    if not changes:
        return signals

    # *** CAIDAS ***
    # Caída estructural (36 meses)
    if changes.get("36m") is not None and changes["36m"] <= THRESHOLDS["drop_struct"]:
        signals.append({
            "code": "PRICE_DROP_STRUCTURAL",
            "severity": "high",
            "message": f"Caida de {changes['36m']}% en 36 meses."
        })

    # Caída estructural (24 meses)
    if changes.get("24m") is not None and changes["24m"] <= THRESHOLDS["drop_cycle"]:
        signals.append({
            "code": "PRICE_DROP_CYCLE",
            "severity": "high",
            "message": f"Caida de {changes['24m']}% en 24 meses."
        })

    # Regla: caída fuerte en el largo plazo (12 meses)
    # si el valor de "12" (-35.7) no es nulo y es menor o igual que THRESHOLDS["drop_long"] (-30)
    if changes.get("12m") is not None and changes["12m"] <= THRESHOLDS["drop_long"]:
        signals.append({
            "code": "PRICE_DROP_LONG_TERM",
            "severity": "high",
            "message": f"Caida de {changes['12m']}% en 12 meses."
        })

    # Regla: caída en el mediano plazo (6 meses)
    if changes.get("6m") is not None and changes["6m"] <= THRESHOLDS["drop_mid"]:
        signals.append({
            "code": "PRICE_DROP_MID_TERM",
            "severity": "medium",
            "message": f"Caida de {changes['6m']}% en 6 meses."
        })

    # Regla: caída reciente en el corto plazo (3 meses)
    if changes.get("3m") is not None and changes["3m"] <= THRESHOLDS["drop_short"]:
        signals.append({
            "code": "PRICE_DROP_SHORT_TERM",
            "severity": "low",
            "message": f"Caida de {changes['3m']}% en 3 meses."
        })

    # *** SUBIDAS ***
    # Subida estructural (36 meses)
    if changes.get("36m") is not None and changes["36m"] >= THRESHOLDS["surge_struct"]:
        signals.append({
            "code": "PRICE_SURGE_STRUCTURAL",
            "severity": "high",
            "message": f"Subida de {changes['36m']}% en 36 meses."
        })

    # Ciclo completo (24 meses)
    if changes.get("24m") is not None and changes["24m"] >= THRESHOLDS["surge_cycle"]:
        signals.append({
            "code": "PRICE_SURGE_CYCLE",
            "severity": "medium",
            "message": f"Subida de {changes['24m']}% en 24 meses."
        })

    # Regla: subida fuerte en el largo plazo (12 meses)
    if changes.get("12m") is not None and changes["12m"] >= THRESHOLDS["surge_long"]:
        signals.append({
            "code": "PRICE_SURGE_LONG_TERM",
            "severity": "high",
            "message": f"Subida de {changes['12m']}% en 12 meses."
        })

    # Subida fuerte en 6 meses
    if changes.get("6m") is not None and changes["6m"] >= THRESHOLDS["surge_mid"]:
        signals.append({
            "code": "PRICE_SURGE_MID_TERM",
            "severity": "medium",
            "message": f"Subida de {changes['6m']}% en 6 meses."
        })

    # Subida fuerte en 3 meses
    if changes.get("3m") is not None and changes["3m"] >= THRESHOLDS["surge_short"]:
        signals.append({
            "code": "PRICE_SURGE_SHORT_TERM",
            "severity": "low",
            "message": f"Subida de {changes['3m']}% en 3 meses."
        })

    return signals



def detect_signals2(prices: dict, changes: dict) -> list:
    signals = []

    if not prices or not changes:
        return signals

    now = prices.get("Now")
    if now is None:
        return signals

    # 1. Validar tendencia alcista de fondo usando 24m
    change_24m = changes.get("24m")
    if change_24m is None or change_24m < LONG_TERM_MIN_GROWTH_24M:
        return signals

    # 2. Construir histórico completo disponible
    historical_prices = {
        "3 meses": prices.get("3m"),
        "6 meses": prices.get("6m"),
        "12 meses": prices.get("12m"),
        "24 meses": prices.get("24m"),
        "36 meses": prices.get("36m"),
    }

    historical_prices = {
        k: v for k, v in historical_prices.items() if v is not None
    }

    if not historical_prices:
        return signals

    # 3. Detectar máximo histórico dentro de los datos disponibles
    peak_period, peak_price = max(
        historical_prices.items(), key=lambda x: x[1]
    )

    # 4. Calcular caída desde el máximo
    pullback_percent = ((now - peak_price) / peak_price) * 100

    # Si no ha caído, no hay señal
    if pullback_percent >= 0:
        return signals

    pullback_abs = abs(pullback_percent)

    # 5. Señales según magnitud de la corrección

    if pullback_abs >= MIN_PULLBACK_PERCENT:
        signals.append({
            "code": "ZONA_VIGILANCIA_CORRECCION",
            "priority": 1,
            "message": (
                f"La acción mantiene tendencia alcista de largo plazo, "
                f"pero ha caído {pullback_abs:.2f}% desde su máximo de "
                f"{peak_price:.2f} (hace {peak_period}). "
                f"Precio actual: {now:.2f}."
            )
        })

    if pullback_abs >= OPPORTUNITY_PULLBACK_PERCENT:
        signals.append({
            "code": "OPORTUNIDAD_CORRECCION",
            "priority": 2,
            "message": (
                f"Corrección relevante detectada. "
                f"Desde su máximo de {peak_price:.2f} (hace {peak_period}) "
                f"la acción ha bajado {pullback_abs:.2f}%. "
                f"Precio actual: {now:.2f}."
            )
        })

    if pullback_abs >= STRONG_PULLBACK_PERCENT:
        signals.append({
            "code": "ALERTA_CORRECCION_FUERTE",
            "priority": 3,
            "message": (
                f"Corrección fuerte en acción de calidad. "
                f"Ha caído {pullback_abs:.2f}% desde su máximo de "
                f"{peak_price:.2f} (hace {peak_period}). "
                f"Precio actual: {now:.2f}."
            )
        })

    return signals


def get_assets_with_signals(results: list) -> list:
    """
    Devuelve la lista de señales que se generaron
    
    :param results: lista del JSON global con todas las señales y assets.
    """
    assets = []

    for item in results:
        signals = item.get("signals", [])
        if signals:
            assets.append(item.get("asset"))

    return assets

def order_signals_for_email(results: list) -> list:
    """
    Ordenar las señales para mandarlas por correo
    
    :param results: JSON general con todos los analisis.
    """
    collected = []

    for item in results:
        asset = item.get("asset")
        signals = item.get("signals", [])

        for signal in signals:
            message = signal.get("message", "")
            priority = signal.get("priority", 0)

            # extraer porcentaje de caída desde el texto
            match = re.search(r"(\d+\.\d+)%", message)
            pullback = float(match.group(1)) if match else 0.0

            collected.append({
                "asset": asset,
                "priority": priority,
                "pullback": pullback,
                "message": f"{asset}: {message}"
            })

    # ordenar:
    # 1. prioridad descendente
    # 2. mayor caída primero
    collected.sort(
        key=lambda x: (x["priority"], x["pullback"]),
        reverse=True
    )

    # devolver solo los strings
    return [item["message"] for item in collected]