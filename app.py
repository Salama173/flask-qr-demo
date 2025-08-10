from flask import Flask, make_response, render_template_string
import qrcode, io, time

app = Flask(__name__)

# هنا بتحطي الرابط الأساسي اللي عايزة الـ QR يتولد منه
app.config['TARGET_URL'] = 'https://web.whatsapp.com/qr'

HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>QR</title>
<style>
    body {
        font-family: system-ui, Segoe UI, Roboto, Arial, sans-serif;
        text-align: center;
        margin: 40px;
    }
    h2 { color: #333; }
    .note { color: #555; margin: 10px 0; }
    img { max-width: 300px; }
</style>
</head>
<body>
<h2>🔄 QR</h2>
<div class="note">يتم تحديث الكود تلقائياً كل 30 ثانية</div>
<img id="qr" src="/qr" alt="QR Code">
<script>
function refreshQR() {
    let el = document.getElementById('qr');
    el.src = '/qr?t=' + Date.now();
}
setInterval(refreshQR, 30000);
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/qr")
def qr_endpoint():
    token = str(int(time.time()))
    target = f"{app.config['TARGET_URL']}?token={token}"
    img = qrcode.make(target)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    response = make_response(img_bytes)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
