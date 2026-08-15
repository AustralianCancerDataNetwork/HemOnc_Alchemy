class HemOncValidationError(RuntimeError):
    """Raised when a generated model fails validation against its schema.

    Analogous to omop_alchemy.errors.CDMValidationError, but produced by
    compiler/validate.py and compiler/diff.py rather than by any
    OMOP-specific spec check.
    """
