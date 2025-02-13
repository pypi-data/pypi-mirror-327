from django.apps import AppConfig


class SensorsConfig(AppConfig):
    name = "NEMO_sensors"
    label = "sensors"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        """
        This code will be run when Django starts.
        """
        pass
