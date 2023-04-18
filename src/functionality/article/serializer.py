def articles_info_data(articles_info):
    if not isinstance(articles_info, list):
        articles_info = [articles_info]

    return [
        {
            "article_id": record.id,
            "user_id": record.user_id,
            "article_link": record.article_link,
            "image_link": record.image_link,
            "category": record.category,
            "website_name": record.website_name,
            "share": record.share,
            "watch": record.watch,
        }
        for record in articles_info
    ]


def articles_info_post_data(articles_info):
    if not isinstance(articles_info, list):
        articles_info = [articles_info]

    return [
        {
            "article_name": record.name,
            "article_id": record.id,
            "image_link": record.image_link,
            "category": record.category,
            "website_name": record.website_name,
            "website_url": record.website_url,
        }
        for record in articles_info
    ]


def saved_article_data(articles_info):
    if not isinstance(articles_info, list):
        articles_info = [articles_info]

    return [
        {
            "article_info": record.article_info,
        }
        for record in articles_info
    ]
