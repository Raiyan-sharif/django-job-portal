def match(required, offered):
    """Compare a job's required skills with a job seeker's skills."""
    required = set(required)
    offered = set(offered)
    matched = sorted(required & offered)
    missing = sorted(required - offered)
    percent = round(100 * len(matched) / len(required)) if required else 0

    if percent >= 75:
        level = 'strong'
    elif percent >= 40:
        level = 'partial'
    else:
        level = 'weak'

    return {'matched': matched, 'missing': missing, 'percent': percent, 'level': level}