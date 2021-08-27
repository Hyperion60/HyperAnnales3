from static_files.models import StaticContent


def get_color(static_content):
    if not type(static_content) is StaticContent:
        return None
    return str(static_content.classe)[1:-1].split(',')[1][2:-1]
