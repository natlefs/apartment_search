from django.db import models
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    """lat/lon global position"""
    latitude: models.FloatField()
    longitude = models.FloatField()


class Housing(models.Model):
    """Describes a unit of housing"""

    class HousingModel(models.TextChoices):
        """The type of unit"""
        APARTMENT = 'LE', _('Leilighet')
        SINGLE_OWNER = 'EB', _('Enebolig')
        CO_OWNED = 'TB', _('Tomannsbolig')

    class OwnershipModel(models.TextChoices):
        """The form of ownership over the unit"""
        OWNER = 'SE', _('Eier (Selveier)')
        COOPERATIVE = 'AN', _('Andel')
        COOPERATIVE_SHARE = 'AK', _('Aksje')

    class EnergyRatingLetter(models.TextChoices):
        """How energy effective is the unit"""
        # https://www.energimerking.no/no/energimerking-bygg/kjopeleie-bolig1/hva-betyr-energimerket-for-meg/
        A = 'A', _('Veldig energieffektiv')
        B = 'B', _('Ganske energieffektiv')
        C = 'C', _('Moderat energieffektiv')
        D = 'D', _('Mindre energieffektiv')
        E = 'E', _('Veldig lite energieffektiv')
        F = 'F', _('Ikke energieffektiv')

    class EnergyRatingColor(models.TextChoices):
        """How clean is the energy used to heat the unit"""
        # https://www.energimerking.no/no/energimerking-bygg/kjopeleie-bolig1/hva-betyr-energimerket-for-meg/
        RED = 'RE', _('Rød')
        ORANGE = 'OR', _('Oransje')
        YELLOW = 'YE', _('Gul')
        LIGHT_GREEN = 'LG', _('Lysegrønn')
        DARK_GREEN = 'DG', _('Mørkegrønn')

    # Metadata
    reference = models.TextField() # for instance finn_code
    picture_count = models.IntegerField()
    description_wordcount = models.IntegerField()
    location = models.OneToOneField(Location, models.CASCADE, primary_key=True)

    # Monetary
    valuation = models.IntegerField()
    total_price = models.IntegerField()
    sale_related_costs = models.IntegerField()
    common_debt = models.IntegerField(default=0)
    common_fortune = models.IntegerField(default=0)
    monthly_cost = models.IntegerField(default=0)

    # Ownership
    housing_model = models.CharField(choices=HousingModel.choices)
    ownership_model = models.CharField(choices=OwnershipModel.choices)
    year_built = models.IntegerField()

    # Space
    bedrooms = models.IntegerField()
    rooms = models.IntegerField()
    living_space = models.IntegerField()
    square_footage = models.IntegerField()
    facilities = models.ForeignKey(to, on_delete)

    # Energy
    energy_letter = models.CharField(choices=EnergyRatingLetter.choices)
    energy_color = models.CharField(choices=EnergyRatingColor.choices)


class Facilities(models.Model):
    """A facility offered in a unit of housing"""
    description = models.TextField()
    housing_unit = models.ForeignKey(Housing, on_delete=models.CASCADE)

    class Meta:
        orderding = ['description']


class SearchParameters(models.Model):
    location = models.OneToOneField(Location, models.CASCADE, primary_key=True)
    search_radius = models.IntegerField()
    max_monthly_cost = models.IntegerField()
    max_total_price = models.IntegerField()
    min_bedrooms = models.IntegerField()

    def to_url(self):
        return (
            'https://www.finn.no/realestate/homes/search.html'
            f'?lat={self.location.latitude}&lon={self.location.longitude}&radius={self.radius}'
            f'&no_of_bedrooms={1}&price_collective_to={self.total_price}'
            f'&rent_to={self.max_monthly_cost}'
            '&sort=PUBLISHED_DESC'
        )
