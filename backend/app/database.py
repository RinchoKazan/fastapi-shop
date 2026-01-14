from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={
        "check_same_thread": False,
    }
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    # инициализировать нашу бд с помощью engine
    Base.metadata.create_all(bind=engine)


"""
это **прям сердце работы SQLAlchemy**.

---

# 🧠 Общая картина (сначала смысл)

Весь этот код делает **три вещи**:

1. 🏭 **Создаёт “двигатель”** для базы данных (engine)
2. 📞 **Готовит фабрику сессий** (SessionLocal)
3. 🧱 **Готовит основу для таблиц** (Base)

Если коротко:

> **Engine** — знает *где база*
> **Session** — делает *конкретные запросы*
> **Base** — описывает *таблицы*

---

# 🔹 Импорты (что откуда берётся)

```python
from sqlalchemy import create_engine
```

👉 Функция, которая создаёт **engine**
(двигатель общения с БД)

---

```python
from sqlalchemy.ext.declarative import declarative_base
```

👉 Функция, которая создаёт **Base**
(основу для всех таблиц)

---

```python
from sqlalchemy.orm import sessionmaker
```

👉 Фабрика для создания **сессий**

---

```python
from .config import settings
```

👉 Импорт настроек (строка подключения к БД)

---

# 🔹 Engine — «где база и как к ней идти»

```python
engine = create_engine(
    settings.database_url,
    connect_args={
        "check_same_thread": False,
    }
)
```

### Простыми словами

> Engine — это **менеджер подключений** к базе

Он:

* знает тип БД (`sqlite`)
* знает путь (`shop.db`)
* открывает соединения, когда нужно
* закрывает их, когда не нужно

📌 **Сам engine запросы не выполняет**

---

### `check_same_thread=False`

SQLite по умолчанию:

> “один поток = одно соединение”

FastAPI:

> “много потоков”

👉 Эта опция разрешает SQLite работать нормально в FastAPI.

---

# 🔹 SessionLocal — «разговор с базой»

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

### Что такое `sessionmaker`

👉 **Фабрика**, которая делает сессии

Пример:

```python
db = SessionLocal()
```

Каждый раз — **новая сессия**

---

### Что такое Session

> Session — это **один рабочий диалог с БД**

Через неё ты:

* читаешь данные
* добавляешь
* обновляешь
* удаляешь

---

### Параметры

#### `autocommit=False`

❌ Не сохранять изменения автоматически

👉 Ты сам явно говоришь:

```python
db.commit()
```

Без этого данные **не запишутся**

---

#### `autoflush=False`

❌ Не отправлять изменения в БД автоматически

👉 Данные уйдут в БД только:

* при `commit()`
* или при ручном `flush()`

📌 Это делает поведение **предсказуемым**

---

#### `bind=engine`

👉 Говорим:

> “Все сессии работают через этот engine”

---

# 🔹 Base — «чертёж таблиц»

Ты обрезал код на `Bas`, скорее всего дальше:

```python
Base = declarative_base()
```

### Что это значит

👉 `Base` — **родительский класс для всех моделей**

Пример:

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
```

📌 SQLAlchemy понимает:

> “Это таблица, её нужно создать в БД”

---

# 🔹 Вся схема одной картинкой (словами)

```
FastAPI endpoint
       ↓
   Session (SessionLocal)
       ↓
     Engine
       ↓
   SQLite файл
```

---

# 🔹 Почему это разделено

| Объект  | Зачем                  |
| ------- | ---------------------- |
| Engine  | один на всё приложение |
| Session | одна на запрос         |
| Base    | один для всех моделей  |

---

# 🔹 Типичное использование

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Каждый запрос:

* получает свою сессию
* работает
* закрывает её

---

# 🔹 Очень коротко (если забыть всё)

> 🔧 **Engine** — куда подключаемся
> 📞 **Session** — работаем с БД
> 🧱 **Base** — описываем таблицы


"""