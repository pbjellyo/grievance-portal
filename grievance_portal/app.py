from flask import Flask, render_template, request, redirect, session, url_for
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "super-secret-key"

EMAIL_ADDRESS = "brookepmj@gmail.com"
EMAIL_PASSWORD = "bnlngjjrgkzjbwvc"

USERNAME = "you"
PASSWORD = "pink123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect("/grievance")
        else:
            return render_template("login.html", error="Wrong username or password 😢")
    return render_template("login.html")

@app.route("/grievance", methods=["GET", "POST"])
def grievance():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        grievance = request.form["grievance"]

        msg = EmailMessage()
        msg["Subject"] = f"New Grievance: {title}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = "brookepmj@gmail.com"
        msg.set_content(grievance)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            return render_template("success.html")
        except Exception as e:
            return f"Error sending email: {e}"

    return render_template("form.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
