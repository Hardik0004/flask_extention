from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from flask import current_app as app
from flask import g, request
from flask_api import status
from sqlalchemy import false, true

from database import db
from src.functionality.article.serializer import (
    articles_info_data,
    articles_info_post_data,
    saved_article_data,
)
from src.resources.article.model import Article, SavedArticle
from src.utils.exception import MuzliException
from src.utils.validator import authenticated, authenticated_user


def get_article_category(url):
    app.logger.info("Functionality: article category from url")
    req_data: dict = request.json
    category = req_data.get("category")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    if category:
        return category
    else:
        category = (
            soup.find("meta", property="article:section")["content"]
            if soup.find("meta", property="article:section")
            else None
        )
        if category:
            return category
        else:
            category = "General"
    return category


@authenticated_user
def post_article_info():
    app.logger.info("Functionality: create article from url")
    req_data: dict = request.json
    user_id = g.user.user_id
    url = req_data.get("article_link")
    category = get_article_category(url)
    parsed_url = urlparse(url)
    website_url = parsed_url.netloc
    if website_url.startswith("https://www."):
        website_url = website_url[12:]
    print(website_url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_link = soup.find("meta", property="og:image")["content"]
    article_name = soup.find("meta", property="og:title")["content"]
    website_name = soup.find("meta", property="og:site_name")["content"]
    article_link = soup.find("meta", property="og:url")["content"]

    article_info = Article(
        article_link=article_link,
        user_id=user_id,
        category=category,
        image_link=image_link,
        website_name=website_name,
        website_url=website_url,
        name=article_name,
    )
    db.session.add(article_info)
    db.session.commit()
    article_info = articles_info_post_data(article_info)
    db.session.close()

    return article_info


@authenticated_user
def get_articles_for_user():
    app.logger.info("Functionality: get article for user")
    user_id = g.user.user_id
    article_info = Article.query.filter(
        Article.user_id == user_id, Article.is_deleted == false()
    ).all()

    if not article_info:
        raise MuzliException(status.HTTP_404_NOT_FOUND, "User not found")

    return article_info


@authenticated
def get_articles():
    app.logger.info("Functionality: get all article")
    article_info = Article.query.filter(Article.is_deleted == false()).all()

    if not article_info:
        raise MuzliException(status.HTTP_404_NOT_FOUND, "Articles not found")

    return article_info


@authenticated_user
def update_articles():
    app.logger.info("Functionality: get article for user")
    user_id = g.user.user_id
    req_data: dict = request.json
    id = req_data.get("id")
    article_info = Article.query.filter(
        Article.user_id == user_id, Article.id == id, Article.is_deleted == false()
    ).update(req_data)
    if not article_info:
        raise MuzliException(status.HTTP_404_NOT_FOUND, "Article not found")
    db.session.commit()
    db.session.close()
    return "Updated Article Successfully"


@authenticated_user
def delete_articles():
    app.logger.info("Functionality: delete article")
    user_id = g.user.user_id
    req_data: dict = request.json
    id = req_data.get("id")
    article_info = Article.query.filter(
        Article.user_id == user_id, Article.id == id, Article.is_deleted == false()
    ).first()

    if not article_info:
        raise MuzliException(status.HTTP_404_NOT_FOUND, "Article not found")
    article_info.is_deleted = true()
    db.session.commit()
    db.session.close()
    return "Delete Article Successfully"


@authenticated
def increment_share():
    app.logger.info("Functionality: share")
    id = request.args.get("article_id")
    article = Article.query.filter(
        Article.id == id, Article.is_deleted == false(), Article.is_active == true()
    ).first()

    if not article:
        raise MuzliException(status.HTTP_404_NOT_FOUND, "Article not found")
    article.share += 1
    db.session.commit()
    article_share = article.share
    db.session.close()

    return article_share


@authenticated
def increment_watch():
    app.logger.info("Functionality: watch")
    id = request.args.get("article_id")
    article = Article.query.filter(
        Article.id == id, Article.is_deleted == false(), Article.is_active == true()
    ).first()

    if not article:
        raise MuzliException(status.HTTP_404_NOT_FOUND, "Article not found")
    article.watch += 1
    db.session.commit()
    article_watch = article.watch
    db.session.close()

    return article_watch


@authenticated
def get_share():
    app.logger.info("Functionality: get share")
    id = request.args.get("article_id")
    article = Article.query.filter(
        Article.id == id, Article.is_deleted == false(), Article.is_active == true()
    ).first()

    if not article:
        raise MuzliException(status.HTTP_404_NOT_FOUND, "Article not found")

    article_share = article.share
    db.session.close()

    return article_share


@authenticated
def get_watch():
    app.logger.info("Functionality: get watch")
    id = request.args.get("article_id")
    article = Article.query.filter(
        Article.id == id, Article.is_deleted == false(), Article.is_active == true()
    ).first()

    if not article:
        raise MuzliException(status.HTTP_404_NOT_FOUND, "Article not found")
    article_watch = article.watch
    db.session.close()

    return article_watch


@authenticated_user
def save_article():
    app.logger.info("Functionality: save article")
    user_id = g.user.user_id
    req_data: dict = request.json
    article_id = req_data.get("article_id")

    article_info = Article.query.filter(
        Article.id == article_id,
        Article.is_deleted == false(),
        Article.is_active == true(),
    ).first()
    article_info = articles_info_data(article_info)
    saved_article = SavedArticle(
        user_id=user_id,
        article_info=article_info,
    )

    db.session.add(saved_article)
    db.session.commit()
    db.session.close()
    return "Article Save Successfully"


@authenticated_user
def get_save_article_user():
    app.logger.info("Functionality: get saved article for user")
    user_id = g.user.user_id
    saved_article_info = SavedArticle.query.filter(
        SavedArticle.user_id == user_id
    ).all()
    saved_article = saved_article_data(saved_article_info)

    db.session.close()

    return saved_article
