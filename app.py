from flask import Flask, render_template, request, jsonify, url_for
import psycopg
import os

app = Flask(__name__)

# 🔥 PostgreSQL Connection (Render)
conn = psycopg.connect(
    host=os.environ.get("DB_HOST"),
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    port=os.environ.get("DB_PORT", 5432),
    sslmode="require"
)

cursor = conn.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/form/<int:token>")
def form(token):
    return render_template("form.html", token=token)

@app.route("/check_unique", methods=["POST"])
def check_unique():
    data = request.get_json()
    field = data.get("field")
    value = data.get("value")

    allowed_fields = ["user_id", "email", "phone"]

    if field not in allowed_fields:
        return jsonify({"exists": False})

    query = f"SELECT 1 FROM users WHERE {field} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()

    return jsonify({"exists": bool(result)})

@app.route("/submit/<int:token>", methods=["POST"])
def submit(token):
    user_id = request.form["user_id"]
    email = request.form["email"]
    phone = request.form["phone"]

    sql = "INSERT INTO users (user_id, email, phone, token) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (user_id, email, phone, token))
    conn.commit()

    image_name = f"img{token}.png"

    content_map = {
        1: "DIGITAL FORENSICS",
        2: "BLOCKCHAIN TECHNOLOGY",
        3: "GREEN COMPUTING",
        4: "DIGITAL FORENSICS",
        5: "BLOCKCHAIN TECHNOLOGY",
        6: "GREEN COMPUTING",
        7: "DIGITAL FORENSICS",
        8: "BLOCKCHAIN TECHNOLOGY",
        9: "GREEN COMPUTING",
        10: "DIGITAL FORENSICS",
        11: "BLOCKCHAIN TECHNOLOGY",
        12: "GREEN COMPUTING",
        13: "DIGITAL FORENSICS",
        14: "BLOCKCHAIN TECHNOLOGY",
        15: "GREEN COMPUTING",
    }

    content = content_map.get(token, "GENERAL TOPIC")

    return render_template(
        "result.html",
        user_id=user_id,
        email=email,
        phone=phone,
        image=url_for('static', filename=f"images/{image_name}"),
        content=content
    )

if __name__ == "__main__":
    app.run()
