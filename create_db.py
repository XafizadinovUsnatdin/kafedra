from app import app, db
from models import User, Xodim, IlmiyIsh, UslubiyIsh, Fan, Yangilik
from werkzeug.security import generate_password_hash

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ── Admin ──────────────────────────────────────────────────────────
        admin = User(
            username='admin',
            email='admin@kafedra.uz',
            full_name='Tizim Administratori',
            password_hash=generate_password_hash('admin123'),
            role='admin',
        )
        db.session.add(admin)

        # ── O'qituvchilar ──────────────────────────────────────────────────
        teachers_data = [
            ('abdullayev', 'Abdullayev Jamshid Holiqovich', 'abdullayev@kafedra.uz',
             'Professor', 'DSc', 'professor', 'Axborot texnologiyalari kafedrasi'),
            ('toshmatov', 'Toshmatov Sardor Baxtiyorovich', 'toshmatov@kafedra.uz',
             'Dotsent', 'PhD', 'dotsent', 'Axborot texnologiyalari kafedrasi'),
            ('xoliqova', "Xoliqova Malika Ro'ziyevna", 'xoliqova@kafedra.uz',
             "Katta o'qituvchi", 'PhD', 'dotsent', 'Axborot texnologiyalari kafedrasi'),
            ('mirzayev', 'Mirzayev Bobur Anvarovich', 'mirzayev@kafedra.uz',
             "Katta o'qituvchi", 'yoq', 'yoq', 'Axborot texnologiyalari kafedrasi'),
            ('raximova', "Raximova Gulnora Norbo'tayevna", 'raximova@kafedra.uz',
             'Assistent', 'yoq', 'yoq', 'Axborot texnologiyalari kafedrasi'),
        ]

        teachers = []
        for uname, fullname, email, lavozim, daraja, unvon, kafedra in teachers_data:
            u = User(
                username=uname,
                email=email,
                full_name=fullname,
                password_hash=generate_password_hash('pass123'),
                role='teacher',
            )
            db.session.add(u)
            db.session.flush()
            x = Xodim(
                user_id=u.id,
                lavozim=lavozim,
                ilmiy_daraja=daraja,
                ilmiy_unvon=unvon,
                kafedra=kafedra,
                telefon='+998901234567',
                bio=(f"{fullname} — Axborot texnologiyalari kafedrasi {lavozim.lower()}i. "
                     f"Kompyuter fanlari va dasturlash bo'yicha yetakchi mutaxassis."),
            )
            db.session.add(x)
            teachers.append(u)

        # ── Talabalar ──────────────────────────────────────────────────────
        for i in range(1, 4):
            s = User(
                username=f'student{i}',
                email=f'student{i}@edu.uz',
                full_name=f'Talaba {i}-namuna',
                password_hash=generate_password_hash('pass123'),
                role='student',
            )
            db.session.add(s)

        db.session.flush()

        # ── Ilmiy ishlar ───────────────────────────────────────────────────
        ilmiy_data = [
            (teachers[0].id, "Sun'iy intellekt algoritmlarini o'quv jarayoniga tatbiq etish", 'maqola', 2023,
             'Raqamli texnologiyalar jurnali', 'https://doi.org/10.1234/rt.2023.01',
             "Ushbu maqolada sun'iy intellekt usullaridan ta'lim sohasida foydalanish imkoniyatlari ko'rib chiqilgan."),
            (teachers[0].id, "Ma'lumotlar bazasi boshqaruv tizimlari: zamonaviy yondashuvlar", 'monografiya', 2022,
             'Fan va texnologiya nashriyoti', None,
             "Zamonaviy MBBT larning arxitekturasi va ularni ta'lim muassasalarida qo'llash masalalari yoritilgan."),
            (teachers[1].id, "Bulutli hisoblash texnologiyalari va ularning ta'limdagi o'rni", 'maqola', 2023,
             "Axborot texnologiyalari va ta'lim", 'https://doi.org/10.5678/at.2023.02',
             "Bulutli hisoblash texnologiyalarini oliy ta'lim muassasalarida joriy etish tajribalari tahlil qilingan."),
            (teachers[1].id, "Kiberxavfsizlik asoslari va tarmoq muhofazasi", 'maqola', 2022,
             'Xavfsizlik texnologiyalari jurnali', None,
             "Zamonaviy kibertahdidlar va ulardan himoyalanish usullari ko'rib chiqilgan."),
            (teachers[2].id, "Python dasturlash tilini o'qitishda innovatsion metodlar", 'tezis', 2023,
             "Xalqaro ilmiy-amaliy konferensiya materiallari", None,
             "Python dasturlash tilini o'rgatishda loyiha asosida ta'lim metodologiyasi taqdim etilgan."),
            (teachers[2].id, "Veb-dasturlash texnologiyalarining rivojlanish tendensiyalari", 'maqola', 2021,
             "IT va ta'lim jurnali", 'https://doi.org/10.9012/it.2021.05',
             "Zamonaviy frontend va backend texnologiyalarining rivojlanish yo'nalishlari tahlil qilingan."),
            (teachers[3].id, "Mobil ilovalar ishlab chiqishda agil metodologiya", 'tezis', 2022,
             "Yosh olimlar konferensiyasi", None,
             "Mobil ilova yaratishda Scrum metodologiyasini qo'llash tajribalari ko'rsatilgan."),
            (teachers[0].id, "Neyron tarmoqlar yordamida tasvirni aniqlash", 'maqola', 2024,
             "Kompyuter fanlari jurnali", 'https://doi.org/10.2024/cs.08',
             "Chuqur o'qitish (deep learning) usullari yordamida tasvirlarni klassifikatsiya qilish tadqiq qilingan."),
            (teachers[1].id, "IoT qurilmalarining xavfsizligi: muammolar va yechimlar", 'patent', 2023,
             "O'zbekiston Intellektual mulk agentligi", None,
             "IoT qurilmalar uchun ishlab chiqilgan yangi xavfsizlik protokoli patentlangan."),
            (teachers[2].id, "Ma'lumotlar tahlili va vizualizatsiya metodlari", 'maqola', 2023,
             "Big Data va tahlil jurnali", None,
             "Katta hajmli ma'lumotlarni tahlil qilish va natijalarni vizual ko'rsatish usullari taqdim etilgan."),
            (teachers[3].id, "Blokchain texnologiyasi va ta'limdagi qo'llanilishi", 'dissertatsiya', 2023,
             "O'zMU", None,
             "Blokchain texnologiyasini ta'lim sertifikatlarini tasdiqlashda qo'llash imkoniyatlari o'rganilgan."),
            (teachers[4].id, "Gamifikatsiya elementlarini o'quv jarayoniga tatbiq etish", 'tezis', 2024,
             "Yoshlar innovatsiyalari forumi", None,
             "O'quv jarayonida o'yin elementlarini qo'llash orqali talabalar motivatsiyasini oshirish yo'llari."),
        ]

        for muallif_id, sarlavha, tur, yil, nashr, doi, tavsif in ilmiy_data:
            ii = IlmiyIsh(
                sarlavha=sarlavha,
                muallif_id=muallif_id,
                tur=tur,
                yil=yil,
                nashr_joyi=nashr,
                doi_link=doi,
                tavsif=tavsif,
                holat='tasdiqlangan',
            )
            db.session.add(ii)

        # ── Uslubiy ishlar ─────────────────────────────────────────────────
        uslubiy_data = [
            (teachers[0].id, "Ma'lumotlar bazasi: nazariya va amaliyot", 'darslik',
             "Ma'lumotlar bazasi", 2022, 'TATU nashriyoti',
             "Ushbu darslik MBBT kursini o'rganuvchi talabalarga mo'ljallangan."),
            (teachers[0].id, "SQL tilida dasturlash bo'yicha amaliy qo'llanma", 'oqquv_qollanma',
             "Ma'lumotlar bazasi", 2023, 'TATU nashriyoti',
             "SQL so'rovlarini yozish va optimallashtirish bo'yicha amaliy mashqlar to'plami."),
            (teachers[1].id, "Kompyuter tarmoqlari asoslari: o'quv qo'llanma", 'oqquv_qollanma',
             "Kompyuter tarmoqlari", 2022, "O'z DSP nashriyoti",
             "Kompyuter tarmoqlarining asosiy tushunchalari va protokollar tizimi yoritilgan."),
            (teachers[1].id, "Axborot xavfsizligi kursi dasturi", 'dastur',
             "Axborot xavfsizligi", 2023, 'Kafedra nashriyoti',
             "Axborot xavfsizligi fanining to'liq o'quv dasturi va mavzular taqsimoti."),
            (teachers[2].id, "Python dasturlash: boshlang'ich va o'rta daraja", 'darslik',
             "Dasturlash tillari", 2023, "O'quv adabiyotlari nashriyoti",
             "Python dasturlash tilini bosqichma-bosqich o'rgatuvchi to'liq kurs darsligi."),
            (teachers[2].id, "Veb-dasturlash texnologiyalari kursi silabuslari", 'sillabusi',
             "Veb-dasturlash", 2024, 'Kafedra nashriyoti',
             "HTML, CSS, JavaScript va React texnologiyalari bo'yicha kurs silabuslari."),
            (teachers[3].id, "Mobil dasturlash: Android va iOS", 'oqquv_qollanma',
             "Mobil dasturlash", 2022, 'Fan nashriyoti',
             "Android va iOS platformalari uchun mobil ilovalar yaratish bo'yicha qo'llanma."),
            (teachers[3].id, "Loyiha boshqaruvi asoslari kursi silabuslari", 'sillabusi',
             "Loyiha boshqaruvi", 2023, 'Kafedra nashriyoti',
             "IT loyihalarini boshqarish metodologiyalari bo'yicha kurs silabuslari."),
            (teachers[4].id, "Algoritm va ma'lumotlar tuzilmalari", 'darslik',
             "Algoritmlar", 2023, "O'quv adabiyotlari nashriyoti",
             "Asosiy algoritmlar va ma'lumotlar tuzilmalari bo'yicha to'liq darslik."),
            (teachers[0].id, "Sun'iy intellekt va mashinaviy o'qitish: uslubiy qo'llanma", 'uslubiy_qollanma',
             "Sun'iy intellekt", 2024, 'TATU nashriyoti',
             "AI va ML sohalari bo'yicha laboratoriya ishlari va mustaqil topshiriqlar to'plami."),
            (teachers[1].id, "Kiberxavfsizlik kursi o'quv dasturi", 'dastur',
             "Kiberxavfsizlik", 2024, 'Kafedra nashriyoti',
             "Zamonaviy kiberxavfsizlik yo'nalishi uchun to'liq o'quv dasturi."),
            (teachers[2].id, "Django freymvork orqali veb-dasturlash", 'uslubiy_qollanma',
             "Veb-dasturlash", 2023, 'Fan nashriyoti',
             "Django freymvorki yordamida dinamik veb-saytlar yaratish bo'yicha uslubiy ko'rsatmalar."),
        ]

        for muallif_id, sarlavha, tur, fan_nomi, yil, nashriyot, tavsif in uslubiy_data:
            ui = UslubiyIsh(
                sarlavha=sarlavha,
                muallif_id=muallif_id,
                tur=tur,
                fan_nomi=fan_nomi,
                yil=yil,
                nashriyot=nashriyot,
                tavsif=tavsif,
                holat='tasdiqlangan',
            )
            db.session.add(ui)

        # ── Fanlar ──────────────────────────────────────────────────────────
        fanlar_data = [
            ("Ma'lumotlar bazasi", 'AT201', teachers[0].id, 3, 60, 3, 2, "AT yo'nalishi"),
            ("Kompyuter tarmoqlari", 'AT202', teachers[1].id, 3, 60, 4, 2, "AT yo'nalishi"),
            ("Dasturlash tillari: Python", 'AT203', teachers[2].id, 4, 90, 1, 1, "AT yo'nalishi"),
            ("Veb-dasturlash texnologiyalari", 'AT301', teachers[2].id, 4, 90, 5, 3, "AT yo'nalishi"),
            ("Mobil dasturlash", 'AT302', teachers[3].id, 3, 60, 6, 3, "AT yo'nalishi"),
            ("Sun'iy intellekt asoslari", 'AT401', teachers[0].id, 3, 60, 7, 4, "AT yo'nalishi"),
            ("Axborot xavfsizligi", 'AT303', teachers[1].id, 3, 60, 5, 3, "AT yo'nalishi"),
            ("Algoritm va ma'lumotlar tuzilmalari", 'AT102', teachers[4].id, 4, 90, 2, 1, "AT yo'nalishi"),
            ("Loyiha boshqaruvi", 'AT402', teachers[3].id, 3, 60, 7, 4, "AT yo'nalishi"),
            ("Kiberxavfsizlik", 'AT403', teachers[1].id, 3, 60, 8, 4, "AT yo'nalishi"),
        ]
        for nomi, kodi, muallim_id, kredit, soatlar, semestr, kurs, mutaxassislik in fanlar_data:
            f = Fan(
                nomi=nomi, kodi=kodi, muallim_id=muallim_id,
                kredit=kredit, soatlar=soatlar,
                semestr=semestr, kurs=kurs, mutaxassislik=mutaxassislik,
                tavsif=f"{nomi} bo'yicha to'liq kurs. Nazariy va amaliy mashg'ulotlar."
            )
            db.session.add(f)

        # ── Yangiliklar ──────────────────────────────────────────────────────
        yangiliklar_data = [
            (admin.id, "Kafedrada yangi ilmiy laboratoriya ochildi",
             "Axborot texnologiyalari kafedrasida zamonaviy ilmiy-tadqiqot laboratoriyasi ochildi. "
             "Laboratoriya sun'iy intellekt va katta ma'lumotlar tahlili yo'nalishlarida faoliyat yuritadi. "
             "Barcha talabalar va o'qituvchilar laboratoriyadan foydalanishlari mumkin."),
            (admin.id, "Xalqaro konferensiyada qatnashish natijalari",
             "Kafedra o'qituvchilari Toshkentda bo'lib o'tgan 'Zamonaviy axborot texnologiyalari' "
             "xalqaro ilmiy-amaliy konferensiyasida 5 ta maqola bilan qatnashdilar. "
             "Barcha maqolalar konferensiya to'plamiga kiritildi."),
            (admin.id, "2024-yil uchun ilmiy ishlar rejalashtirildi",
             "Kafedra 2024-yil uchun ilmiy-tadqiqot ishlar rejasini tasdiqladi. "
             "Rejaga ko'ra, yil davomida 15 ta maqola, 2 ta monografiya va 1 ta patent ishlab chiqilishi rejalashtirilgan. "
             "Barcha o'qituvchilar rejalashtirilgan muddatlarga amal qilishlari kerak."),
            (admin.id, "Yangi o'quv yili uchun sillabuslar yangilandi",
             "2024-2025 o'quv yili uchun barcha fanlar silabuslari yangilandi va tasdiqlandi. "
             "Yangi sillabuslar tizimga yuklangan bo'lib, talabalar ularni yuklab olishlari mumkin."),
        ]
        for muallif_id, sarlavha, matn in yangiliklar_data:
            y = Yangilik(sarlavha=sarlavha, matn=matn, muallif_id=muallif_id, is_published=True)
            db.session.add(y)

        db.session.commit()
        print("OK: Ma'lumotlar bazasi muvaffaqiyatli yaratildi va to'ldirildi!")
        print("\nLogin ma'lumotlari:")
        print("  Admin:       admin / admin123")
        print("  O'qituvchi1: abdullayev / pass123")
        print("  O'qituvchi2: toshmatov / pass123")
        print("  O'qituvchi3: xoliqova / pass123")
        print("  Talaba:      student1 / pass123")
        print("\nSaytni ishga tushirish: python app.py")
        print("Manzil: http://localhost:5000")


if __name__ == '__main__':
    seed()
