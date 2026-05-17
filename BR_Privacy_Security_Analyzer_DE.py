#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BlackRabbitZ Privacy & Security Analyzer
Start: python3 BlackRabbitZ_Privacy_Security_Analyzer_DE.py
Optional: logo.png / BlackRabbitZ.png in denselben Ordner legen.

Dieses Tool ist ein Awareness-/Lern-Tool.
Es scannt keine Geräte, liest keine Daten aus und greift nicht in Systeme ein.
Die Bewertung basiert nur auf den Antworten des Users.
"""

import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except Exception:
    PIL_OK = False

APP_TITLE = "BlackRabbitZ Privacy & Security Analyzer"

COLORS = {
    "bg": "#0b0c0f",
    "panel": "#111216",
    "panel2": "#17181d",
    "card": "#0f1014",
    "border": "#2d3038",
    "red": "#ff2436",
    "red2": "#b61726",
    "green": "#2ee86f",
    "yellow": "#ffcc33",
    "orange": "#ff8a2a",
    "line": "#7f141d",
    "text": "#f1f1f1",
    "muted": "#b9bcc4",
    "soft": "#858a94",
    "select": "#20222a"
}

BASE_FONT = ("Segoe UI", 10)
SMALL_FONT = ("Segoe UI", 9)
TITLE_FONT = ("Segoe UI Semibold", 26)
SUB_FONT = ("Segoe UI Semibold", 13)
QUESTION_FONT = ("Segoe UI Semibold", 10)
MONO_FONT = ("Consolas", 10)


def res_path(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), name)


RADIO_QUESTIONS = [
    ("pc_os", "Welches Betriebssystem nutzt du am PC/Laptop hauptsächlich?", [
        ("windows11", "Windows 11"),
        ("windows10", "Windows 10"),
        ("linux", "Linux"),
        ("macos", "macOS"),
        ("mixed", "Mehrere Systeme"),
    ]),
    ("pc_account", "Wie meldest du dich am PC hauptsächlich an?", [
        ("local_account", "Lokales Konto"),
        ("microsoft_account", "Microsoft-/Online-Konto"),
        ("apple_id", "Apple-ID"),
        ("google_account", "Google-Konto"),
        ("unknown", "Weiß ich nicht"),
    ]),
    ("pc_encryption", "Ist deine Festplatte verschlüsselt?", [
        ("encrypted", "Ja, z.B. BitLocker/FileVault/LUKS"),
        ("not_encrypted", "Nein"),
        ("unknown", "Weiß ich nicht"),
    ]),
    ("pc_updates", "Wie gehst du mit Updates am PC um?", [
        ("auto_updates", "Automatisch / regelmäßig"),
        ("manual_updates", "Manuell, aber regelmäßig"),
        ("rare_updates", "Selten"),
        ("disabled_updates", "Deaktiviert oder stark verzögert"),
    ]),
    ("pc_admin", "Nutzt du im Alltag dauerhaft Adminrechte?", [
        ("standard_user", "Nein, normales Benutzerkonto"),
        ("admin_user", "Ja, meistens Admin"),
        ("unknown", "Weiß ich nicht"),
    ]),
    ("phone_os", "Welches Smartphone nutzt du hauptsächlich?", [
        ("android_google", "Android mit Google-Diensten"),
        ("android_samsung", "Samsung Android"),
        ("android_xiaomi", "Xiaomi/Redmi/POCO Android"),
        ("android_custom", "Custom ROM / de-googled Android"),
        ("iphone", "iPhone / iOS"),
        ("no_phone", "Kein Smartphone"),
    ]),
    ("phone_updates", "Wie aktuell ist dein Smartphone?", [
        ("phone_current", "Aktuelle Sicherheitsupdates"),
        ("phone_somewhat_old", "Einige Monate alt"),
        ("phone_old", "Sehr alt / bekommt keine Updates mehr"),
        ("phone_unknown", "Weiß ich nicht"),
    ]),
    ("phone_lock", "Wie sperrst du dein Smartphone?", [
        ("strong_pin", "Starker PIN/Passcode"),
        ("biometric_pin", "Fingerabdruck/FaceID plus PIN"),
        ("weak_pin", "Kurzer PIN/Muster"),
        ("no_lock", "Gar keine Sperre"),
    ]),
    ("phone_location", "Wie nutzt du Standortdienste am Handy?", [
        ("location_strict", "Nur wenn nötig"),
        ("location_mixed", "Für einige Apps dauerhaft"),
        ("location_always", "Meistens dauerhaft aktiv"),
        ("location_unknown", "Weiß ich nicht"),
    ]),
    ("browser", "Welchen Browser nutzt du hauptsächlich?", [
        ("librewolf", "LibreWolf / gehärteter Firefox"),
        ("firefox", "Firefox"),
        ("brave", "Brave"),
        ("chrome", "Google Chrome"),
        ("edge", "Microsoft Edge"),
        ("safari", "Safari"),
        ("other_browser", "Anderer Browser"),
    ]),
    ("browser_extensions", "Nutzt du Schutz-Erweiterungen im Browser?", [
        ("ublock", "uBlock Origin / guter Adblocker"),
        ("some_extensions", "Ein paar Erweiterungen"),
        ("no_extensions", "Nein"),
        ("too_many_extensions", "Sehr viele Erweiterungen"),
    ]),
    ("passwords", "Wie verwaltest du Passwörter?", [
        ("password_manager", "Passwortmanager wie Bitwarden/KeePassXC/1Password"),
        ("browser_passwords", "Im Browser gespeichert"),
        ("reused_passwords", "Viele gleiche/ähnliche Passwörter"),
        ("notes_passwords", "Notizen, Screenshots oder Textdateien"),
    ]),
    ("twofa", "Nutzt du Zwei-Faktor-Authentifizierung?", [
        ("twofa_all", "Ja, bei wichtigen Konten"),
        ("twofa_some", "Nur teilweise"),
        ("twofa_sms", "Ja, aber hauptsächlich per SMS"),
        ("twofa_none", "Nein"),
    ]),
    ("cloud", "Wie stark nutzt du Cloud-Sync?", [
        ("cloud_minimal", "Kaum / bewusst eingeschränkt"),
        ("cloud_normal", "Normal für Fotos/Dokumente"),
        ("cloud_heavy", "Sehr viel, fast alles synchronisiert"),
        ("cloud_unknown", "Weiß ich nicht"),
    ]),
    ("messenger", "Welchen Messenger nutzt du am meisten?", [
        ("signal", "Signal"),
        ("threema", "Threema"),
        ("whatsapp", "WhatsApp"),
        ("telegram", "Telegram"),
        ("discord", "Discord"),
        ("mixed_messenger", "Mehrere"),
    ]),
    ("social_media", "Wie nutzt du Social Media?", [
        ("social_low", "Wenig / bewusst"),
        ("social_normal", "Normal"),
        ("social_heavy", "Sehr viel"),
        ("social_public", "Sehr viel und öffentlich"),
    ]),
    ("network", "Wie schützt du dein Netzwerk?", [
        ("secure_wifi", "WPA2/WPA3, starkes Passwort"),
        ("default_router", "Router fast auf Werkseinstellungen"),
        ("open_wifi", "Offenes/unsicheres WLAN"),
        ("unknown", "Weiß ich nicht"),
    ]),
    ("public_wifi", "Nutzt du öffentliche WLANs?", [
        ("public_wifi_never", "Selten / nie"),
        ("public_wifi_sometimes", "Manchmal"),
        ("public_wifi_often", "Oft"),
        ("public_wifi_sensitive", "Oft auch für Banking/Logins"),
    ]),
    ("vpn_tor", "Nutzt du VPN oder Tor?", [
        ("none", "Nein"),
        ("vpn", "VPN"),
        ("tor", "Tor Browser"),
        ("both", "VPN und Tor, je nach Zweck"),
        ("not_sure", "Weiß nicht genau, was das bringt"),
    ]),
    ("downloads", "Wie gehst du mit Downloads/Links um?", [
        ("careful", "Vorsichtig, nur vertrauenswürdige Quellen"),
        ("normal", "Normal, manchmal unbekannte Quellen"),
        ("risky", "Cracks, dubiose Downloads oder fremde Dateien"),
        ("very_risky", "Ich klicke/öffne fast alles"),
    ]),
    ("goal", "Was ist dein Hauptziel?", [
        ("goal_security", "Mehr Sicherheit"),
        ("goal_privacy", "Mehr Privatsphäre"),
        ("goal_anonymity", "Mehr Anonymität"),
        ("goal_learn", "Erstmal verstehen, was unsicher ist"),
        ("goal_all", "Alles verbessern"),
    ]),
]

CHECK_QUESTIONS = [
    ("pc_settings", "PC-Einstellungen: Was trifft zu?", [
        ("telemetry_reduced", "Telemetrie/Diagnosedaten reduziert"),
        ("firewall_enabled", "Firewall aktiv"),
        ("secure_boot", "Secure Boot/TPM bewusst genutzt"),
        ("autostart_clean", "Autostart aufgeräumt"),
        ("backup_pc", "Regelmäßige Backups"),
        ("full_disk_encryption", "Vollverschlüsselung aktiv"),
    ]),
    ("phone_settings", "Handy-Einstellungen: Was trifft zu?", [
        ("app_permissions_checked", "App-Berechtigungen geprüft"),
        ("ad_id_reset", "Werbe-ID deaktiviert/zurückgesetzt"),
        ("app_tracking_off", "App-Tracking eingeschränkt"),
        ("unknown_sources_off", "Unbekannte Quellen/APK-Installation deaktiviert"),
        ("bluetooth_off", "Bluetooth/NFC nur bei Bedarf"),
        ("backup_phone", "Backup bewusst eingerichtet"),
    ]),
    ("apps", "Welche Apps/Dienste nutzt du viel?", [
        ("google_services", "Google-Dienste"),
        ("meta_services", "WhatsApp/Instagram/Facebook"),
        ("tiktok", "TikTok"),
        ("discord_app", "Discord"),
        ("cloud_photos", "Google Fotos/iCloud Fotos"),
        ("banking_phone", "Banking am Handy"),
    ]),
    ("privacy_tools", "Welche Schutzmaßnahmen nutzt du bereits?", [
        ("dns_blocker", "DNS-Blocker / Pi-hole / NextDNS / AdGuard DNS"),
        ("email_alias", "E-Mail-Aliase"),
        ("separate_accounts", "Getrennte Accounts für verschiedene Zwecke"),
        ("encrypted_messenger", "Ende-zu-Ende-verschlüsselte Messenger"),
        ("hardware_keys", "Security Keys / FIDO2 / YubiKey"),
        ("encrypted_backups", "Verschlüsselte Backups"),
    ]),
]

# Punkte: positiv erhöht Score, negativ senkt Score.
SCORES = {
    "encrypted": (8, 7, 2),
    "not_encrypted": (-12, -10, -2),
    "auto_updates": (10, 6, 0),
    "manual_updates": (7, 4, 0),
    "rare_updates": (-8, -4, 0),
    "disabled_updates": (-15, -8, 0),
    "standard_user": (8, 3, 0),
    "admin_user": (-8, -2, 0),
    "phone_current": (10, 5, 0),
    "phone_somewhat_old": (2, 0, 0),
    "phone_old": (-15, -8, 0),
    "strong_pin": (10, 5, 0),
    "biometric_pin": (8, 4, 0),
    "weak_pin": (-7, -3, 0),
    "no_lock": (-20, -8, 0),
    "location_strict": (4, 10, 2),
    "location_mixed": (1, -3, 0),
    "location_always": (-4, -12, -5),
    "librewolf": (8, 12, 5),
    "firefox": (6, 7, 2),
    "brave": (5, 6, 2),
    "chrome": (1, -10, -3),
    "edge": (1, -8, -3),
    "ublock": (8, 10, 2),
    "no_extensions": (-3, -7, -2),
    "too_many_extensions": (-7, -8, -2),
    "password_manager": (15, 6, 0),
    "browser_passwords": (2, -2, 0),
    "reused_passwords": (-20, -8, 0),
    "notes_passwords": (-16, -6, 0),
    "twofa_all": (15, 4, 0),
    "twofa_some": (5, 1, 0),
    "twofa_sms": (3, -1, 0),
    "twofa_none": (-18, -4, 0),
    "cloud_minimal": (3, 8, 2),
    "cloud_normal": (1, -2, 0),
    "cloud_heavy": (-3, -12, -4),
    "signal": (8, 10, 3),
    "threema": (8, 10, 3),
    "whatsapp": (2, -8, -4),
    "telegram": (1, -4, -3),
    "discord": (1, -6, -3),
    "social_low": (4, 8, 2),
    "social_heavy": (-4, -10, -4),
    "social_public": (-7, -15, -6),
    "secure_wifi": (8, 3, 0),
    "default_router": (-4, -2, 0),
    "open_wifi": (-18, -8, -2),
    "public_wifi_never": (3, 2, 0),
    "public_wifi_often": (-5, -4, -2),
    "public_wifi_sensitive": (-15, -8, -4),
    "vpn": (2, 2, 1),
    "tor": (2, 5, 12),
    "both": (3, 6, 10),
    "careful": (8, 5, 0),
    "risky": (-15, -6, -2),
    "very_risky": (-25, -10, -4),
    "android_custom": (5, 12, 4),
    "android_google": (2, -7, -3),
    "android_samsung": (2, -5, -2),
    "android_xiaomi": (1, -8, -3),
    "iphone": (6, 0, -1),
    "microsoft_account": (0, -5, -1),
    "local_account": (3, 5, 1),
    "windows11": (3, -4, -1),
    "windows10": (-2, -4, -1),
    "linux": (5, 5, 2),
    "macos": (5, 0, -1),
}

CHECK_SCORES = {
    "telemetry_reduced": (2, 8, 2),
    "firewall_enabled": (8, 2, 0),
    "secure_boot": (5, 1, 0),
    "autostart_clean": (4, 3, 0),
    "backup_pc": (10, 4, 0),
    "full_disk_encryption": (8, 8, 2),
    "app_permissions_checked": (6, 10, 2),
    "ad_id_reset": (2, 8, 2),
    "app_tracking_off": (4, 10, 3),
    "unknown_sources_off": (8, 3, 0),
    "bluetooth_off": (3, 4, 1),
    "backup_phone": (8, 3, 0),
    "google_services": (0, -8, -3),
    "meta_services": (0, -10, -4),
    "tiktok": (-2, -12, -4),
    "discord_app": (0, -6, -3),
    "cloud_photos": (0, -8, -2),
    "banking_phone": (0, -2, 0),
    "dns_blocker": (4, 9, 2),
    "email_alias": (2, 9, 3),
    "separate_accounts": (5, 10, 5),
    "encrypted_messenger": (5, 10, 3),
    "hardware_keys": (14, 4, 0),
    "encrypted_backups": (10, 8, 1),
}

WARNINGS = {
    "not_encrypted": "Deine Daten sind bei Diebstahl oder Verlust deutlich leichter auslesbar.",
    "disabled_updates": "Deaktivierte Updates lassen bekannte Sicherheitslücken offen.",
    "phone_old": "Ein Handy ohne Sicherheitsupdates ist ein hohes Risiko für Alltag, Banking und private Daten.",
    "no_lock": "Ohne Gerätesperre sind private Daten sofort zugänglich, wenn das Gerät verloren geht.",
    "location_always": "Dauerhaft aktiver Standort erzeugt Bewegungsprofile.",
    "reused_passwords": "Wiederverwendete Passwörter sind einer der größten Account-Risiken.",
    "twofa_none": "Ohne 2FA reicht oft ein geleaktes Passwort für Account-Übernahmen.",
    "cloud_heavy": "Starker Cloud-Sync ist bequem, erhöht aber Datenkonzentration und Tracking-Abhängigkeit.",
    "open_wifi": "Offenes WLAN ist unsicher und kann Missbrauch oder Mitlesen begünstigen.",
    "public_wifi_sensitive": "Banking und wichtige Logins in öffentlichen WLANs sind besonders riskant.",
    "risky": "Dubiose Downloads, Cracks und fremde Dateien erhöhen Malware-Risiko massiv.",
    "very_risky": "Sehr riskantes Klick- und Downloadverhalten ist eine der größten Gefahren überhaupt.",
    "tiktok": "TikTok und ähnliche Apps sammeln viele Nutzungs-, Geräte- und Verhaltensdaten.",
    "meta_services": "Meta-Dienste erzeugen starke Kontakt-, Interessen- und Kommunikationsprofile.",
}

RECOMMENDATIONS = {
    "not_encrypted": "Aktiviere Festplattenverschlüsselung: BitLocker, FileVault oder LUKS.",
    "unknown": "Prüfe die Einstellung bewusst, statt sie offen zu lassen.",
    "rare_updates": "Aktualisiere PC und Programme regelmäßig.",
    "disabled_updates": "Aktiviere Sicherheitsupdates wieder.",
    "admin_user": "Nutze im Alltag ein normales Benutzerkonto und Adminrechte nur bei Bedarf.",
    "phone_old": "Nutze ein Gerät mit aktuellen Sicherheitsupdates oder installiere eine gepflegte Alternative.",
    "weak_pin": "Nutze einen längeren PIN oder ein starkes Passwort.",
    "no_lock": "Aktiviere sofort eine Gerätesperre.",
    "location_always": "Setze Standortzugriff pro App auf 'Nur beim Verwenden'.",
    "chrome": "Teste Firefox, LibreWolf oder Brave mit sinnvollen Datenschutz-Einstellungen.",
    "edge": "Prüfe Tracking-, Sync- und Telemetrie-Einstellungen oder nutze Firefox/LibreWolf.",
    "no_extensions": "Installiere uBlock Origin und halte Erweiterungen minimal.",
    "too_many_extensions": "Entferne unnötige Erweiterungen, da jede Erweiterung Angriffsfläche sein kann.",
    "reused_passwords": "Wechsle zu Bitwarden, KeePassXC oder einem anderen Passwortmanager.",
    "notes_passwords": "Speichere Passwörter nicht in Klartext-Dateien oder Screenshots.",
    "twofa_none": "Aktiviere 2FA zuerst bei E-Mail, Banking, GitHub, Discord und Cloud.",
    "twofa_sms": "Nutze besser Authenticator-App oder Hardware-Key statt SMS.",
    "cloud_heavy": "Reduziere Cloud-Sync und verschlüssele sensible Daten vor dem Upload.",
    "whatsapp": "Nutze für sensible Gespräche Signal oder Threema.",
    "telegram": "Nutze geheime Chats bewusst; Standard-Chats sind nicht gleich wie Signal.",
    "discord": "Vermeide sensible private Daten in Discord und prüfe Privatsphäre-Einstellungen.",
    "social_public": "Reduziere öffentliche persönliche Informationen und alte Posts.",
    "default_router": "Ändere Router-Passwort, prüfe WPA2/WPA3 und deaktiviere WPS.",
    "open_wifi": "Sichere dein WLAN mit WPA2/WPA3 und starkem Passwort.",
    "public_wifi_sensitive": "Vermeide Banking/Logins in öffentlichen WLANs oder nutze Mobilfunk.",
    "not_sure": "Lerne den Unterschied: VPN schützt nicht automatisch Anonymität, Tor ist für andere Zwecke gedacht.",
    "risky": "Lade Software nur von offiziellen Quellen oder Paketmanagern.",
    "very_risky": "Stoppe Cracks/dubiose Downloads. Das Risiko ist deutlich höher als der Nutzen.",
    "google_services": "Deaktiviere unnötige Google-Aktivitätsverläufe und personalisierte Werbung.",
    "meta_services": "Begrenze Kontakte, Berechtigungen und Tracking bei Meta-Apps.",
    "tiktok": "Beschränke Berechtigungen oder nutze TikTok nicht auf deinem Hauptgerät.",
    "cloud_photos": "Prüfe Foto-Cloud-Sync, Standortdaten in Bildern und geteilte Alben.",
}

LEARNING = {
    "privacy": "Privatsphäre bedeutet Kontrolle darüber, welche Daten du preisgibst und wer daraus Profile bauen kann.",
    "security": "Sicherheit bedeutet Schutz vor Zugriff, Malware, Account-Übernahme und Datenverlust.",
    "anonymity": "Anonymität bedeutet, dass Aktivitäten möglichst schwer deiner echten Identität zugeordnet werden können.",
    "metadata": "Metadaten sind oft wichtiger als Inhalte: wann, wo, mit wem, welches Gerät, welche Gewohnheiten.",
    "vpn": "Ein VPN versteckt deine IP vor Webseiten, ersetzt aber kein sicheres Verhalten und macht dich nicht automatisch anonym.",
    "tor": "Tor ist stärker für Anonymität, aber nur sinnvoll, wenn du Verhalten, Logins und Fingerprinting beachtest.",
}


class ScrollFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Panel.TFrame")
        self.canvas = tk.Canvas(self, bg=COLORS["panel"], highlightthickness=0)
        self.inner = ttk.Frame(self.canvas, style="Panel.TFrame")
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview, style="Red.Vertical.TScrollbar")
        self.win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.win, width=e.width))
        self.canvas.bind_all("<MouseWheel>", self._wheel)

    def _wheel(self, event):
        if self.winfo_containing(event.x_root, event.y_root):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1480x880")
        self.minsize(1180, 740)
        self.configure(bg=COLORS["bg"])
        self.vars = {}
        self.check_vars = {}
        self.logo_img = None
        self._style()
        self._ui()

    def _style(self):
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("Root.TFrame", background=COLORS["bg"])
        s.configure("Panel.TFrame", background=COLORS["panel"])
        s.configure("Card.TFrame", background=COLORS["panel"], bordercolor=COLORS["border"], relief="solid", borderwidth=1)
        s.configure("TLabel", background=COLORS["panel"], foreground=COLORS["text"], font=BASE_FONT)
        s.configure("Title.TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=TITLE_FONT)
        s.configure("Tag.TLabel", background=COLORS["bg"], foreground=COLORS["red"], font=("Consolas", 15))
        s.configure("Muted.TLabel", background=COLORS["bg"], foreground=COLORS["muted"], font=BASE_FONT)
        s.configure("Section.TLabel", background=COLORS["panel"], foreground=COLORS["red"], font=SUB_FONT)
        s.configure("Question.TLabel", background=COLORS["panel"], foreground=COLORS["text"], font=QUESTION_FONT)
        s.configure("TRadiobutton", background=COLORS["panel"], foreground=COLORS["muted"], font=BASE_FONT, focuscolor=COLORS["panel"])
        s.map("TRadiobutton", background=[("active", COLORS["panel"])], foreground=[("selected", COLORS["red"]), ("active", COLORS["text"])])
        s.configure("TCheckbutton", background=COLORS["panel"], foreground=COLORS["muted"], font=BASE_FONT, focuscolor=COLORS["panel"])
        s.map("TCheckbutton", background=[("active", COLORS["panel"])], foreground=[("selected", COLORS["red"]), ("active", COLORS["text"])])
        s.configure("Red.TButton", background=COLORS["panel2"], foreground=COLORS["text"], bordercolor=COLORS["red"], padding=(12, 9), font=("Segoe UI Semibold", 9))
        s.map("Red.TButton", background=[("active", COLORS["select"])], foreground=[("active", COLORS["red"])])
        s.configure("Red.Vertical.TScrollbar", background=COLORS["red2"], troughcolor=COLORS["panel2"], arrowcolor=COLORS["red"], bordercolor=COLORS["panel2"])

    def _ui(self):
        root = ttk.Frame(self, style="Root.TFrame", padding=12)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root, style="Root.TFrame")
        header.pack(fill="x", pady=(0, 12))

        logo_frame = tk.Frame(header, bg=COLORS["bg"], highlightbackground=COLORS["border"], highlightthickness=1, width=230, height=230)
        logo_frame.pack(side="left", padx=(0, 24))
        logo_frame.pack_propagate(False)
        self._load_logo(logo_frame)

        htext = ttk.Frame(header, style="Root.TFrame")
        htext.pack(side="left", fill="both", expand=True)

        title_row = ttk.Frame(htext, style="Root.TFrame")
        title_row.pack(anchor="w", pady=(8, 4))
        tk.Label(title_row, text="BlackRabbit", bg=COLORS["bg"], fg=COLORS["text"], font=TITLE_FONT).pack(side="left")
        tk.Label(title_row, text="Z", bg=COLORS["bg"], fg=COLORS["red"], font=TITLE_FONT).pack(side="left")
        tk.Label(title_row, text=" Privacy & Security Analyzer", bg=COLORS["bg"], fg=COLORS["text"], font=TITLE_FONT).pack(side="left")

        ttk.Label(htext, text="SECURE. PROTECT. ANONYMIZE.", style="Tag.TLabel").pack(anchor="w")
        tk.Frame(htext, bg=COLORS["red2"], height=2).pack(fill="x", pady=12)
        ttk.Label(
            htext,
            text=(
                "Awareness-Tool für PC, Smartphone, Browser, Accounts, Cloud, Messenger und digitales Verhalten.\n"
                "Das Tool scannt nichts heimlich. Es bewertet nur Antworten und erklärt Risiken verständlich."
            ),
            style="Muted.TLabel"
        ).pack(anchor="w")

        main = ttk.Frame(root, style="Root.TFrame")
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main, style="Card.TFrame", padding=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right = ttk.Frame(main, style="Card.TFrame", padding=12)
        right.pack(side="right", fill="both", expand=True, padx=(8, 0))

        ttk.Label(left, text="❔  FRAGEN / PROFIL", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        sf = ScrollFrame(left)
        sf.pack(fill="both", expand=True)
        self._build_questions(sf.inner)

        ttk.Label(right, text="◉  AUSGABE / ANALYSE", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        self.out = tk.Text(
            right,
            bg="#090a0d",
            fg=COLORS["text"],
            insertbackground=COLORS["red"],
            relief="solid",
            bd=1,
            highlightbackground=COLORS["border"],
            font=MONO_FONT,
            wrap="word",
            padx=18,
            pady=18,
        )
        self.out.pack(fill="both", expand=True)
        self.out.insert("1.0", "Noch keine Analyse.\n\nBeantworte die Fragen links und klicke auf ANALYSIEREN.")

        btns = ttk.Frame(right, style="Panel.TFrame")
        btns.pack(fill="x", pady=(12, 0))
        ttk.Button(btns, text="▷ ANALYSIEREN", style="Red.TButton", command=self.evaluate).pack(side="left", padx=(0, 8))
        ttk.Button(btns, text="▣ ERGEBNIS SPEICHERN", style="Red.TButton", command=self.save_result).pack(side="left", padx=8)
        ttk.Button(btns, text="↺ ZURÜCKSETZEN", style="Red.TButton", command=self.reset).pack(side="left", padx=8)
        ttk.Button(btns, text="ⓘ LERNMODUS", style="Red.TButton", command=self.learning_mode).pack(side="left", padx=8)
        ttk.Button(btns, text="ⓘ ABOUT", style="Red.TButton", command=self.about_me).pack(side="left", padx=8)

    def _load_logo(self, parent):
        logo_files = ["logo.png", "logo 2.png", "BlackRabbitZ.png", "blackrabbitz.png"]
        for fname in logo_files:
            p = res_path(fname)
            if os.path.exists(p):
                try:
                    if PIL_OK:
                        img = Image.open(p).convert("RGBA")
                        img.thumbnail((210, 210), Image.LANCZOS)
                        self.logo_img = ImageTk.PhotoImage(img)
                    else:
                        self.logo_img = tk.PhotoImage(file=p)
                    tk.Label(parent, image=self.logo_img, bg=COLORS["bg"], borderwidth=0).pack(expand=True)
                    return
                except Exception as e:
                    print(f"Logo konnte nicht geladen werden: {p} | {e}")

        tk.Label(
            parent,
            text="BlackRabbitZ\nPrivacy Analyzer",
            bg=COLORS["bg"],
            fg=COLORS["red"],
            font=("Segoe UI Semibold", 15),
            justify="center",
        ).pack(expand=True)

    def _build_questions(self, parent):
        n = 1
        for key, title, opts in RADIO_QUESTIONS:
            self._qblock(parent, n, title)
            var = tk.StringVar(value=opts[0][0])
            self.vars[key] = var
            for val, label in opts:
                ttk.Radiobutton(parent, text=label, value=val, variable=var).pack(anchor="w", padx=46, pady=2)
            self._sep(parent)
            n += 1

        for key, title, opts in CHECK_QUESTIONS:
            self._qblock(parent, n, title)
            self.check_vars[key] = {}
            for val, label in opts:
                v = tk.BooleanVar(value=False)
                self.check_vars[key][val] = v
                ttk.Checkbutton(parent, text=label, variable=v).pack(anchor="w", padx=46, pady=2)
            self._sep(parent)
            n += 1

    def _qblock(self, parent, num, title):
        row = ttk.Frame(parent, style="Panel.TFrame")
        row.pack(fill="x", pady=(8, 4))
        badge = tk.Label(row, text=str(num), bg=COLORS["panel"], fg=COLORS["red"], font=("Segoe UI Semibold", 11), width=3)
        badge.pack(side="left")
        ttk.Label(row, text=title, style="Question.TLabel").pack(side="left", padx=(5, 0))

    def _sep(self, parent):
        tk.Frame(parent, bg=COLORS["line"], height=1).pack(fill="x", padx=14, pady=12)

    def _collect_answers(self):
        selected = []
        labels = []

        for key, title, opts in RADIO_QUESTIONS:
            val = self.vars[key].get()
            label = next((l for v, l in opts if v == val), val)
            selected.append(val)
            labels.append((title, label))

        checked_labels = []
        for key, title, opts in CHECK_QUESTIONS:
            vals = []
            for val, label in opts:
                if self.check_vars[key][val].get():
                    selected.append(val)
                    vals.append(label)
            if vals:
                checked_labels.append((title, vals))

        return selected, labels, checked_labels

    def _score_level(self, score):
        if score >= 80:
            return "Sehr gut"
        if score >= 65:
            return "Gut"
        if score >= 45:
            return "Mittel"
        if score >= 25:
            return "Schwach"
        return "Kritisch"

    def _bar(self, score):
        filled = max(0, min(20, int(score / 5)))
        return "█" * filled + "░" * (20 - filled)

    def evaluate(self):
        selected, labels, checked_labels = self._collect_answers()

        security = 55
        privacy = 55
        anonymity = 35
        warnings = []
        recommendations = []

        for item in selected:
            ds = SCORES.get(item) or CHECK_SCORES.get(item)
            if ds:
                security += ds[0]
                privacy += ds[1]
                anonymity += ds[2]
            if item in WARNINGS:
                warnings.append(WARNINGS[item])
            if item in RECOMMENDATIONS:
                recommendations.append(RECOMMENDATIONS[item])

        # Zielabhängige Gewichtung/Interpretation
        goal = self.vars["goal"].get()
        if goal == "goal_anonymity" and self.vars["vpn_tor"].get() not in ["tor", "both"]:
            warnings.append("Du willst Anonymität, nutzt aber kein Tor-Konzept. Ein VPN allein ist dafür nicht genug.")
            recommendations.append("Lerne Tor Browser, Tails oder Whonix kennen, aber nutze sie nur mit sauberem Verhalten.")
            anonymity -= 10
        if goal in ["goal_privacy", "goal_all"] and self.vars["browser"].get() in ["chrome", "edge"]:
            recommendations.append("Für mehr Privatsphäre solltest du Browser-Sync, Werbe-ID und Tracking-Einstellungen prüfen.")

        security = max(0, min(100, security))
        privacy = max(0, min(100, privacy))
        anonymity = max(0, min(100, anonymity))
        tracking = max(0, min(100, 100 - privacy + (10 if "tiktok" in selected else 0) + (8 if "meta_services" in selected else 0)))
        attack_surface = max(0, min(100, 100 - security + (12 if self.vars["downloads"].get() in ["risky", "very_risky"] else 0)))

        out = []
        out.append("BLACKRABBITZ PRIVACY & SECURITY ANALYZER")
        out.append("=" * 52)
        out.append("")
        out.append("SCORES")
        out.append("------")
        out.append(f"Security Score:   {security:3d}/100  {self._bar(security)}  {self._score_level(security)}")
        out.append(f"Privacy Score:    {privacy:3d}/100  {self._bar(privacy)}  {self._score_level(privacy)}")
        out.append(f"Anonymity Score:  {anonymity:3d}/100  {self._bar(anonymity)}  {self._score_level(anonymity)}")
        out.append(f"Tracking Exposure:{tracking:3d}/100  {self._bar(tracking)}  {'Hoch' if tracking >= 65 else 'Mittel' if tracking >= 35 else 'Niedrig'}")
        out.append(f"Attack Surface:   {attack_surface:3d}/100  {self._bar(attack_surface)}  {'Hoch' if attack_surface >= 65 else 'Mittel' if attack_surface >= 35 else 'Niedrig'}")
        out.append("")

        out.append("KURZFAZIT")
        out.append("---------")
        if security < 40:
            out.append("Dein Sicherheitsniveau ist kritisch. Priorität: Updates, Passwörter, 2FA, Gerätesperre und Backups.")
        elif privacy < 40:
            out.append("Deine Privatsphäre ist stark eingeschränkt. Priorität: Browser, App-Berechtigungen, Cloud und Tracking reduzieren.")
        elif anonymity < 35 and goal == "goal_anonymity":
            out.append("Für echte Anonymität reicht dein aktuelles Setup noch nicht. Verhalten, Tor/Tails/Whonix und Account-Trennung sind entscheidend.")
        else:
            out.append("Dein Setup ist nicht schlecht, aber es gibt klare Punkte, mit denen du Datenschutz und Sicherheit verbessern kannst.")
        out.append("")

        if warnings:
            out.append("WARNUNGEN")
            out.append("--------")
            for w in list(dict.fromkeys(warnings))[:12]:
                out.append(f"! {w}")
            out.append("")

        out.append("EMPFOHLENE SOFORTMASSNAHMEN")
        out.append("---------------------------")
        recs = list(dict.fromkeys(recommendations))
        if not recs:
            recs = [
                "Prüfe regelmäßig Updates, Backups und App-Berechtigungen.",
                "Nutze starke, einzigartige Passwörter und 2FA.",
                "Halte Browser-Erweiterungen minimal und vertrauenswürdig.",
            ]
        for i, r in enumerate(recs[:14], 1):
            out.append(f"{i:02d}. {r}")
        out.append("")

        out.append("PRIORITÄTENPLAN")
        out.append("---------------")
        out.append("1. Passwortmanager nutzen und doppelte Passwörter ersetzen.")
        out.append("2. 2FA für E-Mail, Cloud, Banking, GitHub, Discord und Social Media aktivieren.")
        out.append("3. PC und Handy aktuell halten; alte Geräte ohne Updates ersetzen oder isolieren.")
        out.append("4. App-Berechtigungen am Handy prüfen: Standort, Kontakte, Mikrofon, Kamera.")
        out.append("5. Browser härten: uBlock Origin, weniger Erweiterungen, Tracking-Schutz.")
        out.append("6. Backups einrichten und wichtige Daten verschlüsseln.")
        out.append("7. Cloud-Sync und Social-Media-Daten bewusst reduzieren.")
        out.append("")

        out.append("LERNHINWEIS")
        out.append("-----------")
        out.append(LEARNING["privacy"])
        out.append(LEARNING["security"])
        out.append(LEARNING["metadata"])
        if self.vars["vpn_tor"].get() in ["vpn", "not_sure"]:
            out.append(LEARNING["vpn"])
        if self.vars["goal"].get() == "goal_anonymity":
            out.append(LEARNING["anonymity"])
            out.append(LEARNING["tor"])
        out.append("")

        out.append("AUSGEWÄHLTE ANTWORTEN")
        out.append("---------------------")
        for title, label in labels:
            out.append(f"- {title} {label}")
        if checked_labels:
            out.append("")
            out.append("Mehrfachauswahl:")
            for title, vals in checked_labels:
                out.append(f"- {title} {', '.join(vals)}")

        self.out.delete("1.0", "end")
        self.out.insert("1.0", "\n".join(out))

    def learning_mode(self):
        lines = [
            "BLACKRABBITZ LERNMODUS",
            "=" * 30,
            "",
            "Sicherheit ≠ Privatsphäre ≠ Anonymität",
            "",
            f"Sicherheit:   {LEARNING['security']}",
            f"Privatsphäre: {LEARNING['privacy']}",
            f"Anonymität:   {LEARNING['anonymity']}",
            "",
            f"Metadaten:    {LEARNING['metadata']}",
            "",
            "Typische Datenquellen:",
            "- Betriebssystem-Telemetrie",
            "- Browser-Cookies und Fingerprinting",
            "- Standortverlauf am Smartphone",
            "- Cloud-Sync von Fotos, Kontakten und Dokumenten",
            "- Messenger-Metadaten",
            "- Social-Media-Profile",
            "- App-Berechtigungen",
            "",
            "Grundregel:",
            "Je bequemer und stärker alles synchronisiert ist, desto mehr Daten liegen zentral bei wenigen Diensten.",
            "Das ist nicht automatisch böse, aber man sollte es bewusst entscheiden.",
        ]
        self.out.delete("1.0", "end")
        self.out.insert("1.0", "\n".join(lines))

    def save_result(self):
        text = self.out.get("1.0", "end").strip()
        if not text:
            return
        p = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textdatei", "*.txt"), ("JSON", "*.json")],
            initialfile="blackrabbitz_privacy_security_analyse.txt",
        )
        if not p:
            return
        try:
            if p.endswith(".json"):
                selected, labels, checked_labels = self._collect_answers()
                data = {
                    "created": datetime.now().isoformat(),
                    "result": text,
                    "answers": labels,
                    "checked": checked_labels,
                }
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(text)
            messagebox.showinfo("Gespeichert", "Ergebnis wurde gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def about_me(self):
        win = tk.Toplevel(self)
        win.title("About BlackRabbitZ")
        win.geometry("700x420")
        win.configure(bg=COLORS["bg"])

        container = tk.Frame(win, bg=COLORS["panel"], highlightbackground=COLORS["border"], highlightthickness=1)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="BlackRabbitZ", bg=COLORS["panel"], fg=COLORS["red"], font=("Segoe UI Semibold", 28)).pack(pady=(25, 20))

        info_text = """# Copyright © 2026 BlackRabbitZ
# Autor: BlackRabbitZ
# Privacy & Security Analyzer
# Awareness-Tool ohne heimliche Scans oder Datenerfassung."""

        tk.Label(container, text=info_text, justify="left", bg=COLORS["panel"], fg=COLORS["text"], font=("Consolas", 12)).pack(pady=10)

        tk.Label(container, text="SECURE. PROTECT. ANONYMIZE.", bg=COLORS["panel"], fg=COLORS["red"], font=("Consolas", 14)).pack(pady=(30, 8))

    def reset(self):
        for key, title, opts in RADIO_QUESTIONS:
            self.vars[key].set(opts[0][0])
        for group in self.check_vars.values():
            for v in group.values():
                v.set(False)
        self.out.delete("1.0", "end")
        self.out.insert("1.0", "Noch keine Analyse.\n\nBeantworte die Fragen links und klicke auf ANALYSIEREN.")


if __name__ == "__main__":
    App().mainloop()
