def truncate(text: str, lines: int, columns: int = 100, trim_text: str = '...') -> str:
    # TODO optimize for large text
    rows = text.split('\n')
    rows_result = []
    for idx in range(min(len(rows), lines)):
        row = rows[idx]
        if len(row) > columns:
            row = row[:columns] + trim_text
        rows_result.append(row)

    if len(rows) <= lines:
        return '\n'.join(rows_result)

    return '\n'.join(rows[:lines]) + '\n' + trim_text
