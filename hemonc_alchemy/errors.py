class HemOncValidationError(RuntimeError):
    """The generated model doesn't match the schema it was generated from.

    Raised while regenerating the model, not while querying it. The message
    lists each problem found.
    """
