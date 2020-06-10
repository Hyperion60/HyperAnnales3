from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from static_files.form.category_forms import CreateCategoryForm
from static_files.methods.category_methods import CreateCategory


@login_required(login_url="/login/")
def CreateCategoryView(request):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    error = False
    if request.POST:
        year, semester, subject, category, title = None, None, None, None, None
        try:
            year = request.POST['year']
            semester = request.POST['semester']
            subject = request.POST['subject']
            category = request.POST['category']
            title = request.POST['title']
        except KeyError:
            context['error'] = "Un ou plusieurs champs sont introuvables"
            error = True
        if not error:
            context = CreateCategory(context, year, semester, subject, title, category)
            try:
                if context['error'] is not None:
                    error = True
            except KeyError:
                if context['message'] is not None:
                    return render(request, "static_content/admin/message_template.html",
                                  {'message': context['message']})
    form = CreateCategoryForm()
    context['year'] = form['year']
    context['semester'] = form['semester']
    context['category'] = form['category']
    context['subject'] = form['subject']
    # Clean error after reset
    if not error:
        context['error'] = None
    return render(request, "static_content/add/add-category.html", context)

