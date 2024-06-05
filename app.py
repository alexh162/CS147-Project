from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_bulb_states():
    conn = sqlite3.connect('bulb_state.db')
    c = conn.cursor()
    c.execute('SELECT state, brightness, color_temp, timestamp FROM bulb_state ORDER BY timestamp DESC')
    states = c.fetchall()
    conn.close()
    return states

def get_settings():
    conn = sqlite3.connect('bulb_state.db')
    c = conn.cursor()
    c.execute('SELECT brightness, color_temp FROM settings ORDER BY id DESC LIMIT 1')
    settings = c.fetchone()
    conn.close()
    return settings if settings else (None, None)

@app.route('/')
def index():
    states = get_bulb_states()
    return render_template('index.html', states=states)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        brightness = request.form['brightness']
        color_temp = request.form['color_temp']
        conn = sqlite3.connect('bulb_state.db')
        c = conn.cursor()
        c.execute('INSERT INTO settings (brightness, color_temp) VALUES (?, ?)', (brightness, color_temp))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('settings.html')

if __name__ == "__main__":
    app.run(debug=True)
