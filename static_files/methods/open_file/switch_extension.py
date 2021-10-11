from static_files.methods.open_file import md, pdf, txt


def switch_extension(request, extension):
    if extension.extension == "pdf":
        return pdf.main(request)
    elif extension.extension == "md":
        return md.main(request)
    elif extension.extension == "txt":
        return txt.main(request)
    else:
        return False  # Page d'erreur


def get_file(request, school, year, semester, subject, file):
    pass