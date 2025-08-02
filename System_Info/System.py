import psutil
import pygetwindow
import time
def Fetch():
  old = psutil.net_io_counters()
  windows = pygetwindow.getWindowsWithTitle('')
  windows_info = f"""[Current Open windows]:
  """
  mem = psutil.virtual_memory()
  if psutil.sensors_battery():
    battery = psutil.sensors_battery()
    battery = f"{battery.percent}% | Charging: {battery.power_plugged}"
  else:
    battery = "No Battery Detected"
    
  disks = "\n".join(f"- {d.device} ({d.mountpoint}) [{d.fstype}]" for d in psutil.disk_partitions())
  net_info = ""
  for iface, stats in psutil.net_if_stats().items():
      net_info += f"\n- {iface}: {'UP' if stats.isup else 'DOWN'}, Speed: {stats.speed}Mbps"

  for win in windows:
    if win.title:
      windows_info += f"\n{win.title}\n{win.topleft}\n{win.size}\n"
  time.sleep(5)
  new = psutil.net_io_counters()

  download = ((new.bytes_recv - old.bytes_recv) / 1024) * 8 # KB/s
  upload = ((new.bytes_sent - old.bytes_sent) / 1024)  * 8  # KB/s


  with open("Memory/System_info.txt","w",encoding="utf-8") as f:
    f.write(f"""
  [CPU]:{psutil.cpu_percent(interval=2.5)}

  [RAM]: {mem.percent}% used | {round(mem.used / (1024**3), 2)} GB used of {round(mem.total / (1024**3), 2)} GB

  [Battery]: {battery}

  [Disks]: {disks}

  [Internet]:donwload:{download:.2f} KB/s | upload:{upload:.2f} KB/s

  [Logged in Users]:{psutil.users()}

  {windows_info}
  """)