from pydantic import BaseModel


class MoonPhase(BaseModel):
    phase: str
    phaseEmoji: str


def format_moon_phase(phase_data: dict) -> str:
    phase_object = MoonPhase.model_validate(phase_data)
    return f"{phase_object.phaseEmoji} {phase_object.phase}"
