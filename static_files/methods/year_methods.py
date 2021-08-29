from static_files.models import YearFile, SemesterFile, SubjectFile, School
from static_files.methods.subject_methods import CreateSubject

# Liste matières
list_prepa = ['Mathématiques', 'Algorithmiques', 'Physique', 'Electronique',
              'Architecture', 'Sciences Humaines', 'QCM']

# Liste matière S5
list_maths_s5 = ['']

# Liste électifs S6
list_maif = ['FMSI : Fondements Mathématiques pour la sécurité informatique',
              'PROL : Programmation Linéaire',
              'ASPI : Analyse Asymptotique pour la Physique',
              'CODO : Compression de données',
              'LOFO : Logique Formelle',
              'LOGI2 : Logique du premier ordre',
              'ODEE : Equation Différentielles pour l\'Ingénieur',
              'FMSI_E : Base Mathématiques pour la sécurité',
              'QUI : Quantum Initiation']
list_maths_s6 = ['ASE1 : Analyse Statistique',
                 'CAMA : Calcul Matriciel',
                 'FPVA : Fonction à plusieurs variables',
                 'MAFI : Bases Mathématiques pour les métiers de la finance',
                 'OPEL : Optimisation Elémentaire',
                 'PROC : Probabilités Continues']
list_prog_s6 = ['CMP1 : Construction des compilateurs niveau -1',
                'CMP2 : Construction des compilateurs niveau -2',
                'ERO1 : Elements de Recherches Opérationnelle',
                'THEG : Théorie des Graphes',
                'TYLA : Typologie des Langages']
list_net_s6 = ['IDVO : Initiation DEVOPS',
               'NET2 : Eléments Réseaux 2',
               'SEDE : Sécurité du Développement',
               'TRSE : Télécom, Réseaux et Services']
list_glsr_s6 = ['PRPA : Programmation Parallèle',
                'PTON : Python, fondements & langage',
                'RESE : Réseaux et Sécurité',
                'RXAN : Réseaux LAN et MAN',
                'SEDE2 : Sécurité du développement 2',
                '3DU1 : Débuter la 3D avec Unity',
                'CPPA : Langage C++ avancé',
                'IANDO : Initiation plateforme ANDROID',
                'IDOT : Environnement DotNet et langage C#',
                'IIOS : Initiation iOS',
                'IJST : JavaScript ReactJS',
                'INIA : Techniques de Machine Learning et d\'Intelligence Artificielle'
                'JANGU : Javascript Angular',
                'MOB2 : Modelisation Objet 2',
                'SCALAIN : Initiation au langage SCALA',
                'SOCRA : Software craftmanship']


# Year obj, semester obj
def create_base_subject(year, semester):
    context = {}
    # Prepa
    if semester.semester < 5:
        list_subject = ['Mathématiques', 'Algorithmiques', 'Physique', 'Electronique',
                        'Architecture', 'Sciences Humaines', 'QCM']
        for subject in list_subject:
            if not len(SubjectFile.objects.filter(year=year.year, semester=semester.semester, subject=subject)):
                CreateSubject(context, subject, semester.pk, year.pk, School.objects.get(school__exact="EPITA"))

    elif semester.semester == 5:
        list_subject = ['Complexité', 'Réseaux', 'Système', 'THL', 'Mathématiques']
        for subject in list_subject:
            if not len(SubjectFile.objects.filter(year=year.year, semester=semester.semester, subject=subject)):
                CreateSubject(context, subject, semester.pk, year.pk, School.objects.get(school__exact="EPITA"))

    elif semester.semester == 6:
        # Electifs
        if not len(SubjectFile.objects.filter(year=year.year, semester=semester.semester, subject="MAIF")):
            CreateSubject(context, "MAIF", semester, year, School.objects.get(school__exact="EPITA"))

        list_subject = ['Mathématiques', 'Réseaux', 'Sécurité', 'Programmation', 'Entreprise']
        for subject in list_subject:
            if not len(SubjectFile.objects.filter(year=year.year, semester=semester.semester, subject=subject)):
                CreateSubject(context, subject, semester.pk, year.pk, School.objects.get(school__exact="EPITA"))


# year(int), semester(pk)
def create_year(year, semester):
    semester_obj = SemesterFile.objects.get(pk=semester)
    new_year = YearFile(year=year, active_semester=semester_obj)
    create_base_subject(new_year, semester_obj)
    new_year.save()


def get_year(year):
    test_y = YearFile.objects.filter(year__exact=year)
    if len(test_y):
        return test_y[0]
    return None


# year(year, semester, school)
def set_year(year, semester, school):
    if not year or not semester or not school:
        return 1
    year_obj = YearFile.objects.filter(year__exact=year, school__exact=school)
    year_obj.active_semester = SemesterFile.objects.get(semester__exact=semester)
    year_obj.save()
    return 0
