import re

CSS_URL_REGEXP = re.compile(
    r'(url\(\/static\/media\/(.+)\))', flags=re.I
)
# "static/media/logo.6ce24c58023cc2f8fd88fe9d219db6c6.svg"
JS_URL_REGEXP = re.compile(
    r'(["\']static\/media\/(.+)["\'])', flags=re.I
)

HTML_SCRIPT_TAG_REGEXP = re.compile(
    r'((<script.*src=["\'])(\/static)(\/.+)(["\']>.*<\/script>))', flags=re.I
)

HTML_LINK_TAG_REGEXP = re.compile(
    r'((<link href=["\'])(\/static)(\/.+)(["\'] rel=["\']stylesheet["\']>))',
    flags=re.I
)
HTML_NOSCRIPT_TAG_REGEXP = re.compile(
     r'<noscript>.*<\/noscript>', flags=re.I
)
HTML_DIVROOT_TAG_REGEXP = re.compile(
     r'<div.*id=["\'].+["\']>.*<\/div>', flags=re.I
)
