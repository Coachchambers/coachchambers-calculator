
from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

EMAIL_ABSENDER = "growwithchambers@gmail.com"
EMAIL_PASSWORT = "yqve qvso daqy saoy"
EMAIL_EMPFÄNGER = "growwithchambers@gmail.com"

def sende_email(daten):
    msg = EmailMessage()
    msg["Subject"] = "Neue Anfrage: Kaloriendefizit-Rechner"
    msg["From"] = EMAIL_ABSENDER
    msg["To"] = EMAIL_EMPFÄNGER

    text = f"""Neue Anfrage von {daten['name']} ({daten['email']})

Geschlecht: {daten['geschlecht']}
Alter: {daten['alter']} Jahre
Größe: {daten['größe']} m
Gewicht: {daten['gewicht']} kg
Wunschgewicht: {daten['wunschgewicht']} kg

Ziel: {daten['differenz']} kg verlieren
Kaloriendefizit gesamt: {daten['gesamt_defizit']} kcal
Dauer: {daten['tage']} Tage (bei 500 kcal/Tag)

Nachricht: {daten['nachricht']}
"""

    msg.set_content(text)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ABSENDER, EMAIL_PASSWORT)
        smtp.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def formular():
    if request.method == "POST":
        try:
            größe = float(request.form["größe"].replace(",", "."))
            gewicht = float(request.form["gewicht"].replace(",", "."))
            wunschgewicht = float(request.form["wunschgewicht"].replace(",", "."))
            differenz = gewicht - wunschgewicht
            gesamt_defizit = round(differenz * 7000)
            tage = round(gesamt_defizit / 500)
            bmi = round(gewicht / (größe * größe), 1)

            daten = {
                "geschlecht": request.form["geschlecht"],
                "alter": request.form["alter"],
                "größe": größe,
                "gewicht": gewicht,
                "wunschgewicht": wunschgewicht,
                "differenz": round(differenz, 1),
                "gesamt_defizit": gesamt_defizit,
                "tage": tage,
                "bmi": bmi,
                "name": request.form["name"],
                "email": request.form["email"],
                "nachricht": request.form["nachricht"]
            }

            sende_email(daten)
            return render_template("form.html", daten=daten)

        except Exception as e:
            return f"Fehler: {e}"
    return render_template("form.html")
    
if __name__ == "__main__":
    print("Starte Flask App...")
    app.run(debug=True)
