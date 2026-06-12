"""
[Aplicación básica del microframework Flask de Python]
Author: Georgina Vogler
Date: 2026-06-12
"""

from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute(
        'SELECT * FROM posts WHERE id = ?',
        (post_id,)
    ).fetchone()
    conn.close()

    if post is None:
        abort(404)

    return post


@app.route("/")
def home():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('entrada.html', post=post)

@app.route('/crear', methods=('GET', 'POST'))
def crear():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Se requiere un título para la entrada')
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO posts (titulo, contenido) VALUES (?, ?)',
                (title, content)
            )
            conn.commit()
            conn.close()

            return redirect(url_for('home'))

    return render_template('crear.html')

@app.route('/<int:id>/editar', methods=('GET', 'POST'))
def editar(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Se requiere un título para la entrada')
        else:
            conn = get_db_connection()
            conn.execute(
                'UPDATE posts SET titulo = ?, contenido = ? WHERE id = ?',
                (title, content, id)
            )
            conn.commit()
            conn.close()

            return redirect(url_for('home'))

    return render_template('editar.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)

    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash(f'"{post["titulo"]}" ha sido eliminado')

    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404