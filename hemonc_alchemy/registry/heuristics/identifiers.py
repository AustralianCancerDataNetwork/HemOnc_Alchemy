
import keyword
import re
PY_KEYWORDS = set(keyword.kwlist)

def safe_identifier(name: str) -> str:
    """Return a safe Python identifier."""
    if name is None:
        return "_"

    # Convert to string and strip invalid identifier characters
    # Keep only letters, digits, and underscores
    ident = re.sub(r'[^0-9a-zA-Z_]', '', str(name))

    # Prefix underscore if it begins with a digit
    if ident and ident[0].isdigit():
        ident = "_" + ident

    # Fallback if everything was stripped
    if not ident:
        ident = "_"

    ident = ident.lower()

    # Avoid python keywords
    if ident in PY_KEYWORDS:
        ident = ident + "_field"

    return ident

