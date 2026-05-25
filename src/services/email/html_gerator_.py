from jinja2 import Template
'''
i choice write the code this shape because a file template was open and close more times, so i open when the project start
this will be close when the project close, also saving CPU processing power and assigning it to the RAM (which is faster than the hard drive)
'''
try:
    with open("src/services/templates/index_code.html", "r", encoding="utf-8") as file:
        template_create_account = Template(file.read())

    with open("src/services/templates/changed_password.html", "r", encoding="utf-8") as file:
        template_changed_password = Template(file.read())
except FileNotFoundError as e:
    print(f"archive not found: {e}")

    template_create_account = None
    template_changed_password = None


def create_html(name: str, code: str, email: str) -> str:

    if not template_create_account:
        raise RuntimeError("Template index_code.html was not loaded correctly.")

    return template_create_account.render(name=name, code=code, emails=email)


def create_html_changed_password(name: str, code: str) -> str:
    if not template_changed_password:
        raise RuntimeError("Template changed_password.html was not loaded correctly.")

    return template_changed_password.render(name=name, code=code)
