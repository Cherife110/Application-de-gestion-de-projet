from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, birth_date, id_number, role, password):
        if not first_name:
            raise ValueError('Les utilisateurs doivent avoir un prénom')
        if not last_name:
            raise ValueError('Les utilisateurs doivent avoir un nom de famille')
        if not birth_date:
            raise ValueError('Les utilisateurs doivent avoir une date de naissance')
        if not id_number:
            raise ValueError('Les utilisateurs doivent avoir un numéro d\'identification')
        if not role:
            raise ValueError('Les utilisateurs doivent avoir un rôle')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            id_number=id_number,
            role=role,
        )
        # Hash the password before saving it to database
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name , id_number,  password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            birth_date="2002-10-01",
            id_number=id_number,
            role=CustomUser.ADMIN,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    #les coordonee admin, 2002-!@#$%^&*
class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    id_number = models.CharField(max_length=30, unique=True)
    #subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    # Rôles
    STUDENT = 1
    TEACHER = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (STUDENT, 'Etudiant'),
        (TEACHER, 'Enseignant'),
        (ADMIN, 'Administrateur'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# Modèle pour représenter une matière
class Subject(models.Model):
    name = models.CharField(max_length=100) # Nom de la matière
    code = models.CharField(max_length=10) # Code de la matière

    def __str__(self):
        return self.name

# Modèle pour représenter un projet/devoir
class Project(models.Model):
    # Statuts possibles pour un projet/devoir
    STATUS_CHOICES = (
        ('EN', 'En cours'), # Le projet/devoir est en cours de réalisation
        ('SO', 'Soumis'), # Le projet/devoir a été soumis par l'étudiant
        ('CO', 'Corrigé'), # Le projet/devoir a été corrigé par l'instructeur
        ('TR', 'Traité'), # Le projet/devoir a été traité par l'instructeur
        ('AR', 'Archivé'), # Le projet/devoir a été archivé par l'instructeur
    )

    title = models.CharField(max_length=200) # Intitulé du projet/devoir
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE) # Matière liée au projet/devoir
    file = models.FileField(upload_to='media/') # Fichier contenant le projet/devoir
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='EN') # Statut du projet/devoir
    feedback = models.TextField(blank=True) # Avis/notes donnés par l'instructeur

    def __str__(self):
        return self.title

# Modèle pour représenter un projet/devoir précédent
class PreviousProject(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE) # Le projet/devoir précédent est lié à un projet/devoir du module de chargement/téléchargement
    summary = models.TextField() # Le résumé du projet/devoir précédent
    archived = models.BooleanField(default=False) # Le statut d'archivage du projet/devoir précédent

    def __str__(self):
        return self.project.title
