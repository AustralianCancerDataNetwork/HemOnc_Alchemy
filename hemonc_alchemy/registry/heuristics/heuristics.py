import re

MAX_ENUM_UNIQUE = 20
MAX_STRING_INLINE = 100

def table_to_class(table: str) -> str:
    """
    Convert table name 'authors_table' -> 'AuthorsTable'.
    """
    table = table.replace(".", "_")
    return "".join(part.capitalize() for part in table.split("_"))


def parse_unique_key(value: str) -> list[str]:
    """
    Parse the 'Unique Key' column into a list of column names.

    Handles patterns like:
      - 'concept_code'
      - 'concept_code_1 + relationship_id + concept_code_2 + vocabulary_id_2'
      - 'name or person_cui'
    """
    if not isinstance(value, str) or not value.strip():
        return []

    # Normalise separators
    text = value.strip()

    # Replace ' or ' with '+' so we treat them as alternate key candidates.
    # For registry purposes we still want the individual column names.
    text = text.replace(" OR ", " or ")
    text = text.replace(" or ", " + ")

    # Now split on '+'
    parts = [p.strip() for p in text.split("+") if p.strip()]

    # Strip any explanatory text in parentheses, keep bare token-ish words
    cols = []
    for p in parts:
        #print(p, re.sub(r"\(.*?\)", "", p).strip())
        for token in p.split():
            ident = re.sub(r'[^0-9a-zA-Z_]', '', str(token))
            if re.match(r"^[A-Za-z_]\w*$", ident):
                cols.append(ident.lower())

    # de-duplicate but keep original order
    seen = set()
    uniq = []
    for c in cols:
        if c not in seen:
            seen.add(c)
            uniq.append(c)

    return uniq
