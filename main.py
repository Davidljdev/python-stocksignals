import json
from datetime import datetime
from analysis.price_analysis import analyze_asset
from config import ASSETS, WINDOWS, THRESHOLDS

def main():
    results = []

    for asset in ASSETS:
        try:
            analysis = analyze_asset(asset)
            if analysis["signals"]:
                results.append(analysis)
        except Exception as e:
            print(f"Error analizando {asset['ticker']}: {e}")

    output = {
        "generated_at": datetime.utcnow().isoformat(),
        "results": results
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
