from flask import Flask, jsonify
import os
import shutil

app = Flask(__name__)

def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return round(int(f.read()) / 1000, 1)

def get_cpu_load():
    load1, _, _ = os.getloadavg()
    return round(load1, 2)

def get_ram():
    with open("/proc/meminfo") as f:
        meminfo = f.read()

    total = int([x for x in meminfo.splitlines() if "MemTotal" in x][0].split()[1])
    available = int([x for x in meminfo.splitlines() if "MemAvailable" in x][0].split()[1])

    used = total - available
    return {
        "used": round(used / 1024, 1),
        "total": round(total / 1024, 1)
    }

def get_disk():
    total, used, _ = shutil.disk_usage("/host")
    return {
        "used": round(used / (1024**3), 1),
        "total": round(total / (1024**3), 1)
    }

@app.route("/dashboard")
def stats():
    return jsonify({
        "temperature": get_cpu_temp(),
        "cpu_load": get_cpu_load(),
        "ram": get_ram(),
        "disk": get_disk()
    })

app.run(host="0.0.0.0", port=5000)

