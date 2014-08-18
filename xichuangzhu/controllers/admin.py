# coding: utf-8
from flask import render_template, Blueprint, request
from ..models import Work, Author, Dynasty, WorkType, Quote
from ..permissions import admin_permission

bp = Blueprint('admin', __name__)


@bp.route('/authors', defaults={'page': 1})
@bp.route('/authors/<int:page>', methods=['GET', 'POST'])
@admin_permission
def authors(page):
    """管理文学家"""
    paginator = Author.query.paginate(page, 30)
    return render_template('admin/authors.html', paginator=paginator)


@bp.route('/works', defaults={'page': 1})
@bp.route('/works/page/<int:page>', methods=['GET', 'POST'])
@admin_permission
def works(page):
    """管理作品"""
    paginator = Work.query.paginate(page, 15)
    return render_template('admin/works.html', paginator=paginator)


@bp.route('/highlight_works', defaults={'page': 1})
@bp.route('/highlight_works/page/<int:page>', methods=['GET', 'POST'])
@admin_permission
def highlight_works(page):
    """全部加精作品"""
    # 查询条件
    work_type = request.args.get('type', 'all')
    dynasty_abbr = request.args.get('dynasty', 'all')

    # 符合条件的作品
    works = Work.query.filter(Work.highlight == True)
    if work_type != 'all':
        works = works.filter(Work.type.has(WorkType.en == work_type))
    if dynasty_abbr != 'all':
        works = works.filter(Work.author.has(Author.dynasty.has(Dynasty.abbr == dynasty_abbr)))
    paginator = works.paginate(page, 15)

    work_types = WorkType.query
    dynasties = Dynasty.query.order_by(Dynasty.start_year.asc())

    authors_count = Author.query.filter(Author.works.any(Work.highlight)).count()
    works_count = Work.query.filter(Work.highlight).count()
    quotes_count = Quote.query.filter(Quote.work.has(Work.highlight)).count()
    return render_template('admin/highlight_works.html', paginator=paginator, work_type=work_type,
                           dynasty_abbr=dynasty_abbr, work_types=work_types, dynasties=dynasties,
                           authors_count=authors_count, works_count=works_count,
                           quotes_count=quotes_count)
