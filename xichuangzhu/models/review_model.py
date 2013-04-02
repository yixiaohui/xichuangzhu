from flask import g

class Review:

# GET

	# get a review
	@staticmethod
	def get_review(review_id):
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, review.ClickNum, user.UserID, user.Abbr AS UserAbbr, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.ReviewID = %d\n
			AND review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID''' % review_id
		g.cursor.execute(query)
		return g.cursor.fetchone()

	# get reviews by random
	@staticmethod
	def get_reviews_by_random(reviews_num):
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Abbr AS UserAbbr, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID\n
			LIMIT %d''' % reviews_num
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get hot reviews
	@staticmethod
	def get_hot_reviews():
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Abbr AS UserAbbr, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID\n'''
		g.cursor.execute(query)
		return g.cursor.fetchall()	

	# get reviews of a work
	@staticmethod
	def get_reviews_by_work(work_id):
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Abbr AS UserAbbr, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.WorkID = %d\n
			AND review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID''' % work_id
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get reviews from a user
	@staticmethod
	def get_reviews_by_user(user_id, num):
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.UserID = %d\n
			AND review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID
			ORDER BY review.Time LIMIT %d''' % (user_id, num)
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get hot reviewers
	@staticmethod
	def get_hot_reviewers(num):
		query = '''SELECT review.UserID, user.Avatar, user.Name, user.Abbr, user.Signature, COUNT(*) AS ReviewNum\n
			FROM review, user\n
			WHERE review.UserID = user.UserID\n
			GROUP BY review.UserID\n
			ORDER BY ReviewNum DESC\n
			LIMIT %d''' % num
		g.cursor.execute(query)
		return g.cursor.fetchall()
# NEW

	# add a review to a work
	@staticmethod
	def add_review(work_id, user_id, title, content):
		query = '''INSERT INTO review (WorkID, UserID, Title, Content)\n
			VALUES (%d, %d, '%s', '%s')''' % (work_id, user_id, title, content)
		g.cursor.execute(query)
		g.conn.commit()
		return g.cursor.lastrowid

# UPDATE

	# edit a view
	@staticmethod
	def edit_review(review_id, title, content):
		query = '''UPDATE review SET Title = '%s', Content = '%s' WHERE ReviewID = %d''' % (title, content, review_id)
		g.cursor.execute(query)
		return g.conn.commit()

	# add click num
	@staticmethod
	def add_click_num(review_id):
		query = '''UPDATE review SET ClickNum = ClickNum + 1 WHERE ReviewID = %d''' % review_id
		g.cursor.execute(query)
		return g.conn.commit()

	# add comment num
	@staticmethod
	def add_comment_num(review_id):
		query = "UPDATE review SET CommentNum = CommentNum + 1 WHERE ReviewID = %d" % review_id
		g.cursor.execute(query)
		return g.conn.commit()