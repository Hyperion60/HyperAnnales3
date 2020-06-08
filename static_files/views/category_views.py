from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from static_files.form.category_forms import CreateCategoryForm


@login_required(login_url="/login/")
def CreateCategoryView(request):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    if request.POST:
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            print(subject)
            context['error'] = "Not implemented"
        else:
            context['error'] = "Form is not valid"
    else:
        context['form'] = CreateCategoryForm()
    print(context)
    return render(request, "static_content/add/add-category.html", context)

