# coding: utf-8
from flask import render_template, request, redirect, url_for, json, session, abort
from xichuangzhu import app, db
from xichuangzhu.models.work import Work, WorkType, WorkTag, WorkImage, WorkReview, Tag
from xichuangzhu.models.dynasty import Dynasty
from xichuangzhu.models.author import Author
from xichuangzhu.models.user import User
from xichuangzhu.models.collect import CollectWork
from xichuangzhu.utils import require_login, require_admin


@app.route('/work/<int:work_id>')
def work(work_id):
    """文学作品"""
    work = Work.query.get_or_404(work_id)

    if 'user_id' in session:
        is_collected = CollectWork.query.filter(CollectWork.work_id == work_id).filter(
            CollectWork.user_id == session['user_id']).count() > 0
    else:
        is_collected = False

    reviews = work.reviews.order_by(WorkReview.create_time.desc()).filter(WorkReview.is_publish == True).limit(4)
    reviews_num = work.reviews.filter(WorkReview.is_publish == True).count()

    images = work.images.order_by(WorkImage.create_time).limit(16)
    images_num = work.images.count()

    other_works = Work.query.filter(Work.author_id == work.author_id).filter(Work.id != work_id).limit(5)

    collectors = User.query.join(CollectWork).join(Work).filter(Work.id == work_id).limit(4)

    return render_template('work/work.html', work=work, reviews=reviews, reviews_num=reviews_num, images=images,
                           images_num=images_num, collectors=collectors, is_collected=is_collected,
                           other_works=other_works)


@app.route('/work/<int:work_id>/collect', methods=['GET'])
@require_login
def collect_work(work_id):
    """收藏作品"""
    collect = CollectWork(user_id=session['user_id'], work_id=work_id)
    db.session.add(collect)
    db.session.commit()
    return redirect(url_for('work', work_id=work_id))


@app.route('/work/<int:work_id>/discollect')
@require_login
def discollect_work(work_id):
    """取消收藏文学作品"""
    db.session.query(CollectWork).filter(CollectWork.user_id == session['user_id']).filter(
        CollectWork.work_id == work_id).delete()
    db.session.commit()
    return redirect(url_for('work', work_id=work_id))


@app.route('/works')
def works():
    """全部文学作品"""
    work_type = request.args.get('type', 'all')
    dynasty_abbr = request.args.get('dynasty', 'all')
    page = int(float(request.args.get('page', 1)))

    query = Work.query
    if work_type != 'all':
        query = query.filter(Work.type.has(WorkType.en == work_type))
    if dynasty_abbr != 'all':
        query = query.filter(Work.author.has(Author.dynasty.has(Dynasty.abbr == dynasty_abbr)))
    pagination = query.paginate(page, 10)

    work_types = WorkType.query
    dynasties = Dynasty.query.order_by(Dynasty.start_year)
    return render_template('work/works.html', pagination=pagination, work_type=work_type, dynasty_abbr=dynasty_abbr,
                           work_types=work_types, dynasties=dynasties)


@app.route('/tags')
def tags():
    """作品标签页"""
    tags = Tag.query.all()
    return render_template('work/tags.html', tags=tags)


@app.route('/tag/<int:tag_id>')
def tag(tag_id):
    """作品标签"""
    tag = Tag.query.get_or_404(tag_id)
    page = int(request.args.get('page', 1))
    pagination = Work.query.filter(Work.tags.any(WorkTag.tag_id == tag_id)).paginate(page, 12)
    return render_template('work/tag.html', tag=tag, pagination=pagination)


@app.route('/work/add', methods=['GET', 'POST'])
@require_admin
def add_work():
    """添加作品"""
    if request.method == 'GET':
        if 'author_id' in request.args:
            author = Author.query.get_or_404(request.args['author_id'])
        else:
            author = None
        work_types = WorkType.query
        return render_template('work/add_work.html', work_types=work_types, author=author)
    work = Work(title=request.form['title'], content=request.form['content'], foreword=request.form['foreword'],
                intro=request.form['intro'], author_id=int(request.form['author_id']),
                type_id=request.form['type_id'])
    db.session.add(work)
    db.session.commit()
    return redirect(url_for('work', work_id=work.id))


@app.route('/work/<int:work_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit_work(work_id):
    """编辑作品"""
    work = Work.query.get_or_404(work_id)
    if request.method == 'GET':
        work_types = WorkType.query
        return render_template('work/edit_work.html', work=work, work_types=work_types)
    else:
        work.title = request.form['title']
        work.content = request.form['content']
        work.foreword = request.form['foreword']
        work.intro = request.form['intro']
        work.author_id = int(request.form['author_id'])
        work.type_id = request.form['type_id']
        db.session.add(work)
        db.session.commit()
        return redirect(url_for('work', work_id=work_id))


@app.route('/work/<int:work_id>/reviews')
def work_reviews(work_id):
    """文学作品的点评"""
    work = Work.query.get_or_404(work_id)
    page = int(request.args.get('page', 1))
    pagination = work.reviews.filter(WorkReview.is_publish == True).order_by(WorkReview.create_time.desc()).paginate(
        page, 10)
    return render_template('work/work_reviews.html', work=work, pagination=pagination)


@app.route('/work/<int:work_id>/images', methods=['GET'])
def work_images(work_id):
    """文学作品的相关图片"""
    work = Work.query.get_or_404(work_id)
    page = int(request.args.get('page', 1))
    pagination = work.images.order_by(WorkImage.create_time.desc()).paginate(page, 16)
    return render_template('work/work_images.html', work=work, pagination=pagination)


@app.route('/work/search_authors', methods=['POST'])
@require_admin
def search_authors():
    """根据关键字返回json格式的作者信息"""
    author_name = request.form.get('author_name', '')
    authors = Author.query.filter(Author.name.like('%%%s%%' % author_name))

    dict_authors = []
    for a in authors:
        dict_authors.append({'id': a.id, 'dynasty': a.dynasty.name, 'name': a.name})
    return json.dumps(dict_authors)