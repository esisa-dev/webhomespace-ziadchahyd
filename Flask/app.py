
from flask import Flask, render_template, request, session, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
import os
from passlib.hash import sha512_crypt
import zipfile
import shutil
import logging


app = Flask(__name__)

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)


fh = logging.FileHandler('myapp.log')
fh.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'] )
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate(username, password):
            session['username'] = username
            logger.info(f'User {username} logged in')
            return redirect(url_for('list_directory'))
        else:
            error = 'Invalid credentials'

    return render_template('signin.html', error=error)
def authenticate(username,password):
    shadow = '/etc/shadow'
    os.system('sudo -S chmod o+r /etc/shadow')
    with open(shadow, 'r') as f:
        lines= f.readlines()
    os.system('sudo -S chmod o-r /etc/shadow')
    for line in lines :
        if(username == line.split(':')[0] ):
            hashed = sha512_crypt.hash(password)
            if sha512_crypt.verify(password, hashed):
                return True
    return False

@app.route('/list_directory/')
@app.route('/list_directory/<path:path>')
def list_directory(path=""):
    root_path = '/'
    full_path = os.path.join(root_path, path)
    items = []
    for item in os.listdir(full_path):
        item_path = os.path.join(full_path, item)
        if os.path.isfile(item_path):
            if item_path.endswith('.txt'): 
                with open(item_path, 'r') as f:
                    content = f.read()
                items.append({
                    'name': item,
                    'is_file': True,
                    'size': os.path.getsize(item_path),
                    'path': item_path,
                    'content': content
                })
            else: 
                items.append({
                    'name': item,
                    'is_file': True,
                    'size': os.path.getsize(item_path),
                    'path': item_path
                })
        else:
            items.append({
                'name': item,
                'is_file': False,
                'size': os.path.getsize(item_path),
                'path': item_path
            })
    return render_template('table.html', items=items)
@app.route('/indexe', methods=['GET', 'POST'])
def indexe():
    if request.method == 'POST':
        search_term = request.form['search']
        user_home_dir = os.path.expanduser('~')
        files = []
        for dirpath, dirnames, filenames in os.walk(user_home_dir):
            for filename in filenames:
                if filename.endswith(search_term):
                    filepath = os.path.join(dirpath, filename)
                    file_stat = os.stat(filepath)
                    file_size = file_stat.st_size
                    files.append({
                        'name': filename,
                        'is_file': True,
                        'size': file_size,
                        'path': filepath
                    })
            for dirname in dirnames:
                if dirname.endswith(search_term):
                    dirpath = os.path.join(dirpath, dirname)
                    dir_stat = os.stat(dirpath)
                    dir_size = dir_stat.st_size
                    files.append({
                        'name': dirname,
                        'is_file': False,
                        'size': dir_size,
                        'path': dirpath
                    })
        return render_template('table.html', items=files)
    return render_template('search.html')

@app.route('/download_home_directory')
def download_home_directory():
    home_dir = os.path.expanduser('~')
    zip_filename = 'home_directory.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(home_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, home_dir))
    logger.info(f'User downloaded home directory')
    return send_file(zip_filename, as_attachment=True)
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    logger.info(f'User logged out')
    return redirect(url_for('login'))
@app.route('/count_files')
def Files():
    user_home_dir = os.path.expanduser('~')
    num_files = sum(len(files) for _, _, files in os.walk(user_home_dir))
    return f"The number of files in your home directory is: {num_files}"
@app.route('/dirs')
def Dirs():
    user_home_dir = os.path.expanduser('~')
    dirs_count = 0
    for  dirnames in os.walk(user_home_dir):
        dirs_count += len(dirnames)
    return f"The number of directories in your home directory is : {dirs_count}."
@app.route('/space')
@app.route('/space')
def space():
    home_dir = os.path.expanduser('~')
    total_space, used_space, free_space = shutil.disk_usage(home_dir)
    return f"Used space: {used_space} bytes, Total space: {total_space} bytes , Free space : {free_space} bytes"



if  __name__== "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,port=5001)