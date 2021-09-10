from django.shortcuts import render

from static_files.methods.bulletin_methods import create_information


def CreateInformation(request, school, year=None):
    context = {'errors': []}
    if request.POST:
        if create_information(request, context):
            context['next'] = "/{}/".format(school)
            if year:
                context['next'] = "/{}/{}/".format(school, year)
            return render(request, "static_content/admin/message_template.html", context)
        context['body'] = request.POST['body']
        context['title'] = request.POST['title']
    return render(request, "static_content/add/add-information.html", context)
