import PySimpleGUI as sg
import os
import shutil
import tempfile
import ctypes
from pathlib import Path
import psutil
import subprocess
import queue
from send2trash import send2trash

texts = {
    'en': {
        'title': 'System Cleaner',
        'temp': 'Clean Temp Files',
        'recycle_bin': 'Empty Recycle Bin',
        'prefetch': 'Clean Prefetch Files',
        'recent': 'Clean Recent Files',
        'windows_logs': 'Clean Windows Update Logs',
        'thumbnail_cache': 'Clean Thumbnail Cache',
        'check_drivers': 'Check Drivers',
        'update_performance': 'Update Windows Performance',
        'check_disk': 'Check Disk Usage',
        'clean_registry': 'Clean Registry',
        'clear_dns': 'Clear DNS Cache',
        'check_processes': 'Check Running Processes',
        'browser_cache': 'Clean Browser Cache',
        'app_logs': 'Clean App Logs',
        'backup_files': 'Clean Backup Files',
        'installer_files': 'Clean Installer Files',
        'start_cleaning': 'Start Cleaning',
        'language': 'Language'
    },
    'id': {
        'title': 'Pembersih Sistem',
        'temp': 'Bersihkan File Temp',
        'recycle_bin': 'Kosongkan Recycle Bin',
        'prefetch': 'Bersihkan File Prefetch',
        'recent': 'Bersihkan File Terbaru',
        'windows_logs': 'Bersihkan Log Pembaruan Windows',
        'thumbnail_cache': 'Bersihkan Cache Thumbnail',
        'check_drivers': 'Periksa Driver',
        'update_performance': 'Perbarui Performa Windows',
        'check_disk': 'Periksa Penggunaan Disk',
        'clean_registry': 'Bersihkan Registry',
        'clear_dns': 'Kosongkan Cache DNS',
        'check_processes': 'Periksa Proses yang Berjalan',
        'browser_cache': 'Bersihkan Cache Browser',
        'app_logs': 'Bersihkan Log Aplikasi',
        'backup_files': 'Bersihkan File Backup',
        'installer_files': 'Bersihkan File Installer',
        'start_cleaning': 'Mulai Pembersihan',
        'language': 'Bahasa'
    }
}
def check_disk_usage():
    disk = psutil.disk_usage('/')
    return f"Disk Usage: {disk.percent}%"
def clean_temp():
    temp_dirs = [
        Path(os.environ['TEMP']),
        Path('C:/Windows/Temp')
    ]
    for temp_dir in temp_dirs:
        if temp_dir.exists() and temp_dir.is_dir():
            for item in temp_dir.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    print(f"Failed to delete {item}: {e}")

def clean_recycle_bin():
    try:
        for root, dirs, files in os.walk("C:/$Recycle.Bin"):
            for file in files:
                try:
                    send2trash(os.path.join(root, file))
                except Exception as e:
                    print(f"Failed to delete {file}: {e}")
    except Exception as e:
        print(f"Error cleaning Recycle Bin: {e}")

def clean_prefetch():
    prefetch_dir = Path('C:/Windows/Prefetch')
    if prefetch_dir.exists() and prefetch_dir.is_dir():
        for item in prefetch_dir.iterdir():
            try:
                if item.is_file():
                    item.unlink()  # Remove file
            except Exception as e:
                print(f"Failed to delete {item}: {e}")

def clean_recent():
    recent_dir = Path(os.path.expanduser('~')) / 'Recent'
    if recent_dir.exists() and recent_dir.is_dir():
        for item in recent_dir.iterdir():
            try:
                item.unlink()  # Remove file
            except Exception as e:
                print(f"Failed to delete {item}: {e}")

def clean_windows_logs():
    windows_logs_dir = Path('C:/Windows/Logs')
    if windows_logs_dir.exists() and windows_logs_dir.is_dir():
        for item in windows_logs_dir.iterdir():
            try:
                if item.is_file():
                    item.unlink()  # Remove file
                elif item.is_dir():
                    shutil.rmtree(item)  # Remove directory
            except Exception as e:
                print(f"Failed to delete {item}: {e}")

def clean_thumbnail_cache():
    thumbnail_cache_dir = Path('C:/Users') / Path(os.getenv('USERNAME')) / 'AppData/Local/Microsoft/Windows/Explorer'
    if thumbnail_cache_dir.exists() and thumbnail_cache_dir.is_dir():
        for item in thumbnail_cache_dir.iterdir():
            try:
                if item.is_file():
                    item.unlink()  # Remove file
            except Exception as e:
                print(f"Failed to delete {item}: {e}")

def clean_registry():
    try:
        subprocess.run("reg delete HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs /f", shell=True)
        print("Registry cleaned.")
    except Exception as e:
        print(f"Failed to clean registry: {e}")

def clear_dns_cache():
    try:
        subprocess.run("ipconfig /flushdns", shell=True)
        print("DNS cache cleared.")
    except Exception as e:
        print(f"Failed to clear DNS cache: {e}")

def check_drivers():
    try:
        result = subprocess.run("driverquery", capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            drivers = result.stdout
            print("Drivers List: ")
            print(drivers)
        else:
            print("Failed to retrieve drivers information.")
    except Exception as e:
        print(f"Failed to check drivers: {e}")
        
                    
def clean_browser_cache():
    browsers = [
        Path(os.environ['LOCALAPPDATA']) / 'Google/Chrome/User Data/Default/Cache',
        Path(os.environ['APPDATA']) / 'Mozilla/Firefox/Profiles',
        Path(os.environ['LOCALAPPDATA']) / 'Microsoft/Edge/User Data/Default/Cache'
    ]
    
    for browser in browsers:
        if browser.exists() and browser.is_dir():
            for item in browser.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    print(f"Failed to delete {item}: {e}")

def clean_app_logs():
    app_logs_dir = Path("C:/ProgramData/")
    for item in app_logs_dir.iterdir():
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            print(f"Failed to delete {item}: {e}")

def clean_backup_files():
    backup_dir = Path("C:/Windows/Backups")
    for item in backup_dir.iterdir():
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            print(f"Failed to delete {item}: {e}")

def clean_installer_files():
    installer_dir = Path("C:/Windows/Installer")
    for item in installer_dir.iterdir():
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            print(f"Failed to delete {item}: {e}")

def create_layout(language):
    lang_text = texts[language]
    layout = [
        [sg.Text(lang_text['title'], font=("Helvetica", 16), justification='center')],
        [sg.Text(lang_text['language'], size=(8, 1)), sg.Combo(['English', 'Bahasa Indonesia'], default_value='English', key='language', size=(15, 1))],
        [sg.TabGroup([[
            sg.Tab('Clean System', [
                [sg.Checkbox(lang_text['temp'], key='temp')],
                [sg.Checkbox(lang_text['recycle_bin'], key='recycle_bin')],
                [sg.Checkbox(lang_text['prefetch'], key='prefetch')],
                [sg.Checkbox(lang_text['recent'], key='recent')],
                [sg.Checkbox(lang_text['windows_logs'], key='windows_logs')],
                [sg.Checkbox(lang_text['thumbnail_cache'], key='thumbnail_cache')],
                [sg.Checkbox(lang_text['clean_registry'], key='clean_registry')],
                [sg.Checkbox(lang_text['clear_dns'], key='clear_dns')],
                [sg.Checkbox(lang_text['browser_cache'], key='browser_cache')],
                [sg.Checkbox(lang_text['app_logs'], key='app_logs')],
                [sg.Checkbox(lang_text['backup_files'], key='backup_files')],
                [sg.Checkbox(lang_text['installer_files'], key='installer_files')]
            ])],
            [sg.Tab('Advanced', [
                [sg.Button(lang_text['check_drivers'], key='check_drivers')],
                [sg.Button(lang_text['update_performance'], key='update_performance')],
                [sg.Button(lang_text['check_disk'], key='check_disk')],
                [sg.Button(lang_text['check_processes'], key='check_processes')]
            ])]
        ])],
        [sg.Button(lang_text['start_cleaning'], key='start_cleaning', size=(20, 2))],
        [sg.StatusBar('Ready', size=(30, 1), key='status')]
    ]
    return layout

def main():
    language = 'en'
    task_queue = queue.Queue()
    window = sg.Window("System Cleaner", create_layout(language), keep_on_top=True, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if values['language'] == 'Bahasa Indonesia':
            language = 'id'
        else:
            language = 'en'

        window.close()
        window = sg.Window("System Cleaner", create_layout(language), keep_on_top=True, finalize=True)

        if event == 'start_cleaning':
            if values['temp']:
                clean_temp()
            if values['recycle_bin']:
                clean_recycle_bin()
            if values['prefetch']:
                clean_prefetch()
            if values['clean_registry']:
                clean_registry()
            if values['clear_dns']:
                clear_dns_cache()
            if values['browser_cache']:
                clean_browser_cache()
            if values['app_logs']:
                clean_app_logs()
            if values['backup_files']:
                clean_backup_files()
            if values['installer_files']:
                clean_installer_files()
            sg.popup("Cleaning completed!", title="Done", keep_on_top=True)

        if event == 'check_drivers':
            check_drivers()
            sg.popup("Driver check completed!", title="Done", keep_on_top=True)

        if event == 'update_performance':
            update_performance()
            sg.popup("Performance update completed!", title="Done", keep_on_top=True)

        if event == 'check_disk':
            disk_usage = check_disk_usage()
            sg.popup(disk_usage, title="Disk Usage", keep_on_top=True)

        if event == 'check_processes':
            processes = check_running_processes()
            process_list = '\n'.join([f"{p['name']} (PID: {p['pid']}) - CPU: {p['cpu_percent']}% - Memory: {p['memory_percent']}%" for p in processes])
            sg.popup(process_list, title="Running Processes", keep_on_top=True)

    window.close()

if __name__ == "__main__":
    main()
