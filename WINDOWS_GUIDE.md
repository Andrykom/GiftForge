# 🪟 Запуск GiftForge MVP на Windows

## Проблема
Git Bash закрывается после выполнения скрипта — это нормальное поведение.

## Решение

### Вариант 1: Использовать start.bat (рекомендуется)
1. Откройте папку проекта в Проводнике
2. Двойной клик по `start.bat`
3. Окно останется открытым после выполнения

### Вариант 2: PowerShell
```powershell
.\start.ps1
```

### Вариант 3: Командная строка (CMD)
```cmd
start.bat
```

### Вариант 4: VS Code Terminal
1. Откройте проект в VS Code
2. Terminal → New Terminal
3. Выберите Git Bash или PowerShell
4. Выполните:
   ```bash
   ./start.sh
   ```
   или
   ```powershell
   .\start.ps1
   ```

## 🚀 После запуска инфраструктуры

Откройте **новое** окно терминала для работы с проектом:

```bash
# Проверка статуса
./status.sh        # или status.bat

# Запуск API (в foreground, для разработки)
docker-compose up core-api

# Запуск в фоне
docker-compose up -d core-api

# Логи API
docker-compose logs -f core-api

# Остановка всего
docker-compose down
```

## 🔧 Полезные команды Windows

```cmd
# Проверка Docker
docker --version
docker-compose --version

# Список контейнеров
docker ps

# Остановить все контейнеры
docker-compose stop

# Полный сброс (удалит данные!)
docker-compose down -v
```

## 🐛 Если окно всё равно закрывается

1. Откройте CMD/PowerShell вручную
2. Перейдите в папку проекта:
   ```cmd
   cd C:\path\to\giftforge-mvp
   ```
3. Запустите:
   ```cmd
   start.bat
   ```

## 📁 Файлы проекта

После запуска `start.bat` у вас будут работать:
- ✅ PostgreSQL на порту 5432
- ✅ Redis на порту 6379
- ✅ Таблицы созданы через Alembic

Далее запускайте API и ботов отдельно.
