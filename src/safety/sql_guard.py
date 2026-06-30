def assert_readonly_sql(sql: str) -> None:
    lowered = sql.lower()
    banned = ["insert ", "update ", "delete ", "drop ", "alter ", "truncate "]
    if any(keyword in lowered for keyword in banned):
        raise ValueError("Only readonly SQL is allowed")
