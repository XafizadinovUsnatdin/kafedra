# Kafedra ilmiy-uslubiy tizimi - Mermaid diagrammalar

Quyidagi diagrammalar loyiha strukturasi va `app.py`/`models.py` dagi real kod oqimlariga moslab tuzilgan.

## 1) Umumiy arxitektura (komponentlar)

```mermaid
flowchart LR
  subgraph Users[Users]
    Guest[Guest]
    Student[Student]
    Teacher[Teacher]
    Admin[Admin]
  end

  Browser[Browser]
  Guest --> Browser
  Student --> Browser
  Teacher --> Browser
  Admin --> Browser

  Browser -->|HTTP| Flask[Flask app\n(app.py)]
  Flask --> Templates[Templates\n(Jinja2)]
  Flask --> Static[Static assets\n(Bootstrap 5, CSS/JS, SVG)]

  Flask -->|ORM| DB[(SQLAlchemy DB)]
  DB -->|sqlite file| SqliteFile[instance/kafedra.db]
  DB -->|optional| Postgres[(PostgreSQL via DATABASE_URL)]

  Flask --> Uploads[(File storage\nuploads/)]
  Uploads --> Docs[uploads/docs/*]
  Uploads --> Photos[uploads/photos/*]

  Flask --> ExportExcel[Excel export\n(openpyxl)]
  Flask --> ExportPDF[PDF export\n(reportlab)]
```

## 2) Ma'lumotlar bazasi (ERD)

> `Izoh` polymorphic: izoh ilmiy yoki uslubiy ishga bog'lanishi mumkin (ikkalasidan bittasi).

```mermaid
erDiagram
  USERS ||--o| XODIMLAR : "user_id"
  USERS ||--o{ ILMIY_ISHLAR : "muallif_id"
  USERS ||--o{ USLUBIY_ISHLAR : "muallif_id"
  USERS o|--o{ FANLAR : "muallim_id (nullable)"
  USERS o|--o{ YANGILIKLAR : "muallif_id (nullable)"
  USERS ||--o{ IZOHLAR : "muallif_id"

  ILMIY_ISHLAR ||--o{ IZOHLAR : "ilmiy_ish_id (nullable)"
  USLUBIY_ISHLAR ||--o{ IZOHLAR : "uslubiy_ish_id (nullable)"

  USERS {
    int id PK
    string username "unique"
    string email "unique"
    string password_hash
    string full_name
    string role "admin|teacher|student"
    boolean is_active
    datetime created_at
  }

  XODIMLAR {
    int id PK
    int user_id FK
    string lavozim
    string ilmiy_daraja
    string ilmiy_unvon
    string kafedra
    string telefon
    text bio
    string photo_path
  }

  ILMIY_ISHLAR {
    int id PK
    int muallif_id FK
    string sarlavha
    string hammuallif
    string tur
    int yil
    string nashr_joyi
    string doi_link
    string fayl_path
    text tavsif
    string holat "kutilmoqda|tasdiqlangan|..."
    int views_count
    int downloads_count
    datetime created_at
  }

  USLUBIY_ISHLAR {
    int id PK
    int muallif_id FK
    string sarlavha
    string hammuallif
    string tur
    string fan_nomi
    int yil
    string nashriyot
    string fayl_path
    text tavsif
    string holat "kutilmoqda|tasdiqlangan|..."
    int views_count
    int downloads_count
    datetime created_at
  }

  FANLAR {
    int id PK
    string nomi
    string kodi
    int muallim_id FK
    int kredit
    int soatlar
    int semestr
    int kurs
    string mutaxassislik
    text tavsif
  }

  YANGILIKLAR {
    int id PK
    string sarlavha
    text matn
    int muallif_id FK
    string rasm_url
    boolean is_published
    datetime created_at
  }

  IZOHLAR {
    int id PK
    text matn
    int muallif_id FK
    int ilmiy_ish_id FK "nullable"
    int uslubiy_ish_id FK "nullable"
    datetime created_at
  }
```

## 3) Router xaritasi (endpointlar + ruxsatlar)

```mermaid
flowchart TB
  subgraph Auth[Auth]
    L1["GET/POST /login\nGuest only"]
    L2["GET /logout\nlogin_required"]
    L3["GET/POST /register\nGuest only"]
    L4["GET/POST /settings\nlogin_required"]
  end

  subgraph Main[Main]
    M1["GET /\nPublic"]
    M2["GET /dashboard\nlogin_required"]
  end

  subgraph Ilmiy[Ilmiy ishlar]
    I1["GET /ilmiy\nPublic (admin: holat filter)"]
    I2["GET /ilmiy/:id\nPublic if tasdiqlangan\nelse admin/owner"]
    I3["POST /ilmiy/:id/izoh\nlogin_required"]
    I4["GET/POST /ilmiy/qoshish\nlogin_required + teacher_required"]
    I5["GET/POST /ilmiy/:id/tahrirlash\nlogin_required + owner/admin"]
    I6["POST /ilmiy/:id/ochirish\nlogin_required + owner/admin"]
  end

  subgraph Uslubiy[Uslubiy ishlar]
    U1["GET /uslubiy\nPublic (admin: holat filter)"]
    U2["GET /uslubiy/:id\nPublic if tasdiqlangan\nelse admin/owner"]
    U3["POST /uslubiy/:id/izoh\nlogin_required"]
    U4["GET/POST /uslubiy/qoshish\nlogin_required + teacher_required"]
    U5["GET/POST /uslubiy/:id/tahrirlash\nlogin_required + owner/admin"]
    U6["POST /uslubiy/:id/ochirish\nlogin_required + owner/admin"]
  end

  subgraph Xodimlar[Xodimlar]
    X1["GET /xodimlar\nPublic"]
    X2["GET /xodimlar/:id\nPublic"]
    X3["GET/POST /profil/tahrirlash\nlogin_required"]
  end

  subgraph Fanlar[Fanlar]
    F1["GET /fanlar\nPublic"]
    F2["GET /fanlar/:id\nPublic"]
    F3["GET/POST /fanlar/qoshish\nlogin_required + teacher_required"]
  end

  subgraph Talaba[Talaba kabineti]
    T1["GET /talaba/kabinet\nlogin_required"]
  end

  subgraph Hisobot[Hisobotlar]
    H1["GET /hisobotlar\nlogin_required"]
    H2["GET /hisobotlar/excel\nlogin_required"]
    H3["GET /hisobotlar/pdf\nlogin_required"]
  end

  subgraph AdminPanel[Admin panel]
    A1["GET /admin\nlogin_required + admin_required"]
    A2["GET /admin/foydalanuvchilar\nlogin_required + admin_required"]
    A3["POST /admin/foydalanuvchi/:id/holat\nlogin_required + admin_required"]
    A4["GET /admin/kutilmoqda\nlogin_required + admin_required"]
    A5["POST /admin/tasdiqlash/ilmiy/:id\nlogin_required + admin_required"]
    A6["POST /admin/tasdiqlash/uslubiy/:id\nlogin_required + admin_required"]
  end

  subgraph Yangiliklar[Yangiliklar]
    Y1["GET /yangiliklar\nPublic"]
    Y2["GET /yangiliklar/:id\nPublic"]
    Y3["GET/POST /yangiliklar/qoshish\nlogin_required + admin_required"]
  end

  subgraph FilesAPI[Files & API]
    D1["GET /uploads/:filename\nlogin_required (downloads counter)"]
    S1["GET /api/statistika\nPublic JSON"]
  end
```

## 4) Login oqimi (sequence)

```mermaid
sequenceDiagram
  participant U as User
  participant B as Browser
  participant A as Flask (app.py)
  participant DB as DB (SQLAlchemy)

  U->>B: Username + password
  B->>A: POST /login
  A->>DB: SELECT users WHERE username=...
  DB-->>A: User row
  A->>A: check_password_hash()
  alt is_active == false
    A-->>B: flash "Hisobingiz faollashtirilinmagan"
    B-->>U: Show error
  else ok
    A->>A: login_user() (session cookie)
    A-->>B: Redirect /dashboard (or next)
    B-->>U: Dashboard page
  end
```

## 5) Ilmiy ish qo'shish + admin tasdiqlashi (sequence)

```mermaid
sequenceDiagram
  participant T as Teacher/Admin
  participant B as Browser
  participant A as Flask (app.py)
  participant FS as uploads/ (filesystem)
  participant DB as DB (SQLAlchemy)
  participant ADM as Admin

  T->>B: Form + file upload
  B->>A: POST /ilmiy/qoshish
  A->>A: teacher_required
  A->>FS: save_file() -> uploads/docs/<ts>_file
  A->>DB: INSERT ilmiy_ishlar (holat=kutilmoqda or tasdiqlangan)
  DB-->>A: commit
  A-->>B: Redirect /ilmiy/:id

  alt Teacher (not admin)
    Note over A,DB: holat='kutilmoqda'
    ADM->>B: Approve from /admin/kutilmoqda
    B->>A: POST /admin/tasdiqlash/ilmiy/:id (holat=tasdiqlangan|...)
    A->>DB: UPDATE ilmiy_ishlar.holat
    DB-->>A: commit
    A-->>B: Redirect /admin/kutilmoqda
  else Admin creates
    Note over A,DB: holat='tasdiqlangan'
  end
```

## 6) Holat state diagram (Ilmiy/Uslubiy)

```mermaid
stateDiagram-v2
  [*] --> kutilmoqda: Teacher create/edit
  kutilmoqda --> tasdiqlangan: Admin tasdiqlaydi
  kutilmoqda --> rad_etilgan: Admin rad etadi (holat qiymati)
  tasdiqlangan --> kutilmoqda: Teacher edit (admin emas)
  tasdiqlangan --> rad_etilgan: Admin o'zgartiradi
  rad_etilgan --> kutilmoqda: Teacher qayta tahrirlaydi
```

## 7) Render deploy oqimi

```mermaid
sequenceDiagram
  participant G as Git Push
  participant R as Render Build
  participant P as Pip
  participant DB as SQLite file
  participant W as Web Service (gunicorn)

  G->>R: Trigger deploy
  R->>P: pip install -r requirements.txt
  R->>R: python create_db.py
  R->>DB: create instance/kafedra.db
  R->>W: gunicorn app:app --bind 0.0.0.0:$PORT
```
