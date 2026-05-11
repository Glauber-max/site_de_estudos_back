from jinja2 import Template

def create_html(name: str, code: str, emails: str):
    with open("src/services/templates/index_code.html", "r", encoding="utf-8") as file:
        template_str = file.read()
        template = Template(template_str)
        html = template.render(name=name, code=code, emails=emails)
        return html