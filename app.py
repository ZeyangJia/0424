from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        session["logged_in"] = True
        return jsonify({"success": True})

    return jsonify({"success": False, "message": "用户名或密码错误"}), 401


@app.route("/admin")
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    return render_template("admin.html")


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.pop("logged_in", None)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
