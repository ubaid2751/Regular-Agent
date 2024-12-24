from string import Template

COMMENT_TEMPLATE = Template(
    """Analyze the given code, identify and fix any errors, including logical bugs, syntax issues, or style problems. Preserve the structure of the code and add comments explaining the fixes made.

    $code

    Return only the corrected code with comments, don't include preamble."""
)

REMOVE_COMMENT_TEMPLATE = Template(
    """Analyze the given code, identify and fix any errors, including logical bugs, syntax issues, or style problems. Preserve the structure of the code. Remove all comments from the code.

    $code

    Return only the corrected code without any comments or preamble."""
)