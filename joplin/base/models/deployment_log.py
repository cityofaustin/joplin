from django.db import models

# Allows us to add statement information about PR deployment process
class DeploymentLog(models.Model):
    # Name of operation
    operation = models.CharField(
        primary_key=True,
        db_index=True,
        max_length=256,
    )
    # Value used during operation execution
    value = models.CharField(
        blank=True,
        null=True,
        max_length=256,
    )
    # Whether the operation was completed
    completed = models.BooleanField(
        blank=True,
        null=True,
    )
