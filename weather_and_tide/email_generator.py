from jinja2 import Template

from weather_and_tide import config

with open(config.PACKAGE_ROOT / "email-template.html") as wtt:
    template = Template(wtt.read(), trim_blocks=True, lstrip_blocks=True)


def generate_email(template_data: dict) -> str:
    return template.render(template_data)
