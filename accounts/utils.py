from .models import Skill


def parse_skills(text):
    """'Python, Django ,  SQL' -> ['python', 'django', 'sql']"""
    names = []
    for part in (text or '').split(','):
        name = ' '.join(part.strip().lower().split())
        if name and name not in names:
            names.append(name)
    return names


def skills_from_text(text):
    """Return Skill objects for a comma-separated string, creating new ones."""
    return [Skill.objects.get_or_create(name=name)[0] for name in parse_skills(text)]


def skills_to_text(skills):
    return ', '.join(skill.name for skill in skills)