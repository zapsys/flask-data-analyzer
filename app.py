import os, json, sqlite3, datetime
import pandas as pd
import fitz  # PyMuPDF
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key'
UPLOAD_FOLDER = 'uploads'
DB_PATH = 'data.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                upload_date TEXT NOT NULL,
                columns TEXT NOT NULL,
                data TEXT NOT NULL,
                row_count INTEGER
            )
        ''')
init_db()

def extract_pdf_fast(filepath):
    all_rows = []
    try:
        doc = fitz.open(filepath)
        for page in doc:
            tables = page.find_tables()
            for table in tables:
                data = table.extract()
                cleaned = [[str(cell).replace('\n', ' ').strip() if cell else "" for cell in row] for row in data]
                all_rows.extend(cleaned)
    except Exception as e:
        print(f"Erro PDF: {e}")
    return all_rows

def clean_data(raw_rows):
    if not raw_rows: return None
    common_len = Counter([len(r) for r in raw_rows]).most_common(1)[0][0]
    valid_rows = [r for r in raw_rows if len(r) == common_len]
    df = pd.DataFrame(valid_rows)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df = df[~df.astype(str).eq(df.columns.astype(str)).all(axis=1)] # Remove headers repetidos
    df.columns = [str(c).strip() for c in df.columns]
    return df.fillna("")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            
            ext = filename.rsplit('.', 1)[1].lower()
            df = None
            if ext == 'pdf': df = clean_data(extract_pdf_fast(path))
            elif ext in ['xls', 'xlsx']: df = pd.read_excel(path).fillna("")
            elif ext == 'csv': df = pd.read_csv(path).fillna("")
            
            if df is not None:
                with get_db() as conn:
                    conn.execute('INSERT INTO files (filename, upload_date, columns, data, row_count) VALUES (?,?,?,?,?)',
                        (filename, datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), 
                         json.dumps(df.columns.tolist()), df.to_json(orient='records'), len(df)))
                flash(f"Sucesso! {len(df)} linhas importadas.")
    
    with get_db() as conn:
        files = conn.execute('SELECT * FROM files ORDER BY id DESC').fetchall()
    return render_template('index.html', files=files)

@app.route('/view/<int:file_id>')
def view_file(file_id):
    with get_db() as conn:
        f = conn.execute('SELECT id, filename, columns, row_count FROM files WHERE id=?', (file_id,)).fetchone()
    return render_template('view.html', file=f, columns=json.loads(f['columns']))

@app.route('/api/data/<int:file_id>')
def get_data(file_id):
    with get_db() as conn:
        return conn.execute('SELECT data FROM files WHERE id=?', (file_id,)).fetchone()['data']

@app.route('/delete/<int:file_id>')
def delete_file(file_id):
    with get_db() as conn:
        conn.execute('DELETE FROM files WHERE id=?', (file_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
