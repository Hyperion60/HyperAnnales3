from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from static_files.models import School, CategoryFile, CategoryColor
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
            school = School.objects.filter(school__exact=request.user.school)
        except KeyError:
            context['error'] = "Un ou plusieurs champs sont introuvables"
            error = True
        if not error:
            context = CreateCategory(context, school, year, semester, subject, title, category)
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


@login_required(login_url="/login/")
def ChangeCategory(request, pk):
    context = {'errors': []}
    context['next'] = request.GET.get('next', '')
    if not request.user.is_staff:
        context['errors'].append("Accès refusé: Droits insuffisants")
        return render(request, "static_content/admin/message_template.html", context)
    category = None
    context['next'] = request.GET.get('next', '')
    try:
        category = CategoryFile.objects.get(pk=pk)
    except CategoryFile.DoesNotExist:
        context['errors'].append("Category : La clé primaire n'existe pas")

    context['category'] = category
    if request.POST:
        context['next'] = request.GET.get('next', '')
        try:
            context['title'] = request.POST['title']
            context['place'] = int(request.POST['place'])
            context['classe'] = CategoryColor.objects.get(pk=request.POST['color'])
        except ValueError:
            context['errors'].append("Informations manquantes")
        except CategoryColor.DoesNotExist:
            context['errors'].append("Clé primaire de classe inexistante")

        if not len(context['errors']):
            context['category'].title = context['title']
            context['category'].place = context['place']

            # Place
            list_cat = CategoryFile.objects.filter(subject=context['category'].subject).order_by('place')
            place = context['place']
            if 0 < place < len(list_cat) + 1:
                if context['category'].place < place:
                    for i in range(context['category'].place + 1, place + 1):
                        list_cat[i].place -= 1
                        list_cat[i].save()
                else:
                    for i in range(context['category'].place - 1, place + 1, -1):
                        list_cat[i].place += 1
                        list_cat[i].save()
                context['category'].place = int(request.POST['place'])

            context['category'].classe = context['classe']
            context['category'].save()
            context['message'] = "Modifications effectuées"
            return render(request, "static_content/admin/message_template.html", context)

    context['colors'] = CategoryColor.objects.all().exclude(pk=context['category'].classe.pk)
    context['max'] = len(CategoryFile.objects.filter(subject=context['category'].subject))
    return render(request, "static_content/change/change-category.html", context)
