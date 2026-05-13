from jinja2 import Template

#it function open the archive in template (index_code.html) and read this, instance template
#and finally  get variables and render this and return html
def create_html(name: str, code: str, emails: str):
    with open("src/services/templates/index_code.html", "r", encoding="utf-8") as file:
        template_str = file.read()
        template = Template(template_str)
        html = template.render(name=name, code=code, emails=emails)
        return html

def create_html_changed_password(name: str, code: str):
    with open("src/services/templates/changed_password.html", "r", encoding="utf-8") as file:
        template_str = file.read()
        template = Template(template_str)
        html = template.render(name=name, code=code)
        return html