def execute_query(connection, queries):
    results = {}
    for query in queries:
        connection.cursor.execute(queries[query])
        results[query] = connection.cursor.fetchall()
    return results
