from flask import current_app # Internal Package: Main flask app module
from flask_login import current_user # Flask login extensions
from flask_login import login_required
from flask import render_template, flash, redirect, url_for # Flask HTML rendering modules
from app.models import User, Post # Internal Module: Implements User, Post model
from flask import request # Flask request module
from app import db # Internal Package: DB handler
from datetime import datetime # Datetime module
from app.main.forms import EditProfileForm # Internal Module: Implements Edit Profile page
from app.main.forms import PostForm # Internal Module: Implements Post form in Index page
from flask_babel import _
from flask import g
from flask_babel import get_locale
from guess_language import guess_language
from flask import jsonify
from app.translate import translate
from app.main import bp
from flask import g # Flask: Global container of Flask
from app.main.forms import SearchForm # Internal: Search form

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET','POST'])
@bp.route('/index', methods=['GET','POST'])
@login_required
def index():

    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live'))
        return redirect(url_for('main.index'))

    page = request.args.get('page',1,type=int)
    posts = current_user.followed_posts().paginate(
        page,current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index',page=posts.next_num) \
            if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url, prev_url=prev_url)



@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page,current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
            if posts.has_next else None
    prev_url = url_for('main.user',username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('user.html', user=user, posts=posts.items,
                next_url=next_url, prev_url=prev_url)

'''    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
'''



@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():

        '''
        form_user = User.query.filter_by(username=form.username.data).first()
        if form_user is not None and form_user.username != current_user.username:
            flash(_('User : "%(username)" already exists. Try different name!',form_user.username))
            return redirect(url_for('main.edit_profile'))
        '''
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title=_('Edit Profile'),form=form)

@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username) not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)!', username=username))
    return redirect(url_for('main.user', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username) not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username).', username=username))
    return redirect(url_for('main.user', username=username))

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,current_app.config['POSTS_PER_PAGE'],False)

    next_url = url_for('main.explore',page=posts.next_num) \
            if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title="Explore", posts=posts.items,
                           next_url=next_url, prev_url=prev_url)



@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)
