from flask import Flask, request, send_file, render_template_string
import io
import re

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>Koha Barcode Fixer</title>
<h2>Upload Scanner TXT File</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=file required>
  <input type=submit value="Validate & Fix">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        content = file.read().decode('utf-8').splitlines()
        
        pattern = re.compile(r'^\d{6}$')
        output = []

        for line in content:
            barcode = line.strip()
            if pattern.match(barcode):
                output.append("BK" + barcode)

        output_data = "\n".join(output)
        return send_file(
            io.BytesIO(output_data.encode()),
            as_attachment=True,
            download_name="koha_ready.txt",
            mimetype="text/plain"
        )

    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)