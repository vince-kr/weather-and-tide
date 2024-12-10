from jinja2 import Template
import os

import config

with open(config.PROJECT_ROOT / "email-template.html") as wtt:
    template = Template(wtt.read(), trim_blocks=True, lstrip_blocks=True)


def generate_email(template_data: dict) -> str:
    return template.render(template_data)
