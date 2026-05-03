from django.utils import timezone

# Génère un code unique basé sur la date actuelle (année et mois)
def generate_monthly_code_now(prefix, model_class):
    """
    Génère un code du type PREFIX-YYYY-MM-XXX
    basé uniquement sur la date actuelle (timezone.now()),
    sans utiliser un champ du modèle.
    """

    now = timezone.now()
    year = now.year
    month = f"{now.month:02d}"

    # Filtrer toutes les entrées créées la même année/mois (selon maintenant)
    filters = {
        "code_demande__startswith": f"{prefix}-{year}-{month}-"
    }

    count = model_class.objects.filter(**filters).count() + 1
    compteur = f"{count:03d}"

    return f"{prefix}-{year}-{month}-{compteur}"



#Exemple d'utilisation dans un modèle Django :
#from utils.code_generator import generate_monthly_code
"""
    def save(self, *args, **kwargs):
        if not self.code_demande:
            self.code_demande = generate_monthly_code(
                prefix="DEM",
                model_class=Demande
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_demande
"""

# Variante plus générique utilisant un champ date spécifié
def generate_monthly_code(prefix, model_class, date_field="date_creation"):
    """
    Génère un code du type : PREFIX-YYYY-MM-XXX
    Réutilisable pour n’importe quel modèle.
    """

    now = timezone.now()
    year = now.year
    month = f"{now.month:02d}"

    filters = {
        f"{date_field}__year": year,
        f"{date_field}__month": now.month,
    }

    # Compte les enregistrements du même mois
    count = model_class.objects.filter(**filters).count() + 1
    compteur = f"{count:03d}"

    return f"{prefix}-{year}-{month}-{compteur}"

# Exemple d'utilisation dans un modèle Django :
# from utils.code_generator import generate_monthly_code
"""
class Demande(models.Model):
    code_demande = models.CharField(max_length=50, unique=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    # autres champs...

    def save(self, *args, **kwargs):
        if not self.code_demande:
            self.code_demande = generate_monthly_code(
                prefix="DEM",
                model_class=Demande,
                date_field="date_creation" # champ date à utiliser
            )
        super().save(*args, **kwargs)
    def __str__(self):
        return self.code_demande
"""   


# Variante avec un type de code (ex: Demandeur, Gestionnaire)
def generate_code_now(prefix, type_code, model_class, type_field_name="type_demande"):
    now = timezone.now()
    year = now.year
    month = f"{now.month:02d}"

    # Nombre d'enregistrements ayant même type/mois/année
    filters = {
        type_field_name: type_code,
        "date_demande__year": year,
        "date_demande__month": now.month
    }

    count = model_class.objects.filter(**filters).count() + 1
    compteur = f"{count:03d}"

    return f"{prefix}-{type_code}-{year}-{month}-{compteur}"





def generate_code(prefix, type_code, model_class, type_field_name="type_demande", date_field="date_demande"):
    now = timezone.now()
    year = now.year
    month = f"{now.month:02d}"

    # Nombre d'enregistrements ayant même type/mois/année
    filters = {
        type_field_name: type_code,
        f"{date_field}__year": year,
        f"{date_field}__month": now.month,
    }

    count = model_class.objects.filter(**filters).count() + 1
    compteur = f"{count:03d}"

    return f"{prefix}-{type_code}-{year}-{month}-{compteur}"









