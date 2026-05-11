from jinja2 import Template
def create_html(name: str, code: str):
    with open("../templates/index_code.html", "r", encoding="utf-8") as file:
        dicts = {"name": "glauber"}
        template_str = file.read()
        template = Template(template_str)
        html = template.render(name=dicts["name"], code=code)
        return html