#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BlackRabbitZ Privacy & Security Analyzer
Start: python3 BlackRabbitZ_Privacy_Security_Analyzer_EN.py
Optional: place logo.png / BlackRabbitZ.png in the same folder.

This tool is an awareness and learning tool.
It does not scan devices, read data, or interfere with systems.
The evaluation is based only on the user's answers.
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
    ("pc_os", "Which operating system do you mainly use on your PC/laptop?", [
        ("windows11", "Windows 11"),
        ("windows10", "Windows 10"),
        ("linux", "Linux"),
        ("macos", "macOS"),
        ("mixed", "Multiple systems"),
    ]),
    ("pc_account", "How do you mainly sign in on your PC?", [
        ("local_account", "Local account"),
        ("microsoft_account", "Microsoft/online account"),
        ("apple_id", "Apple-ID"),
        ("google_account", "Google account"),
        ("unknown", "I don't know"),
    ]),
    ("pc_encryption", "Is your disk encrypted?", [
        ("encrypted", "Yes, e.g. BitLocker/FileVault/LUKS"),
        ("not_encrypted", "No"),
        ("unknown", "I don't know"),
    ]),
    ("pc_updates", "How do you handle updates on your PC?", [
        ("auto_updates", "Automatically / regularly"),
        ("manual_updates", "Manually, but regularly"),
        ("rare_updates", "Rarely"),
        ("disabled_updates", "Disabled or heavily delayed"),
    ]),
    ("pc_admin", "Do you use administrator rights all the time?", [
        ("standard_user", "No, standard user account"),
        ("admin_user", "Yes, mostly admin"),
        ("unknown", "I don't know"),
    ]),
    ("phone_os", "Which smartphone do you mainly use?", [
        ("android_google", "Android with Google services"),
        ("android_samsung", "Samsung Android"),
        ("android_xiaomi", "Xiaomi/Redmi/POCO Android"),
        ("android_custom", "Custom ROM / de-googled Android"),
        ("iphone", "iPhone / iOS"),
        ("no_phone", "No smartphone"),
    ]),
    ("phone_updates", "How up to date is your smartphone?", [
        ("phone_current", "Current security updates"),
        ("phone_somewhat_old", "A few months old"),
        ("phone_old", "Very old / no longer receives updates"),
        ("phone_unknown", "I don't know"),
    ]),
    ("phone_lock", "How do you lock your smartphone?", [
        ("strong_pin", "Strong PIN/passcode"),
        ("biometric_pin", "Fingerprint/Face ID plus PIN"),
        ("weak_pin", "Short PIN/pattern"),
        ("no_lock", "No lock at all"),
    ]),
    ("phone_location", "How do you use location services on your phone?", [
        ("location_strict", "Only when needed"),
        ("location_mixed", "Always enabled for some apps"),
        ("location_always", "Mostly always enabled"),
        ("location_unknown", "I don't know"),
    ]),
    ("browser", "Which browser do you mainly use?", [
        ("librewolf", "LibreWolf / hardened Firefox"),
        ("firefox", "Firefox"),
        ("brave", "Brave"),
        ("chrome", "Google Chrome"),
        ("edge", "Microsoft Edge"),
        ("safari", "Safari"),
        ("other_browser", "Anderer Browser"),
    ]),
    ("browser_extensions", "Do you use protective browser extensions?", [
        ("ublock", "uBlock Origin / good ad blocker"),
        ("some_extensions", "A few extensions"),
        ("no_extensions", "No"),
        ("too_many_extensions", "A lot of extensions"),
    ]),
    ("passwords", "How do you manage passwords?", [
        ("password_manager", "Password manager such as Bitwarden/KeePassXC/1Password"),
        ("browser_passwords", "Stored in the browser"),
        ("reused_passwords", "Many identical/similar passwords"),
        ("notes_passwords", "Notes, screenshots, or text files"),
    ]),
    ("twofa", "Do you use two-factor authentication?", [
        ("twofa_all", "Yes, for important accounts"),
        ("twofa_some", "Only partially"),
        ("twofa_sms", "Yes, but mostly via SMS"),
        ("twofa_none", "No"),
    ]),
    ("cloud", "How much do you use cloud sync?", [
        ("cloud_minimal", "Barely / deliberately limited"),
        ("cloud_normal", "Normal use for photos/documents"),
        ("cloud_heavy", "Very heavily, almost everything is synced"),
        ("cloud_unknown", "I don't know"),
    ]),
    ("messenger", "Which messenger do you use the most?", [
        ("signal", "Signal"),
        ("threema", "Threema"),
        ("whatsapp", "WhatsApp"),
        ("telegram", "Telegram"),
        ("discord", "Discord"),
        ("mixed_messenger", "Several"),
    ]),
    ("social_media", "How do you use social media?", [
        ("social_low", "Little / consciously"),
        ("social_normal", "Normal"),
        ("social_heavy", "Very heavily"),
        ("social_public", "Very heavily and publicly"),
    ]),
    ("network", "How do you protect your network?", [
        ("secure_wifi", "WPA2/WPA3, strong password"),
        ("default_router", "Router mostly on factory settings"),
        ("open_wifi", "Open/insecure WiFi"),
        ("unknown", "I don't know"),
    ]),
    ("public_wifi", "Do you use public WiFi?", [
        ("public_wifi_never", "Rarely / never"),
        ("public_wifi_sometimes", "Sometimes"),
        ("public_wifi_often", "Often"),
        ("public_wifi_sensitive", "Oftenen, including banking/logins"),
    ]),
    ("vpn_tor", "Do you use VPN or Tor?", [
        ("none", "No"),
        ("vpn", "VPN"),
        ("tor", "Tor Browser"),
        ("both", "VPN and Tor, depending on purpose"),
        ("not_sure", "Not sure what it actually does"),
    ]),
    ("downloads", "How do you handle downloads/links?", [
        ("careful", "Carefully, only trusted sources"),
        ("normal", "Normally, sometimes unknown sources"),
        ("risky", "Cracks, shady downloads, or unknown files"),
        ("very_risky", "I click/open almost everything"),
    ]),
    ("goal", "What is your main goal?", [
        ("goal_security", "More security"),
        ("goal_privacy", "More privacy"),
        ("goal_anonymity", "More anonymity"),
        ("goal_learn", "First understand what is insecure"),
        ("goal_all", "Improve everything"),
    ]),
]

CHECK_QUESTIONS = [
    ("pc_settings", "PC settings: What applies?", [
        ("telemetry_reduced", "Telemetry/diagnostic data reduced"),
        ("firewall_enabled", "Firewall enabled"),
        ("secure_boot", "Secure Boot/TPM used deliberately"),
        ("autostart_clean", "Startup apps cleaned up"),
        ("backup_pc", "Regular backups"),
        ("full_disk_encryption", "Full disk encryption enabled"),
    ]),
    ("phone_settings", "Phone settings: What applies?", [
        ("app_permissions_checked", "App permissions reviewed"),
        ("ad_id_reset", "Advertising ID disabled/reset"),
        ("app_tracking_off", "App tracking restricted"),
        ("unknown_sources_off", "Unknown sources/APK installation disabled"),
        ("bluetooth_off", "Bluetooth/NFC only when needed"),
        ("backup_phone", "Backup configured intentionally"),
    ]),
    ("apps", "Which apps/services do you use a lot?", [
        ("google_services", "Google services"),
        ("meta_services", "WhatsApp/Instagram/Facebook"),
        ("tiktok", "TikTok"),
        ("discord_app", "Discord"),
        ("cloud_photos", "Google Photos/iCloud Photos"),
        ("banking_phone", "Banking on the phone"),
    ]),
    ("privacy_tools", "Which protection measures do you already use?", [
        ("dns_blocker", "DNS blocker / Pi-hole / NextDNS / AdGuard DNS"),
        ("email_alias", "Email aliases"),
        ("separate_accounts", "Separate accounts for different purposes"),
        ("encrypted_messenger", "End-to-end encrypted messengers"),
        ("hardware_keys", "Security keys / FIDO2 / YubiKey"),
        ("encrypted_backups", "Encrypted backups"),
    ]),
]

# Points: positive values increase the score, negative values lower it.
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
    "not_encrypted": "Your data is much easier to read if the device is stolen or lost.",
    "disabled_updates": "Disabled updates leave known security vulnerabilities open.",
    "phone_old": "A phone without security updates is a high risk for daily use, banking, and private data.",
    "no_lock": "Without a device lock, private data is immediately accessible if the device is lost.",
    "location_always": "Always-on location creates movement profiles.",
    "reused_passwords": "Reused passwords are one of the biggest account security risks.",
    "twofa_none": "Without 2FA, a leaked password is often enough for account takeover.",
    "cloud_heavy": "Heavy cloud sync is convenient, but increases data concentration and tracking dependency.",
    "open_wifi": "Open WiFi is insecure and can enable abuse or interception.",
    "public_wifi_sensitive": "Banking and important logins on public WiFi are especially risky.",
    "risky": "Shady downloads, cracks, and unknown files greatly increase malware risk.",
    "very_risky": "Very risky clicking and download behavior is one of the biggest dangers overall.",
    "tiktok": "TikTok and similar apps collect a lot of usage, device, and behavioral data.",
    "meta_services": "Meta services create strong contact, interest, and communication profiles.",
}

RECOMMENDATIONS = {
    "not_encrypted": "Enable disk encryption: BitLocker, FileVault, or LUKS.",
    "unknown": "Check this setting intentionally instead of leaving it unknown.",
    "rare_updates": "Update your PC and applications regularly.",
    "disabled_updates": "Re-enable security updates.",
    "admin_user": "Use a standard user account day to day and admin rights only when needed.",
    "phone_old": "Use a device with current security updates or install a maintained alternative.",
    "weak_pin": "Use a longer PIN or a strong password.",
    "no_lock": "Enable a device lock immediately.",
    "location_always": "Set location access per app to 'Only while using'.",
    "chrome": "Try Firefox, LibreWolf, or Brave with sensible privacy settings.",
    "edge": "Check tracking, sync, and telemetry settings or use Firefox/LibreWolf.",
    "no_extensions": "Install uBlock Origin and keep extensions minimal.",
    "too_many_extensions": "Remove unnecessary extensions, because every extension can be an attack surface.",
    "reused_passwords": "Switch to Bitwarden, KeePassXC, or another password manager.",
    "notes_passwords": "Do not store passwords in plain-text files or screenshots.",
    "twofa_none": "Enable 2FA first for email, banking, GitHub, Discord, and cloud accounts.",
    "twofa_sms": "Prefer an authenticator app or hardware key instead of SMS.",
    "cloud_heavy": "Reduce cloud sync and encrypt sensitive data before uploading.",
    "whatsapp": "Use Signal or Threema for sensitive conversations.",
    "telegram": "Use secret chats intentionally; standard chats are not the same as Signal.",
    "discord": "Avoid sensitive private data on Discord and check privacy settings.",
    "social_public": "Reduce public personal information and old posts.",
    "default_router": "Change the router password, check WPA2/WPA3, and disable WPS.",
    "open_wifi": "Secure your WiFi with WPA2/WPA3 and a strong password.",
    "public_wifi_sensitive": "Avoid banking/logins on public WiFi or use mobile data.",
    "not_sure": "Learn the difference: VPN does not automatically protect anonymity; Tor is designed for different use cases.",
    "risky": "Download software only from official sources or package managers.",
    "very_risky": "Stop using cracks/shady downloads. The risk is much higher than the benefit.",
    "google_services": "Disable unnecessary Google activity history and personalized ads.",
    "meta_services": "Limit contacts, permissions, and tracking in Meta apps.",
    "tiktok": "Restrict permissions or avoid using TikTok on your main device.",
    "cloud_photos": "Check photo cloud sync, location data in images, and shared albums.",
}

LEARNING = {
    "privacy": "Privacy means control over which data you expose and who can build profiles from it.",
    "security": "Security means protection against unauthorized access, malware, account takeover, and data loss.",
    "anonymity": "Anonymity means that activities are as difficult as possible to connect to your real identity.",
    "metadata": "Metadata is often more revealing than content: when, where, with whom, which device, which habits.",
    "vpn": "A VPN hides your IP from websites, but it does not replace safe behavior and does not automatically make you anonymous.",
    "tor": "Tor is stronger for anonymity, but only useful if you also consider behavior, logins, and fingerprinting.",
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
                "Awareness tool for PC, smartphone, browser, accounts, cloud services, messengers, and digital behavior.\n"
                "The tool does not perform hidden scans. It only evaluates answers and explains risks clearly."
            ),
            style="Muted.TLabel"
        ).pack(anchor="w")

        main = ttk.Frame(root, style="Root.TFrame")
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main, style="Card.TFrame", padding=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right = ttk.Frame(main, style="Card.TFrame", padding=12)
        right.pack(side="right", fill="both", expand=True, padx=(8, 0))

        ttk.Label(left, text="❔  QUESTIONS / PROFILE", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        sf = ScrollFrame(left)
        sf.pack(fill="both", expand=True)
        self._build_questions(sf.inner)

        ttk.Label(right, text="◉  OUTPUT / ANALYSIS", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
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
        self.out.insert("1.0", "No analysis yet.\n\nAnswer the questions on the left and click ANALYZE.")

        btns = ttk.Frame(right, style="Panel.TFrame")
        btns.pack(fill="x", pady=(12, 0))
        ttk.Button(btns, text="▷ ANALYZE", style="Red.TButton", command=self.evaluate).pack(side="left", padx=(0, 8))
        ttk.Button(btns, text="▣ SAVE RESULT", style="Red.TButton", command=self.save_result).pack(side="left", padx=8)
        ttk.Button(btns, text="↺ RESET", style="Red.TButton", command=self.reset).pack(side="left", padx=8)
        ttk.Button(btns, text="ⓘ LEARNING MODE", style="Red.TButton", command=self.learning_mode).pack(side="left", padx=8)
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
                    print(f"Logo could not be loaded: {p} | {e}")

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
            return "Very good"
        if score >= 65:
            return "Good"
        if score >= 45:
            return "Medium"
        if score >= 25:
            return "Weak"
        return "Critical"

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

        # Goal-dependent weighting/interpretation
        goal = self.vars["goal"].get()
        if goal == "goal_anonymity" and self.vars["vpn_tor"].get() not in ["tor", "both"]:
            warnings.append("You want anonymity, but you do not use a Tor concept. A VPN alone is not enough for that.")
            recommendations.append("Learn about Tor Browser, Tails, or Whonix, but use them only with clean behavior.")
            anonymity -= 10
        if goal in ["goal_privacy", "goal_all"] and self.vars["browser"].get() in ["chrome", "edge"]:
            recommendations.append("For more privacy, you should check browser sync, advertising ID, and tracking settings.")

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
        out.append(f"Tracking Exposure:{tracking:3d}/100  {self._bar(tracking)}  {'High' if tracking >= 65 else 'Medium' if tracking >= 35 else 'Low'}")
        out.append(f"Attack Surface:   {attack_surface:3d}/100  {self._bar(attack_surface)}  {'High' if attack_surface >= 65 else 'Medium' if attack_surface >= 35 else 'Low'}")
        out.append("")

        out.append("SUMMARY")
        out.append("---------")
        if security < 40:
            out.append("Your security level is critical. Priority: updates, passwords, 2FA, device lock, and backups.")
        elif privacy < 40:
            out.append("Your privacy is strongly limited. Priority: browser, app permissions, cloud usage, and reducing tracking.")
        elif anonymity < 35 and goal == "goal_anonymity":
            out.append("Your current setup is not enough for real anonymity. Behavior, Tor/Tails/Whonix, and account separation are crucial.")
        else:
            out.append("Your setup is not bad, but there are clear areas where you can improve privacy and security.")
        out.append("")

        if warnings:
            out.append("WARNINGS")
            out.append("--------")
            for w in list(dict.fromkeys(warnings))[:12]:
                out.append(f"! {w}")
            out.append("")

        out.append("RECOMMENDED IMMEDIATE ACTIONS")
        out.append("---------------------------")
        recs = list(dict.fromkeys(recommendations))
        if not recs:
            recs = [
                "Regularly check updates, backups, and app permissions.",
                "Use strong, unique passwords and 2FA.",
                "Keep browser extensions minimal and trustworthy.",
            ]
        for i, r in enumerate(recs[:14], 1):
            out.append(f"{i:02d}. {r}")
        out.append("")

        out.append("PRIORITY PLAN")
        out.append("---------------")
        out.append("1. Use a password manager and replace duplicate passwords.")
        out.append("2. Enable 2FA for email, cloud, banking, GitHub, Discord, and social media.")
        out.append("3. Keep PC and phone up to date; replace or isolate old devices without updates.")
        out.append("4. Review phone app permissions: location, contacts, microphone, camera.")
        out.append("5. Harden the browser: uBlock Origin, fewer extensions, tracking protection.")
        out.append("6. Set up backups and encrypt important data.")
        out.append("7. Deliberately reduce cloud sync and social media data.")
        out.append("")

        out.append("LEARNING NOTE")
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

        out.append("SELECTED ANSWERS")
        out.append("---------------------")
        for title, label in labels:
            out.append(f"- {title} {label}")
        if checked_labels:
            out.append("")
            out.append("Multiple selection:")
            for title, vals in checked_labels:
                out.append(f"- {title} {', '.join(vals)}")

        self.out.delete("1.0", "end")
        self.out.insert("1.0", "\n".join(out))

    def learning_mode(self):
        lines = [
            "BLACKRABBITZ LEARNING MODE",
            "=" * 30,
            "",
            "Security ≠ Privacy ≠ Anonymity",
            "",
            f"Security:   {LEARNING['security']}",
            f"Privacy:    {LEARNING['privacy']}",
            f"Anonymity:  {LEARNING['anonymity']}",
            "",
            f"Metadaten:    {LEARNING['metadata']}",
            "",
            "Typical data sources:",
            "- Operating system telemetry",
            "- Browser cookies and fingerprinting",
            "- Smartphone location history",
            "- Cloud sync of photos, contacts, and documents",
            "- Messenger metadata",
            "- Social media profiles",
            "- App permissions",
            "",
            "Basic rule:",
            "The more convenient and heavily synchronized everything is, the more data is centralized with a few services.",
            "That is not automatically bad, but it should be a conscious decision.",
        ]
        self.out.delete("1.0", "end")
        self.out.insert("1.0", "\n".join(lines))

    def save_result(self):
        text = self.out.get("1.0", "end").strip()
        if not text:
            return
        p = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text file", "*.txt"), ("JSON", "*.json")],
            initialfile="blackrabbitz_privacy_security_analysis.txt",
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
            messagebox.showinfo("Saved", "Result has been saved.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def about_me(self):
        win = tk.Toplevel(self)
        win.title("About BlackRabbitZ")
        win.geometry("700x420")
        win.configure(bg=COLORS["bg"])

        container = tk.Frame(win, bg=COLORS["panel"], highlightbackground=COLORS["border"], highlightthickness=1)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="BlackRabbitZ", bg=COLORS["panel"], fg=COLORS["red"], font=("Segoe UI Semibold", 28)).pack(pady=(25, 20))

        info_text = """# Copyright © 2026 BlackRabbitZ
# Author: BlackRabbitZ
# Privacy & Security Analyzer
# Awareness tool without hidden scans or data collection."""

        tk.Label(container, text=info_text, justify="left", bg=COLORS["panel"], fg=COLORS["text"], font=("Consolas", 12)).pack(pady=10)

        tk.Label(container, text="SECURE. PROTECT. ANONYMIZE.", bg=COLORS["panel"], fg=COLORS["red"], font=("Consolas", 14)).pack(pady=(30, 8))

        tk.Label(
            container,
            text="Discord",
            bg=COLORS["panel"],
            fg=COLORS["red"],
            font=("Segoe UI Semibold", 16)
        ).pack(pady=(18, 6))

        link = tk.Label(
            container,
            text="https://discord.gg/XX4E7FtXWk",
            bg=COLORS["panel"],
            fg="#6aa9ff",
            cursor="hand2",
            font=("Consolas", 12, "underline")
        )
        link.pack()

        def open_discord(event=None):
            import webbrowser
            webbrowser.open("https://discord.gg/XX4E7FtXWk")

        link.bind("<Button-1>", open_discord)

    def reset(self):
        for key, title, opts in RADIO_QUESTIONS:
            self.vars[key].set(opts[0][0])
        for group in self.check_vars.values():
            for v in group.values():
                v.set(False)
        self.out.delete("1.0", "end")
        self.out.insert("1.0", "No analysis yet.\n\nAnswer the questions on the left and click ANALYZE.")


if __name__ == "__main__":
    App().mainloop()
