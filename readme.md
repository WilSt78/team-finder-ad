# Team Finder

Платформа для поиска единомышленников и создания команд для совместной работы над проектами.

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/WilSt78/team-finder-ad.git
cd team-finder-ad

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Активировать (Linux/Mac)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл

DJANGO_SECRET_KEY=your-secret-key
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver