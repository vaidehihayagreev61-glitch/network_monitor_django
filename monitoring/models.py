from django.db import models


class NetworkDevice(models.Model):
    DEVICE_TYPES = [
        ("Computer", "Computer"),
        ("Server", "Server"),
        ("Router", "Router"),
        ("Printer", "Printer"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Unknown", "Unknown"),
        ("Online", "Online"),
        ("Offline", "Offline"),
    ]

    device_name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(unique=True)
    device_type = models.CharField(max_length=30, choices=DEVICE_TYPES, default="Other")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Unknown")
    response_time = models.FloatField(default=0)
    last_checked = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["device_name"]

    def __str__(self):
        return f"{self.device_name} ({self.ip_address})"


class MonitoringRecord(models.Model):
    device = models.ForeignKey(
        NetworkDevice, on_delete=models.CASCADE, related_name="records"
    )
    status = models.CharField(max_length=10, choices=NetworkDevice.STATUS_CHOICES)
    response_time = models.FloatField(default=0)
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-checked_at"]

    def __str__(self):
        return f"{self.device.device_name}: {self.status} at {self.checked_at}"
