from decimal import Decimal

from django.db import models
from .utils import get_token_info
from .tasks import import_volumes

class Token(models.Model):
    name = models.CharField(max_length=100, blank=True)
    symbol = models.CharField(max_length=100, blank=True)
    decimals = models.IntegerField(blank=True)
    total_supply = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=50, unique=True)  # contract address
    ico_start_date = models.DateField(null=True, blank=True)
    ico_end_date = models.DateField(null=True, blank=True)
    is_scum = models.BooleanField(default=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        info = get_token_info(self.address)
        if not self.name:
            self.name = info.get("name", self.address)

        if not self.symbol:
            self.symbol =  info.get("symbol", "Symbol")

        if not self.decimals:
            decimals = info.get("decimals", "18")
            self.decimals = int(decimals)
        if not self.total_supply:
            totalSupply = info.get("totalSupply", "100000000")
            self.total_supply = str(totalSupply)
        super(Token, self).save(*args, **kwargs)
        import_volumes.delay(self.id, self.address)


class Volume(models.Model):
    type = models.CharField(max_length=30)
    date = models.DateTimeField()
    volume = models.DecimalField(max_digits=40, decimal_places=2)
    token = models.ForeignKey(Token, related_name="volumes", on_delete=models.CASCADE)

    class Meta:
        index_together = [
            ["date", "token"],
        ]