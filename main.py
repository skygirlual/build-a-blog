from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(510))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return redirect ('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def allblogposts():
    allPosts = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blogposts.html',title="My Fantastic Blog", posts=allPosts)

@app.route('/post/<int:post_id>', methods=['POST', 'GET'])
def show_post(post_id):
    max_post_id = db.session.query(db.func.max(Blog.id)).scalar()
    if post_id == 0 or post_id > max_post_id:
            return redirect ('/blog')

    onePost = Blog.query.filter(Blog.id==post_id).all()
    title_post=onePost[0].title

    return render_template('post.html', posts=onePost, post_id=post_id)

@app.route('/newpost', methods=['POST', 'GET'])
def newPost():

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        
        # input validation
        checklist =[post_title, post_body]
        title_error = ''
        body_error = ''
        for item in checklist:
            if len(post_title) <1 or len(post_title) > 120:
                title_error = "Post must have a title."
                return render_template('newpost.html', post_body = post_body, title_error = title_error)

            if len(post_body) <1 or len(post_body) > 520:
                body_error = "You forgot the body."
                return render_template('newpost.html', post_title = post_title, body_error = body_error)

        if not title_error and not body_error:
            new_post = Blog(post_title, post_body)
            db.session.add(new_post)
            db.session.commit()
            new_post_id = db.session.query(db.func.max(Blog.id)).scalar()
            onePost = Blog.query.filter(Blog.id==new_post_id).all()
            return redirect('/post/%s' % new_post_id)

    else:
        return render_template('newpost.html')

if __name__ == '__main__':
    app.run()