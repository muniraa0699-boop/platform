from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CITIZEN = 'fuqaro'
    ROLE_AUTHORITY = 'hokimiyat'
    ROLE_CHOICES = [
        (ROLE_CITIZEN, 'Fuqaro'),
        (ROLE_AUTHORITY, 'Hokimiyat xodimi'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CITIZEN, verbose_name="Rol")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    is_authority_approved = models.BooleanField(default=True, verbose_name="Tasdiqlangan")

    def is_citizen(self):
        return self.role == self.ROLE_CITIZEN

    def is_authority(self):
        return self.role == self.ROLE_AUTHORITY

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


VILOYATLAR = [
    ('toshkent_sh', "Toshkent shahri"),
    ('toshkent', "Toshkent viloyati"),
    ('samarqand', "Samarqand viloyati"),
    ('buxoro', "Buxoro viloyati"),
    ('andijon', "Andijon viloyati"),
    ('fargona', "Farg'ona viloyati"),
    ('namangan', "Namangan viloyati"),
    ('qashqadaryo', "Qashqadaryo viloyati"),
    ('surxondaryo', "Surxondaryo viloyati"),
    ('navoiy', "Navoiy viloyati"),
    ('xorazm', "Xorazm viloyati"),
    ('jizzax', "Jizzax viloyati"),
    ('sirdaryo', "Sirdaryo viloyati"),
    ('qoraqalpogiston', "Qoraqalpog'iston Respublikasi"),
]

TUMANLAR = {
    'toshkent_sh': ['Yunusobod', 'Chilonzor', 'Mirobod', 'Yakkasaroy', 'Shayxontohur', 'Olmazor', 'Uchtepa', 'Bektemir', 'Sergeli', 'Mirzo Ulug\'bek', 'Yashnobod'],
    'toshkent': ['Angren', 'Bekabad', 'Bo\'stonliq', 'Buka', 'Chinoz', 'Qibray', 'O\'rtachirchiq', 'Oqqo\'rg\'on', 'Parkent', 'Piskent', 'Quyi Chirchiq', 'Ohangaron', 'Toshkent tumani', 'Yuqori Chirchiq', 'Zangiota'],
    'samarqand': ['Samarqand', 'Urgut', 'Kattaqo\'rg\'on', 'Bulung\'ur', 'Ishtixon', 'Jomboy', 'Qo\'shrabot', 'Narpay', 'Nurobod', 'Oqdaryo', 'Pastdarg\'om', 'Payariq', 'Posyon', 'Tayloq', 'Toyloq'],
    'buxoro': ['Buxoro', 'G\'ijduvon', 'Jondor', 'Kogon', 'Qorovulbozor', 'Peshku', 'Romitan', 'Shofirkon', 'Vobkent'],
    'andijon': ['Andijon', 'Asaka', 'Baliqchi', 'Bo\'z', 'Buloqboshi', 'Jalaquduq', 'Izboskan', 'Xo\'jaobod', 'Marhamat', 'Oltinko\'l', 'Paxtaobod', 'Qo\'rg\'ontepa', 'Shahrixon', 'Ulug\'nor'],
    'fargona': ['Farg\'ona', 'Qo\'qon', 'Marg\'ilon', 'Beshariq', 'Buvayda', 'Dang\'ara', 'Furqat', 'Oltiariq', 'Bag\'dod', 'Quva', 'Rishton', 'So\'x', 'Toshloq', 'Uchko\'prik', 'O\'zbekiston', 'Yozyovon'],
    'namangan': ['Namangan', 'Chortoq', 'Chust', 'Kosonsoy', 'Ming\'buloq', 'Norin', 'Pop', 'To\'raqo\'rg\'on', 'Uychi', 'Yangiqo\'rg\'on'],
    'qashqadaryo': ['Qarshi', 'G\'uzor', 'Dehqonobod', 'Kasbi', 'Koson', 'Kitob', 'Muborak', 'Nishon', 'Shahrisabz', 'Yakkabog\''],
    'surxondaryo': ['Termiz', 'Angor', 'Bandixon', 'Boysun', 'Denov', 'Jarqo\'rg\'on', 'Muzrabot', 'Oltinsoy', 'Qumqo\'rg\'on', 'Sariosiyo', 'Sherobod', 'Sho\'rchi', 'Uzun'],
    'navoiy': ['Navoiy', 'Karmana', 'Konimex', 'Nurota', 'Tomdi', 'Uchquduq', 'Xatirchi'],
    'xorazm': ['Urganch', 'Bog\'ot', 'Gurlan', 'Xazarasp', 'Xiva', 'Xonqa', 'Qo\'shko\'pir', 'Shovot', 'Yangiariq', 'Yangibozor'],
    'jizzax': ['Jizzax', 'Arnasoy', 'Baxmal', 'Do\'stlik', 'Forish', 'G\'allaorol', 'Mirzacho\'l', 'Paxtakor', 'Sharof Rashidov', 'Yangiobod', 'Zafarobod', 'Zarbdor', 'Zomin'],
    'sirdaryo': ['Guliston', 'Baxt', 'Boyovut', 'Havast', 'Mirzaobod', 'Oqoltin', 'Sardoba', 'Sayxunobod', 'Shirin', 'Xovos'],
    'qoraqalpogiston': ['Nukus', 'Amudaryo', 'Beruniy', 'Chimboy', 'Ellikkala', 'Kegeyli', 'Mo\'ynoq', 'Nukus tumani', 'Qanliko\'l', 'Qorao\'zak', 'Shumanay', 'Taxtako\'pir', 'To\'rtko\'l', 'Xo\'jayli'],
}


class WasteReport(models.Model):
    STATUS_PENDING = 'kutilmoqda'
    STATUS_ACCEPTED = 'qabul_qilindi'
    STATUS_IN_PROGRESS = 'jarayonda'
    STATUS_CLEANING = 'tozalanmoqda'
    STATUS_DONE = 'tozalandi'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Kutilmoqda'),
        (STATUS_ACCEPTED, 'Qabul qilindi'),
        (STATUS_IN_PROGRESS, 'Ko\'rib chiqilmoqda'),
        (STATUS_CLEANING, 'Tozalanmoqda'),
        (STATUS_DONE, 'Tozalandi'),
    ]

    WASTE_TYPE_CHOICES = [
        ('uy', 'Uy chiqindisi'),
        ('qurilish', 'Qurilish chiqindisi'),
        ('plastik', 'Plastmassa/Plastik'),
        ('xavfli', 'Xavfli chiqindilar'),
        ('boshqa', 'Boshqa'),
    ]

    SIZE_CHOICES = [
        ('kichik', 'Kichik'),
        ('orta', "O'rta"),
        ('katta', 'Katta'),
    ]

    citizen = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports', verbose_name="Fuqaro")
    latitude = models.FloatField(verbose_name="Kenglik")
    longitude = models.FloatField(verbose_name="Uzunlik")
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPE_CHOICES, verbose_name="Chiqindi turi")
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, verbose_name="Hajmi")
    description = models.TextField(blank=True, verbose_name="Izoh")
    image = models.ImageField(upload_to='reports/', blank=True, null=True, verbose_name="Rasm")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name="Holati")
    viloyat = models.CharField(max_length=50, choices=VILOYATLAR, blank=True, verbose_name="Viloyat")
    tuman = models.CharField(max_length=100, blank=True, verbose_name="Tuman")
    address = models.CharField(max_length=255, blank=True, verbose_name="Manzil")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_reports', verbose_name="Mas'ul xodim"
    )
    authority_note = models.TextField(blank=True, verbose_name="Hokimiyat izohi")

    def get_status_color(self):
        colors = {
            self.STATUS_PENDING: 'red',
            self.STATUS_ACCEPTED: 'orange',
            self.STATUS_IN_PROGRESS: 'yellow',
            self.STATUS_CLEANING: 'blue',
            self.STATUS_DONE: 'green',
        }
        return colors.get(self.status, 'gray')

    def get_marker_color(self):
        colors = {
            self.STATUS_PENDING: '#ef4444',
            self.STATUS_ACCEPTED: '#f97316',
            self.STATUS_IN_PROGRESS: '#eab308',
            self.STATUS_CLEANING: '#3b82f6',
            self.STATUS_DONE: '#22c55e',
        }
        return colors.get(self.status, '#6b7280')

    def __str__(self):
        return f"#{self.pk} - {self.get_waste_type_display()} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Chiqindi xabari"
        verbose_name_plural = "Chiqindi xabarlari"
        ordering = ['-created_at']


class Notification(models.Model):
    TYPE_NEW_REPORT = 'yangi_xabar'
    TYPE_STATUS_CHANGED = 'holat_ozgardi'
    TYPE_ASSIGNED = 'tayinlandi'

    TYPE_CHOICES = [
        (TYPE_NEW_REPORT, 'Yangi xabar'),
        (TYPE_STATUS_CHANGED, 'Holat o\'zgardi'),
        (TYPE_ASSIGNED, 'Tayinlandi'),
    ]

    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications', verbose_name="Qabul qiluvchi")
    report = models.ForeignKey(WasteReport, on_delete=models.CASCADE, related_name='notifications', verbose_name="Xabar")
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name="Turi")
    message = models.TextField(verbose_name="Xabar matni")
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    def __str__(self):
        return f"{self.recipient} - {self.message[:50]}"

    class Meta:
        verbose_name = "Bildirishnoma"
        verbose_name_plural = "Bildirishnomalar"
        ordering = ['-created_at']
