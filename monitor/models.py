from django.db import models


class Token(models.Model):
    name = models.CharField(max_length=100, blank=True)
    contract = models.CharField(max_length=50, unique=True)  # contract address
    ico_start_date = models.DateField(null=True, blank=True)
    ico_end_date = models.DateField(null=True, blank=True)
    is_scum = models.BooleanField(default=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.contract
        super(Token, self).save(*args, **kwargs)
