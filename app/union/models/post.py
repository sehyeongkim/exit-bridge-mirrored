from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Boolean
from core.db.mixins import TimestampMixin
from core.db import Base


class Feed(Base, TimestampMixin):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gp_id = Column(Integer, nullable=False)
    union_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    deleted_at = Column(DateTime)


class FeedComment(Base, TimestampMixin):
    __tablename__ = 'feed_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), nullable=False)
    feed_id = Column(Integer, nullable=False)
    content = Column(String(255))
    is_secret = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    mentioned_at = Column(DateTime)


class MainPost(Base, TimestampMixin):
    __tablename__ = 'main_posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=False)
    gp_id = Column(Integer, nullable=False)
    intro = Column(Text)
    title = Column(String(40))
    is_activated = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    main_post_detail_id = Column(Integer)


class MainPostDetail(Base):
    __tablename__ = 'main_post_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    html_text = Column(Text)
    inobiz_url = Column(Text)
    dart_url = Column(Text)
    attachment_json = Column(JSON)
    article_json = Column(JSON)


class MainPostQna(Base, TimestampMixin):
    __tablename__ = 'main_post_qna'

    id = Column(Integer, primary_key=True, autoincrement=True)
    main_post_id = Column(Integer, nullable=False)
    user_id = Column(String(20), nullable=False)
    title = Column(String(40))
    content = Column(Text)
    is_answered = Column(Boolean, default=False)
    answer = Column(Text)


class Click(Base, TimestampMixin):
    __tablename__ = 'clicks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    click_count = Column(Integer)
    post_type = Column(String(20))
    post_id = Column(Integer)
