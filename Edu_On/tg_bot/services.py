from contextlib import closing

from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return []
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def get_videos(sub_name, name=None):
    extra = ""
    if name:
        extra = f""" and tv."name"='{name}'"""

    sql = f"""
    select ts."name", array_agg(row_to_json(tv)) as videos from tg_bot_sub ts
    inner join (
    select video, sub_id, "name", chat_id  from tg_bot_videos 
    ) tv on tv.sub_id = ts.id
        where ts."name" = '{sub_name}' {extra}

    group by ts."name" 
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)

        items = dictfetchone(cursor)
        result = []


        if items:
            for i in items["videos"]:
                result.append(i)

    return result
















