import smtplib
from email.message import EmailMessage
from utils.environment import Environment
from utils.traslator import translate_html

class Email:
    def __init__(self):
        self.user = Environment.EMAIL_USER
        self.password = Environment.EMAIL_PASSWORD
        self.destiny = Environment.EMAIL_DESTINY

    def send_email(self, body : str):
        #print("\n=== TEST EMAIL (GMAIL SMTP) ===")    

        if not self.password or not self.destiny:
            print("X EMAIL FALLÓ – Variables de entorno no cargadas")
            return
        
        if not body:
            print("No se indicó cuerpo del mensaje")
            return

        try:
            msg = EmailMessage()
            msg["Subject"] = "Market Alerts"
            msg["From"] = self.user
            msg["To"] = self.destiny
            #msg.set_content("Developed by David L")
            msg.add_alternative(body,subtype="html", charset="utf-8")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.user, self.password)
                smtp.send_message(msg)

            print("V EMAIL OK")

        except Exception as e:
            print("X EMAIL FALLÓ", e)

    @staticmethod
    def generar_bloque_html(titulo: str, mensajes: list[str]) -> str:
        items = "".join(f"<li>{m}</li>" for m in mensajes)

        return f"""
        <h2 style="margin-bottom:8px;">{titulo}</h2>
        <ul style="padding-left:18px;">
            {items}
        </ul>
        """
    
    @staticmethod
    def traducir_lista(mensajes: list[str]) -> list[str]:
        return [translate_html(m) for m in mensajes]
    
    @staticmethod
    def construir_descripcion(lista_senales : list[str], assets) -> str:
        if not lista_senales or not assets:
            return None
        
        cadena_assets = ""
        # for asset in assets:
        #     if asset["ticker"]:
        #         cadena_assets += asset.get("ticker") + ", "
        
        # iterar en la lista y solo obtener los ticker (si no hay en un elemento, devuelve nulo)
        cadena_assets = [asset["ticker"] for asset in assets if asset.get("ticker")]
        # ahora, le agregamos el ', ' intermedio
        cadena_assets = ", ".join(cadena_assets)

        if cadena_assets and len(cadena_assets) > 3:
            # slicing para eliminar los 3 ultimos caracteres
            cadena_assets = cadena_assets[:-3]

        if cadena_assets:
            cadena_assets = f"""
            Se revisan diariamente los siguientes activos de mercado: {cadena_assets} para encontrar mejores oportunidades.
            """

        descripcion_esp = f"""
        {cadena_assets}
        <br>
        De {len(assets)} acciones, ETF, y BTC; se obtuvieron {len(lista_senales)} señales de posible compra o revisión.
        """

        #print(f"lista_senales: {str(lista_senales)}")
        #print(f"assets: {str(assets)}")
        #print(f"descripcion_esp: {descripcion_esp}")

        return descripcion_esp

    @staticmethod
    def construir_html_email(mensajes_es: list[str], descripcion_esp: str) -> str:

        bloque_descripcion = ""
        if descripcion_esp:
            descripcion_eng = translate_html(descripcion_esp)
            bloque_descripcion = f"""
            <tr>
                <td style="padding:20px 0; font-size:14px; line-height:1.6;">
                    <p style="margin:0 0 8px 0;"><strong>ENG:</strong> {descripcion_eng}</p>
                    <hr>
                    <p style="margin:0;"><strong>ESP:</strong> {descripcion_esp}</p>
                </td>
            </tr>
            """

        mensajes_en = Email.traducir_lista(mensajes_es)

        bloque_es = Email.generar_bloque_html(
            "📊 Señales de mercado (Español)",
            mensajes_es
        )

        bloque_en = Email.generar_bloque_html(
            "📊 Market Signals (English)",
            mensajes_en
        )

        return f"""
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="
            margin:0;
            padding:0;
            background-color:#f4f6f8;
            font-family:'Poppins','Segoe UI',Roboto,Arial,sans-serif;
        ">

            <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td align="center">

                        <table width="900" cellpadding="0" cellspacing="0" style="
                            background-color:#ffffff;
                            border-radius:8px;
                            padding:32px;
                        ">

                            <!-- HEADER -->
                            <tr>
                                <td style="text-align:center; padding-bottom:16px;">
                                    <h1 style="margin:0; font-size:22px;">
                                        📈 Market Asset Scanner
                                    </h1>
                                    <p style="margin:6px 0 0; font-size:12px; color:#666;">
                                        Developed by @dajanluvid
                                    </p>
                                </td>
                            </tr>

                            <!-- DESCRIPTION -->
                            {bloque_descripcion}

                            <!-- DIVIDER -->
                            <tr>
                                <td style="padding:12px 0;">
                                    <hr style="border:none; border-top:1px solid #ddd;">
                                </td>
                            </tr>

                            <!-- ENGLISH BLOCK -->
                            <tr>
                                <td>
                                    {bloque_en}
                                </td>
                            </tr>

                            <!-- DIVIDER -->
                            <tr>
                                <td style="padding:12px 0;">
                                    <hr style="border:none; border-top:1px solid #ddd;">
                                </td>
                            </tr>

                            <!-- SPANISH BLOCK -->
                            <tr>
                                <td>
                                    {bloque_es}
                                </td>
                            </tr>

                            <!-- FOOTER -->
                            <tr>
                                <td style="
                                    padding-top:20px;
                                    font-size:11px;
                                    color:#888;
                                    text-align:center;
                                ">
                                    Automated alert · No manual action required
                                </td>
                            </tr>

                        </table>

                    </td>
                </tr>
            </table>

        </body>
        </html>
        """
