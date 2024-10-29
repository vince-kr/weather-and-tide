from jinja2 import Template
import os

with open(os.path.dirname(os.path.abspath(__file__)) + '/weather-tide-template.html') as wtt:
    template = Template(wtt.read())

def generate_email(template_data: dict) -> str:
    return template.render(template_data)
