
# Sanitize response to prevent markdown formatting issues
def sanitize_response(text):
    if not isinstance(text, str):
        text = str(text)
    
    # Escape special markdown characters
    replacements = {
        '$': '\\$',      # LaTeX math
        '*': '\\*',      # Bold/italic
        '_': '\\_',      # Bold/italic
        '`': '\\`',      # Code blocks
        '#': '\\#',      # Headers
        '[': '\\[',      # Links
        ']': '\\]',      # Links
        '(': '\\(',      # Links
        ')': '\\)',      # Links
        '|': '\\|',      # Tables
        '^': '\\^',      # Superscript
        '~': '\\~',      # Strikethrough
        '<': '&lt;',     # HTML tags
        '>': '&gt;',     # HTML tags
        '&': '&amp;'     # HTML entities
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text