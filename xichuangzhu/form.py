# coding: utf-8
from flask_wtf import Form
from wtforms import TextField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ReviewForm(Form):
    """Form for add and edit work review"""
    title = TextField('标题', [DataRequired(message="标题不能为空")])
    content = TextAreaField('内容', [DataRequired(message="内容不能为空")])


class TopicForm(Form):
    """Form for add and edit topic"""
    title = TextField('标题', [DataRequired(message="标题不能为空")])
    content = TextAreaField('内容', [DataRequired(message="内容不能为空")])


class CommentForm(Form):
    """Form for add comment"""
    content = TextAreaField('回复', [DataRequired(message="回复不能为空")])


class EmailForm(Form):
    """Form for send email"""
    email = TextField('邮箱', [DataRequired(message="邮箱不能为空"), Email(message="无效的邮箱")])
    user_id = HiddenField('用户ID', [DataRequired(message="用户ID不能为空")])


class WorkImageForm(Form):
    """Form for add and edit work image"""
    image = FileField('作品', [FileRequired('作品图片不能为空')])