from jinja2 import Template

with open("weather-tide-template.html") as wtt:
    template = Template(wtt.read())

def generate_email(template_data: dict) -> str:
    return template.render(template_data)
