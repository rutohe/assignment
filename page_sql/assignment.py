import os
from flask import Flask, render_template, request, g
import sqlite3

DBFILE='todo.sqlite'

app = Flask(__name__)

def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()

# データベースに接続する関数
def connect_db():
    # SQLiteデータベースに接続
    conn = sqlite3.connect(DBFILE)
    return conn

# before_requestフックでリクエストごとに接続を確立
@app.before_request
def before_request():
    # データベース接続を作成し、gオブジェクトに保存
    g.db = connect_db()

# teardown_requestフックでリクエスト終了時に接続を切断
@app.teardown_request
def teardown_request(exception):
    # 接続がある場合は切断
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# データベースファイルを開く
# with app.app_context():
#     before_request()

#     query_create_table='''
#         CREATE TABLE IF NOT EXISTS task(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT NOT NULL,
#         done BOOLEAN
#         )
#         '''
    
#     cur=g.db.cursor()
#     cur.execute(query_create_table)        
#     g.db.commit()
#     teardown_request(exception=None)

with app.app_context():
#    before_request()
    init_db()
#    teardown_request(exception=None)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET'])
def form_create():
    query_list_task='''
        SELECT id,title,done FROM task
    '''
    
    cur=g.db.cursor()
    cur.execute(query_list_task)
    tasks=cur.fetchall()
    list_html="<table>"
    list_html+="<tr><th></th><th>ID</th><th>Title</th><th>Done</th></tr>"
    for task in tasks:
        list_html+="<tr><td><input type='checkbox' value='" +str(task[2]==1) + "'/></td><td>"+str(task[0]) + "</td><td>" +task[1] + "</td><td>"+ str(task[2]) + "</td></tr>"
    list_html+="</table>"
    return render_template('create.html',
        title="Create a ToDo Item",
        message="",
        table=list_html
    )

@app.route('/create', methods=['POST'])
def respond_create():
    posted_title=request.form['title']
    
    query_create_task='''
    INSERT INTO task (title,done) VALUES (?,?)
    '''
    
    cur=g.db.cursor()
    cur.execute(query_create_task,(posted_title,False))
    g.db.commit()    
    
    query_list_task='''
        SELECT id,title,done FROM task
    '''
    
    cur=g.db.cursor()
    cur.execute(query_list_task)
    tasks=cur.fetchall()
    list_html="<table>"
    list_html+="<tr><th>ID</th><th>Title</th><th>Done</th></tr>"
    for task in tasks:
        list_html+="<tr><td><input type='checkbox' value='" +str(task[2]==1) + "'/></td><td>"+str(task[0]) + "</td><td>" +task[1] + "</td><td>"+ str(task[2]) + "</td></tr>"
    list_html+="</table>"
    message=posted_title + " Created"

    return render_template('create.html',
        title="Result of Creating a ToDo Item",
        message=message,
        table=list_html
    )
    
@app.route('/read', methods=['GET'])
def read():  
    return render_template('read.html',
        record=""
    )

@app.route('/read', methods=['POST'])
def respond_read():
    posted_id=request.form['id']
    
    query_read_task='''
    SELECT id,title,done FROM task where id=?
    '''
    
    cur=g.db.cursor()
    cur.execute(query_read_task,[posted_id])
    tasks=cur.fetchall()
    if tasks:
        deleteBeforeId = "<form method='POST' action='/delete'><input type='hidden' name='id' value='"
        deleteAfterId =  "' /><input type='submit' value='Delete'/></form>"
        updateHeader = "<form method='POST' action='/update'>"
        updateBeforeHidden = "<input type='hidden' name='id' value='"
        updateAfterHidden = "'/><input type='submit' value='edit'/>"
        updateFooter = "</form>"
        updateDone = "<input type='text' id='done' name='done' required value='"
        updateTitle = "<input type='text' id='title' name='title' required value='"
        updateFormFooter = "'/>"
        list_html="<table>"
        list_html+="<tr><th>ID</th><th>Title</th><th>Done</th></tr>"
        for task in tasks:
            list_html+="<tr>"+updateHeader+"<td>"+ str(task[0]) + "</td><td>" + updateTitle + str(task[1]) + updateFormFooter + "</td><td>"+ updateDone + str(task[2]) + updateFormFooter + "</td><td>"+ updateBeforeHidden + str(task[0]) + updateAfterHidden +updateFooter + deleteBeforeId + str(task[0]) + deleteAfterId + "</td></tr>"
        list_html+= "</table>"
    else:
        list_html="No record found"
    
    return render_template('read.html',
        record=list_html
    )        

@app.route('/update', methods=['GET'])
def update():  
    return render_template('update.html',
        result=""
    )

@app.route('/update', methods=['POST'])
def respond_update():
    posted_id=request.form['id']
    posted_title=request.form['title']
    posted_done=request.form['done'].lower() in ['true','1','t','y','yes']
    
    query_update_task='''
    UPDATE task SET title=?,done=? where id=?
    '''
    
    cur=g.db.cursor()
    cur.execute(query_update_task,(posted_title,posted_done,posted_id))
    g.db.commit()
    
    if cur.rowcount>0:
        list_html="Updated or Unchanged"
    else:
        list_html="No record found"
    
    return render_template('update.html',
        result=list_html
    )
    
    
@app.route('/delete', methods=['GET'])
def delete():  
    return render_template('delete.html',
        result=""
    )

@app.route('/delete', methods=['POST'])
def respond_delete():
    posted_id=request.form['id']
    
    query_delete_task='''
    DELETE FROM task where id=?
    '''
    
    cur=g.db.cursor()
    cur.execute(query_delete_task,[posted_id])
    g.db.commit()
    
    if cur.rowcount>0:
        list_html="Deleted"
    else:
        list_html="No record found"
    
    return render_template('delete.html',
        result=list_html
    )

@app.route('/list', methods=['GET'])
def list():
    query_list_task='''
    SELECT id,title,done FROM task
    '''
    
    cur=g.db.cursor()
    cur.execute(query_list_task)
    tasks=cur.fetchall()
    list_html="<table>"
    list_html+="<tr><th></th><th>ID</th><th>Title</th><th>Done</th></tr>"
    for task in tasks:
        list_html+="<tr><td><input type='checkbox' value='" +str(task[2]==1) + "'/></td><td>"+str(task[0]) + "</td><td>" +task[1] + "</td><td>"+ str(task[2]) + "</td></tr>"
    list_html+="</table>"
    
    return render_template('list.html',
        list=list_html
    )

# お約束
if __name__ == '__main__':
    allowed_host='0.0.0.0'
    server_port=3000
    app.debug=True
    app.run(host=allowed_host,port=server_port)