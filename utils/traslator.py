from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup, NavigableString

def translate_html(
    html_text: str,
    source_lang: str = "es",
    target_lang: str = "en"
) -> str:
    """
    Traduce solo el texto visible de un string HTML,
    preservando completamente las etiquetas.
    """

    soup = BeautifulSoup(html_text, "html.parser")
    translator = GoogleTranslator(source=source_lang, target=target_lang)

    for element in soup.descendants:
        if isinstance(element, NavigableString):
            text = str(element).strip()
            if text:
                try:
                    translated = translator.translate(text)
                    element.replace_with(translated)
                except Exception:
                    # si falla la traducción, dejamos el texto original
                    pass

    return str(soup)
