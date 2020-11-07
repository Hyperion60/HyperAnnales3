from django.shortcuts import render
from django_sendfile import sendfile
import markdown2



# static_file (int: StaticFile.pk)
def open_file(static_file):
    return str(create_token(static_file))


def pdf_model(request, static_file):
    context = {}
    context['year'] = static_file.content.year()
    context['semester'] = static_file.content.semester()
    context['subject'] = static_file.content.subject()
    context['title'] = static_file.content.name
    context['token'] = open_file(static_file.pk)
    return render(request, "static_content/get/pdf_model.html", context)

def zip_model(request, static_file):
    return sendfile(request, static_file.path, attachment=True, attachment_filename=static_file.content.name)

def template_choice(method, request, static_file):
    if method == "pdf":
        return "static_content/get/pdf_model.html"
    elif method == "md":
        return "static_content/get/md_model.html"
    elif method == "code":
        return "static_content/get/code_model.html"
    elif method == "zip":
        return "static_content/get/zip_model.html"
    else:
        return None
