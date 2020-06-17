from sendfile import sendfile
import markdown2


def template_choice(method):
    if method == "pdf":
        return "static_content/get/pdf_model.html"
    elif method == "md":
        return "static_content/get/md_model.html"
    elif method == "code":
        return "static_content/get/code_model.html"
    else:
        return None