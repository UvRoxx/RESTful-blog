from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = StringField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


posts = db.session.query(BlogPost).all()


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    for post in posts:
        if post.id == index:
            requested_post = post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/create", methods=['GET', 'POST'])
def create_post():
    create_form = CreatePostForm()
    if create_form.validate_on_submit():
        title = create_form.title.data
        subtitle = create_form.subtitle.data
        body = create_form.body.data
        author = create_form.author.data
        img_url = create_form.img_url.data
        new_post = BlogPost(title=title, subtitle=subtitle, date=date.today(), body=body, author=author,
                            img_url=img_url)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts', posts=posts))
    return render_template('make-post.html', form=create_form)


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    edit_post = BlogPost.query.get(id)
    edit_form = CreatePostForm(
        title=edit_post.title,
        subtitle=edit_post.subtitle,
        author=edit_post.author,
        body=edit_post.body,
        img_url=edit_post.img_url)
    if edit_form.validate_on_submit():
        edit_post.title = edit_form.title.data
        edit_post.subtitle = edit_form.subtitle.data
        edit_post.body = edit_form.body.data
        edit_post.author = edit_form.author.data
        edit_post.img_url = edit_form.img_url.data
        db.session.commit()
        print("updated")
        return redirect(url_for("show_post", index=edit_post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/del/<id>")
def del_post(id):
    post_to_del = BlogPost.query.get(id)
    db.session.delete(post_to_del)
    db.session.commit()
    return render_template(url_for('get_all_posts',posts=posts))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
