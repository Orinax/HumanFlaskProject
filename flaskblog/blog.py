from bs4 import BeautifulSoup
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskblog.auth import login_required
from flaskblog.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog' )


def truncate_html(html_content, post_id, max_length=500, min_length=200):
    """
    Truncates HTML content while preserving basic formatting
    """
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')

    # Find a good breaking point
    if not paragraphs:
        return html_content

    # Create a new div with the ql-editor class to maintain Quill formatting
    new_div = soup.new_tag('div')
    new_div['class'] = 'ql-editor'

    # Create an empty paragraph for spacting
    empty_para = soup.new_tag('p')
    empty_para.string = '\n'
    
    # Create the link inside an italics tag
    link_para = soup.new_tag('p')
    italics = soup.new_tag('em')
    continue_reading_link = soup.new_tag('a')
    continue_reading_link['href'] = url_for('blog.detail_view', id=post_id)
    continue_reading_link.string = 'Continue reading...'
    italics.append(continue_reading_link)
    link_para.append(italics)

    # Check the length of the first paragraph
    first_para = paragraphs[0].get_text()
    
    if len(first_para) > min_length:
        # If first paragraph is long, only show that one
        first_para = paragraphs[0]
        if len(paragraphs) > 1:
            new_div.append(first_para)
            new_div.append(empty_para)
            new_div.append(link_para)
        else:
            new_div.append(first_para)
    else:
        current_length = 0
        for i, para in enumerate(paragraphs):
            para_text = para.get_text()
            if current_length + len(para_text) > max_length:
                new_div.append(empty_para)
                new_div.append(link_para)
                break
            new_div.append(para)
            current_length += len(para_text)

            if i == len(paragraphs) - 1:
                break

            if current_length < len(''.join(p.get_text() for p in paragraphs)) and i == len(paragraphs) - 1:
                new_div.append(empty_para)
                new_div.append(link_para)

    return str(new_div)

def get_post(id, check_author=True):
    '''
    Get the entire contents of a post for the given id.
    '''
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

def get_most_recent_post():
    '''
    Get the entire contents of the most recent post.
    '''
    db = get_db()

    # Get posts for current page
    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC',
    ).fetchone()
 
    return post

def get_post_titles():
    '''
    Get only the post titles for all posts ever made.
    (This may need to be adjusted later if there are too many posts).
    '''
    db = get_db()

    # Get posts for current page
    posts = db.execute(
        'SELECT p.id, title'
        ' FROM post p'
        ' ORDER BY created DESC',
    ).fetchall()
 
    # Convert posts to list of dictionaries
    posts_preview = []
    for post in posts:
        post_dict = dict(post)
        posts_preview.append(post_dict)

    return posts_preview


@bp.route('/')
@bp.route('/page/<int:page>')
def index(page=1):
    post = get_most_recent_post()
    post_titles = get_post_titles()

    return render_template('blog/index.html', post=post, 
                           posts=post_titles, page=page,)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                'VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>', methods=('GET',))
def detail_view(id):
    post = get_post(id, check_author=False);
    post_titles = get_post_titles()
    return render_template('blog/detail.html', post=post, posts=post_titles,)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
