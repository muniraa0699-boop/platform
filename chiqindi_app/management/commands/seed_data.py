from django.core.management.base import BaseCommand
from chiqindi_app.models import CustomUser, WasteReport, Notification


class Command(BaseCommand):
    help = "Test ma'lumotlari yaratish"

    def handle(self, *args, **options):
        # Superuser
        if not CustomUser.objects.filter(username='admin').exists():
            admin = CustomUser.objects.create_superuser(
                username='admin', email='admin@chiqindi.uz',
                password='admin123', first_name='Admin', last_name='Super',
                role=CustomUser.ROLE_AUTHORITY
            )
            self.stdout.write(self.style.SUCCESS('✓ Superuser yaratildi: admin / admin123'))

        # Fuqarolar
        if not CustomUser.objects.filter(username='fuqaro1').exists():
            f1 = CustomUser.objects.create_user(
                username='fuqaro1', email='fuqaro1@gmail.com', password='fuqaro123',
                first_name='Jasur', last_name='Karimov',
                role=CustomUser.ROLE_CITIZEN, phone='+998901234567'
            )
            self.stdout.write(self.style.SUCCESS('✓ Fuqaro yaratildi: fuqaro1 / fuqaro123'))
        else:
            f1 = CustomUser.objects.get(username='fuqaro1')

        if not CustomUser.objects.filter(username='fuqaro2').exists():
            f2 = CustomUser.objects.create_user(
                username='fuqaro2', email='fuqaro2@gmail.com', password='fuqaro123',
                first_name='Malika', last_name='Yusupova',
                role=CustomUser.ROLE_CITIZEN, phone='+998909876543'
            )
            self.stdout.write(self.style.SUCCESS('✓ Fuqaro yaratildi: fuqaro2 / fuqaro123'))
        else:
            f2 = CustomUser.objects.get(username='fuqaro2')

        # Hokimiyat xodimlari
        if not CustomUser.objects.filter(username='hokimiyat1').exists():
            h1 = CustomUser.objects.create_user(
                username='hokimiyat1', email='hokimiyat1@toshkent.uz', password='hokimiyat123',
                first_name='Bobur', last_name='Rahimov',
                role=CustomUser.ROLE_AUTHORITY, phone='+998711234567'
            )
            self.stdout.write(self.style.SUCCESS('✓ Hokimiyat yaratildi: hokimiyat1 / hokimiyat123'))
        else:
            h1 = CustomUser.objects.get(username='hokimiyat1')

        if not CustomUser.objects.filter(username='hokimiyat2').exists():
            h2 = CustomUser.objects.create_user(
                username='hokimiyat2', email='hokimiyat2@samarqand.uz', password='hokimiyat123',
                first_name='Dilnoza', last_name='Ergasheva',
                role=CustomUser.ROLE_AUTHORITY, phone='+998712345678'
            )
            self.stdout.write(self.style.SUCCESS('✓ Hokimiyat yaratildi: hokimiyat2 / hokimiyat123'))
        else:
            h2 = CustomUser.objects.get(username='hokimiyat2')

        # Chiqindi xabarlari
        if WasteReport.objects.count() < 5:
            test_reports = [
                {
                    'citizen': f1, 'latitude': 41.2995, 'longitude': 69.2401,
                    'waste_type': 'uy', 'size': 'katta', 'viloyat': 'toshkent_sh',
                    'tuman': 'Chilonzor', 'address': 'Chilonzor-9 MFY',
                    'description': 'Katta uy chiqindisi to\'plami',
                    'status': WasteReport.STATUS_PENDING,
                },
                {
                    'citizen': f1, 'latitude': 39.6542, 'longitude': 66.9597,
                    'waste_type': 'qurilish', 'size': 'katta', 'viloyat': 'samarqand',
                    'tuman': 'Samarqand', 'address': 'Registon ko\'chasi',
                    'description': 'Qurilish materiallar qoldiqlari',
                    'status': WasteReport.STATUS_ACCEPTED,
                },
                {
                    'citizen': f2, 'latitude': 39.7747, 'longitude': 64.4286,
                    'waste_type': 'plastik', 'size': 'orta', 'viloyat': 'buxoro',
                    'tuman': 'Buxoro', 'address': 'Ark yaqini',
                    'description': 'Plastik shishaalar va qadoqlar',
                    'status': WasteReport.STATUS_CLEANING,
                },
                {
                    'citizen': f2, 'latitude': 40.7821, 'longitude': 72.3442,
                    'waste_type': 'xavfli', 'size': 'kichik', 'viloyat': 'andijon',
                    'tuman': 'Andijon', 'address': 'Sanoat ko\'chasi 12',
                    'description': 'Kimyoviy moddalar qoldiqlari',
                    'status': WasteReport.STATUS_IN_PROGRESS,
                },
                {
                    'citizen': f1, 'latitude': 40.1036, 'longitude': 65.3792,
                    'waste_type': 'boshqa', 'size': 'orta', 'viloyat': 'navoiy',
                    'tuman': 'Navoiy', 'address': 'Markaziy park',
                    'description': 'Aralash chiqindilar',
                    'status': WasteReport.STATUS_DONE,
                },
            ]

            for data in test_reports:
                WasteReport.objects.create(**data)

            self.stdout.write(self.style.SUCCESS('✓ 5 ta test xabar yaratildi'))

        self.stdout.write(self.style.SUCCESS('\n=== Test ma\'lumotlari yaratildi ==='))
        self.stdout.write('Login ma\'lumotlari:')
        self.stdout.write('  admin / admin123  (superuser)')
        self.stdout.write('  fuqaro1 / fuqaro123')
        self.stdout.write('  fuqaro2 / fuqaro123')
        self.stdout.write('  hokimiyat1 / hokimiyat123')
        self.stdout.write('  hokimiyat2 / hokimiyat123')
