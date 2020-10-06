def row2dict(row) -> dict:
    res = {}
    for column in row.__table__.columns:
        res[column.name] = str(getattr(row, column.name))
    del(res['id'])
    return res
