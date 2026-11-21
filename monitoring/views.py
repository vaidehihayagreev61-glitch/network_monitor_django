import platform
import subprocess
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import NetworkDeviceForm
from .models import MonitoringRecord, NetworkDevice


@login_required
def dashboard(request):
    devices = NetworkDevice.objects.all()
    context = {
        "devices": devices[:8],
        "total": devices.count(),
        "online": devices.filter(status="Online").count(),
        "offline": devices.filter(status="Offline").count(),
        "unknown": devices.filter(status="Unknown").count(),
    }
    return render(request, "monitoring/dashboard.html", context)


@login_required
def device_list(request):
    return render(request, "monitoring/device_list.html", {
        "devices": NetworkDevice.objects.all()
    })


@login_required
def device_create(request):
    form = NetworkDeviceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Device added successfully.")
        return redirect("device_list")
    return render(request, "monitoring/device_form.html", {
        "form": form, "page_title": "Add device"
    })


@login_required
def device_update(request, pk):
    device = get_object_or_404(NetworkDevice, pk=pk)
    form = NetworkDeviceForm(request.POST or None, instance=device)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Device details updated.")
        return redirect("device_list")
    return render(request, "monitoring/device_form.html", {
        "form": form, "page_title": "Edit device"
    })


@login_required
def device_delete(request, pk):
    device = get_object_or_404(NetworkDevice, pk=pk)
    if request.method == "POST":
        device.delete()
        messages.success(request, "Device deleted.")
        return redirect("device_list")
    return render(request, "monitoring/device_confirm_delete.html", {"device": device})


@login_required
def check_device(request, pk):
    if request.method != "POST":
        return redirect("device_list")

    device = get_object_or_404(NetworkDevice, pk=pk)
    # One ping to one explicitly saved device. No shell is used.
    flag = "-n" if platform.system().lower() == "windows" else "-c"
    start = time.monotonic()
    try:
        result = subprocess.run(
            ["ping", flag, "1", str(device.ip_address)],
            capture_output=True,
            text=True,
            timeout=4,
            check=False,
        )
        elapsed_ms = round((time.monotonic() - start) * 1000, 2)
        if result.returncode == 0:
            device.status = "Online"
            device.response_time = elapsed_ms
            messages.success(request, f"{device.device_name} is reachable ({elapsed_ms} ms).")
        else:
            device.status = "Offline"
            device.response_time = 0
            messages.warning(request, f"{device.device_name} did not respond to ping.")
    except (OSError, subprocess.TimeoutExpired):
        device.status = "Offline"
        device.response_time = 0
        messages.warning(request, "Ping could not be completed. Check that the ping utility is available.")

    device.last_checked = timezone.now()
    device.save()
    MonitoringRecord.objects.create(
        device=device,
        status=device.status,
        response_time=device.response_time,
    )
    return redirect("device_list")


@login_required
def reports(request):
    records = MonitoringRecord.objects.select_related("device")[:100]
    recent = list(reversed(records))
    return render(request, "monitoring/reports.html", {
        "records": records,
        "chart_labels": [r.checked_at.strftime("%d %b %H:%M") for r in recent],
        "chart_values": [r.response_time for r in recent],
    })
