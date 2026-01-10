import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskblog.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)


    @app.context_processor
    def inject_recent_posts():
        db_conn = db.get_db()
        raw_posts = db_conn.execute(
            'SELECT id, title, created FROM post ORDER BY created DESC LIMIT 3'
        ).fetchall()

        formatted_posts = []
        for post in raw_posts:
            date_str = post['created'].strftime('%Y-%m-%d')
            formatted_posts.append({
                'id': post['id'],
                'title': post['title'],
                'created': date_str
            })

        return dict(recent_posts=formatted_posts)

    return app


