import json
from datetime import datetime
from analysis.price_analysis import analyze_asset
from config import ASSETS, WINDOWS, THRESHOLDS
from utils.environment import Environment
from analysis.signals import get_assets_with_signals, order_signals_for_email
from utils.email import Email

def main():
    results = []
    signal_list = []
    signal_email = []
    Environment.load_environment_variables()
    print(f'=== ANALYSIS FOR THIS ASSETS: {len(ASSETS)} ===')
    print(ASSETS)
    print('=== === ===')
    # iterate for each stock / crypto / etf
    for asset in ASSETS:
        try:
            analysis = analyze_asset(asset)
            if analysis["signals"]:
                results.append(analysis)
        except Exception as e:
            print(f"Main.py: Error validating {asset['ticker']}: {e}")
    
    if results is not None or results != []:
        signal_list = get_assets_with_signals(results)
        signal_email = order_signals_for_email(results)

    output = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "results": results,
        "total_signals" : f"{len(signal_list)} signals of {len(ASSETS)} assets"
    }

    #print(json.dumps(output, indent=2))
    print(json.dumps(output, ensure_ascii=False, indent=2))
    #print(str(signal_email))
    email = Email()
    descripcion = Email.construir_descripcion(signal_list,ASSETS)
    html = Email.construir_html_email(signal_email, descripcion)
    email.send_email(html)


if __name__ == "__main__":
    main()
