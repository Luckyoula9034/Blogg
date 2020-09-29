from flask import render_template
from app import app

# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    massage ='welcome to the blog world'
    return render_template('index.html',massage=massage)

@app.route('/blog/<blog_id>')
def movie(blog_id):

    '''
    View movie page function that returns the movie details page and its data
    '''
    return render_template('blog.html',id = blog_id)