from flask import Flask, render_template, request, redirect, url_for

# 一个 Flask 应用实例
app = Flask(__name__)
# 定义一个路由 (Routing)
@app.route('/')
def show_index_page():
    """ 显示首页 """
    return render_template('index.html')

@app.route('/contact')
def show_contact_page():
    """ 显示联系页 """
    return render_template('contact.html')

@app.route('/interests')
def show_interests_page():
    """ 显示兴趣页 """
    return render_template('interests.html')

@app.route('/about')
def show_about_page():
    """ 显示关于页 """
    return render_template('about.html')

@app.route('/blogs')
def show_blogs_page():
    """ 显示博客页 """
    return render_template('blogs_summary.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        pw = request.form.get("password", "").strip()
        # TODO: 这里替换为你的鉴权逻辑，比如对接数据库或哈希校验
        if pw == "ok":
            return redirect("/management")  # 或 url_for('management')
        else:
            return render_template("login.html", error="密码错误"), 401
    return render_template("login.html")

@app.route('/management')
def management():
    """ 显示管理页 """
    return render_template('management.html')