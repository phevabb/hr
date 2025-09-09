from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import ForeignKey
from dateutil.relativedelta import relativedelta
from datetime import date

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        """
        Create and return a regular user with a user_id and password.
        """
        if not user_id:
            raise ValueError('The User ID must be set')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        """
        Create and return a superuser with a user_id and password.
        """

        # Mandatory flags
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Default values for required fields


        return self.create_user(user_id, password, **extra_fields)

class Region(models.Model):
    region = models.CharField(max_length=120)
    class Meta:
        verbose_name_plural = 'Regions'
        verbose_name = 'Region'
    def __str__(self):
        return self.region

class Districts(models.Model):
    district = models.CharField(max_length=120)
    class Meta:
        verbose_name_plural = 'Districts'
        verbose_name = 'District'
    def __str__(self):
        return self.district

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = 'Departments'
        verbose_name = 'Department'
    def __str__(self):
        return self.department_name

class Classes(models.Model):
    classes_name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name_plural = 'Classes'
        verbose_name = 'Class'
    def __str__(self):
        return self.classes_name

class ManagementUnit(models.Model):
    management_unit_name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = 'Management Units'
        verbose_name = 'Management Unit'
    def __str__(self):
        return self.management_unit_name

class CurrentGrade(models.Model):
    current_grade = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name_plural = 'Current Grades'
        verbose_name = 'Current Grade'
    def __str__(self):
        return self.current_grade

class ChangeOfGrade(models.Model):
    grade = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = 'Change of Grades'
        verbose_name = 'Change of Grade'
    def __str__(self):
        return self.grade

# Custom User model
class User(AbstractUser):


    TITLE_CHOICES = [
        ('Esq.', 'Esq.'),
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Ms.', 'Ms.'),
    ]

    ON_LEAVE_TYPE_CHOICES = [
        ( 'NO','NO'),
        ('STUDY LEAVE WITH PAY','STUDY LEAVE WITH PAY'),
        ('STUDY LEAVE WITHOUT PAY','STUDY LEAVE WITHOUT PAY')

    ]


    ROLE_CHOICES = [
        ('Admin', "Admin"),
        ('Manager', "Manager"),
        ("Staff", "Staff"),
    ]
    PROFESSIONAL_CHOICES = [
        ('Professional', "Professional"),
        ('Subprofessional', "Subprofessional"),

    ]

    GENDER_CHOICES = [
        ('Male', "Male"),
        ('Female', "Female"),
    ]

    CLASS_CHOICES = [
        ('Accounts Class', 'Accounts Class'),
        ('Administrative Class', 'Administrative Class'),
        ('Audit Class', 'Audit Class'),
        ('General', 'General'),
        ('Drivers Class', 'Drivers Class'),
        ('Executive Class', 'Executive Class'),
        ('Information Class', 'Information Class'),
        ('Information Technology Class', 'Information Technology Class'),
        ('Labourers Class', 'Labourers Class'),
        ('Procurement Class', 'Procurement Class'),
        ('Programme Class', 'Programme Class'),
        ('Records Class', 'Records Class'),
        ('Revenue Class', 'Revenue Class'),
        ('Revenue Inspector Class', 'Revenue Inspector Class'),
        ('Sanitation Class', 'Sanitation Class'),
        ('Secretarial Class', 'Secretarial Class'),
        ('Security Class', 'Security Class'),
        ('Stool Lands Class', 'Stool Lands Class'),
        ('Stool Lands Inspectors Class', 'Stool Lands Inspectors Class'),
        ('Stool Lands Revenue Class', 'Stool Lands Revenue Class'),
    ]

    STAFF_CHOICES = [
        ('SENIOR STAFF', "SENIOR STAFF"),
        ('JUNIOR STAFF', "JUNIOR STAFF"),
    ]

    DISTRICT_CHOICES = [
        ('Accra Metropolitan Assembly', 'Accra Metropolitan Assembly'),
        ('Asunafo North', 'Asunafo North'),
        ('Sekondi-Takoradi Metropolitan Assembly', 'Sekondi-Takoradi Metropolitan Assembly'),
        ('Sekondi', 'Sekondi'),
        ('Sekondi', 'Sekondi'),  # Duplicate preserved
        ('Techiman', 'Techiman'),
        ('Mfantseman Municipal Assembly', 'Mfantseman Municipal Assembly'),
        ('Head Office', 'Head Office'),
        ('Sunyani Municipal', 'Sunyani Municipal'),
        ('Berekum', 'Berekum'),
        ('Tano North Municipal', 'Tano North Municipal'),
        ('Regional Office', 'Regional Office'),
        ('Asuogyaman District Assembly', 'Asuogyaman District Assembly'),
        ('Kade District', 'Kade District'),
        ('Nkoranza North & South', 'Nkoranza North & South'),
        ('Aowin', 'Aowin'),
        ('Abuakwa North Municipal', 'Abuakwa North Municipal'),
        ('Kwahu West', 'Kwahu West'),
        ('Kwahu West', 'Kwahu West'),  # Duplicate preserved
        ('Kwahu', 'Kwahu'),
        ('Yeji Pru East', 'Yeji Pru East'),
        ('Aowin Municipal', 'Aowin Municipal'),
        ('Birim North District', 'Birim North District'),
        ('Tano North Municipal', 'Tano North Municipal'),  # Duplicate preserved
        ('Kwahu Afram Plains South', 'Kwahu Afram Plains South'),
        ('Asuogyaman', 'Asuogyaman'),
        ('Akim Oda', 'Akim Oda'),
        ('Regional Office', 'Regional Office'),  # Duplicate preserved
        ('Accra Metropolitan Assembly', 'Accra Metropolitan Assembly'),  # Duplicate preserved
        ('Asamankese', 'Asamankese'),
        ('New Juaben South', 'New Juaben South'),
        ('Kwaebibirem Municipality', 'Kwaebibirem Municipality'),
        ('Birim South District', 'Birim South District'),
        ('Atiwa East', 'Atiwa East'),
        ('West Akim Municipal', 'West Akim Municipal'),
        ('New Abirem', 'New Abirem'),
        ('New Tafo-Akyem (Abuakwa North Municipal Assembly)', 'New Tafo-Akyem (Abuakwa North Municipal Assembly)'),
        ('Sunyani Municipal Assembly', 'Sunyani Municipal Assembly'),
        ('Asene Manso Akroso', 'Asene Manso Akroso'),
        ('Fanteakwa North District Assembly', 'Fanteakwa North District Assembly'),
        ('Asunafo North', 'Asunafo North'),  # Duplicate preserved
        ('New Juaben North', 'New Juaben North'),
        ('Aowin', 'Aowin'),  # Duplicate preserved
        ('Sunyani', 'Sunyani'),
        ('Sunyani Municipal Assembly', 'Sunyani Municipal Assembly'),  # Duplicate preserved
        ('Sunyani Municipality', 'Sunyani Municipality'),
        ('Jaman South Municipal', 'Jaman South Municipal'),
        ('Bia West', 'Bia West'),
        ('Sunyani Municipal', 'Sunyani Municipal'),  # Duplicate preserved
        ('Wenchi', 'Wenchi'),
        ('Dormaa West', 'Dormaa West'),
        ('Begoro', 'Begoro'),
        ('Banda District', 'Banda District'),
        ('Kyebi', 'Kyebi'),
        ('La Dadekotopone', 'La Dadekotopone'),
        ('Dambai', 'Dambai'),
        ('Assin Foso', 'Assin Foso'),
        ('Techiman North', 'Techiman North'),
        ('Sefwi Wiawso Municipal', 'Sefwi Wiawso Municipal'),
        ('La Dade Kotopong', 'La Dade Kotopong'),
        ('Asutifi North', 'Asutifi North'),
        ('Akim Oda', 'Akim Oda'),  # Duplicate preserved
        ('Kumasi Metropolitan Assembly', 'Kumasi Metropolitan Assembly'),
        ('Bolgatanga Municipal', 'Bolgatanga Municipal'),
        ('Asutifi North', 'Asutifi North'),  # Duplicate preserved
        ('Weija Gbawe', 'Weija Gbawe'),
        ('Jaman North', 'Jaman North'),
        ('Elubo', 'Elubo'),
        ('Kwabiberium Municipal Assembly', 'Kwabiberium Municipal Assembly'),
        ('Dormaa Municipal', 'Dormaa Municipal'),
        ('Tarkwa Nsuaem', 'Tarkwa Nsuaem'),
        ('Akyemansa', 'Akyemansa'),
        ('Kumasi', 'Kumasi'),
        ('Cape Coast', 'Cape Coast'),
        ('Asankragwa', 'Asankragwa'),
        ('Sefwi Bodi', 'Sefwi Bodi'),
        ('Daboase', 'Daboase'),
        ('Tarkwa Nsuaem', 'Tarkwa Nsuaem'),  # Duplicate preserved
        ('Sefwi Wiawso', 'Sefwi Wiawso'),
        ('Cape Coast', 'Cape Coast'),  # Duplicate preserved
        ('Kumasi Metropolitan District', 'Kumasi Metropolitan District'),
        ('Axim', 'Axim'),
        ('New Juaben South Municipal', 'New Juaben South Municipal'),
        ('New Juaben South Municipal', 'New Juaben South Municipal'),  # Duplicate preserved
        ('New Juaben North', 'New Juaben North'),
        ('Tamale Metropolitan Assembly', 'Tamale Metropolitan Assembly'),
        ('Dambai District', 'Dambai District'),
        ('Sekondi-Takoradi Metropolitan Assembly', 'Sekondi-Takoradi Metropolitan Assembly'),  # Duplicate preserved
        ('Nkwanta - South', 'Nkwanta - South'),
        ('New Juaben South', 'New Juaben South'),  # Duplicate preserved
        ('Shai Osu-Doku District', 'Shai Osu-Doku District'),
        ('Bosomtwe District', 'Bosomtwe District'),
        ('Antwima Mponua', 'Antwima Mponua'),
        ('Wassa East', 'Wassa East'),
        ('Kasoa', 'Kasoa'),
        ('Ga Central Municipality', 'Ga Central Municipality'),
        ('Bole', 'Bole'),
        ('Twifo Atti-Morkwa', 'Twifo Atti-Morkwa'),
        ('Obuasi', 'Obuasi'),
        ('Madina Municipal Branch Office', 'Madina Municipal Branch Office'),
        ('Builsa North Municipal', 'Builsa North Municipal'),
        ('Amansie West', 'Amansie West'),
        ('Madina Municipal', 'Madina Municipal'),
        ('Offinso', 'Offinso'),
        ('Sekondi-Takoradi', 'Sekondi-Takoradi'),
        ('Twifo Praso', 'Twifo Praso'),
        ('Bia East', 'Bia East'),
        ('Bibiani Anhwiaso Bekwai', 'Bibiani Anhwiaso Bekwai'),
        ('Ledzekuku-Krowor', 'Ledzekuku-Krowor'),
        ('Bolgatanga Municipal', 'Bolgatanga Municipal'),  # Duplicate preserved
        ('West Mamprusi', 'West Mamprusi'),
        ('Teshie-Nungua', 'Teshie-Nungua'),
        ('Bolgatanga Municipal Assembly', 'Bolgatanga Municipal Assembly'),
        ('Salaga', 'Salaga'),
        ('Teshie-Nungua', 'Teshie-Nungua'),  # Duplicate preserved
        ('Atwima Mponua', 'Atwima Mponua'),
        ('Bawku Municipal', 'Bawku Municipal'),
        ('Juaboso', 'Juaboso'),
        ('Bibiani', 'Bibiani'),
        ('Atwima Nwabiagya North', 'Atwima Nwabiagya North'),
        ('Bibiani, Awheaso, Bekwai', 'Bibiani, Awheaso, Bekwai'),
        ('Sekondi-Takoradi', 'Sekondi-Takoradi'),  # Duplicate preserved
        ('Kassena Nankana West', 'Kassena Nankana West'),
        ('Techiman Municipal', 'Techiman Municipal'),
        ('Kassena Nankana West', 'Kassena Nankana West'),  # Duplicate preserved
        ('Konongo', 'Konongo'),
        ('Afigya Kwabre South District', 'Afigya Kwabre South District'),
        ('Kasoa Sub-Region', 'Kasoa Sub-Region'),
        ('Secondi Takoradi', 'Secondi Takoradi'),
        ('Jomoro', 'Jomoro'),
        ('Kumasi Metropolitan', 'Kumasi Metropolitan'),
        ('Prestea-Huni Valley', 'Prestea-Huni Valley'),
        ('Adansi South District', 'Adansi South District'),
        ('Madina District', 'Madina District'),
        ('Wassa Akropong', 'Wassa Akropong'),
        ('Kwabre East Municipal', 'Kwabre East Municipal'),
        ('Osu Klottey', 'Osu Klottey'),
        ('Tano South', 'Tano South'),
        ('Kumasi', 'Kumasi'),  # Duplicate preserved
        ('Asante Mampong Municipality', 'Asante Mampong Municipality'),
        ('Sekyere South', 'Sekyere South'),
        ('Atwima Kwanwoma District', 'Atwima Kwanwoma District'),
        ('Suaman', 'Suaman'),
        ('Kumasi Metro', 'Kumasi Metro'),
        ('Ahafo Ano North', 'Ahafo Ano North'),
        ('Agona Swedru', 'Agona Swedru'),
        ('Asunafo North Municipal Assembly', 'Asunafo North Municipal Assembly'),
        ('Awutu Senya West', 'Awutu Senya West'),
        ('Nkawie', 'Nkawie'),
        ('Asunafo South', 'Asunafo South'),
        ('Accra Metropolitan', 'Accra Metropolitan'),
        ('Kumasi Metropolitan Assembly', 'Kumasi Metropolitan Assembly'),  # Duplicate preserved
        ('Adansi South', 'Adansi South'),
        ('Tano South', 'Tano South'),  # Duplicate preserved
        ('Sekyere-East District', 'Sekyere-East District'),
        ('Asunafo North Municipal', 'Asunafo North Municipal'),
        ('Nzema East Municipal', 'Nzema East Municipal'),
        ('Accra Metropolitan', 'Accra Metropolitan'),  # Duplicate preserved
        ('Asutifi South', 'Asutifi South'),
        ('Asikuma Odoben Brakwa', 'Asikuma Odoben Brakwa'),
        ('Awutu Senya East Municipal Assembly', 'Awutu Senya East Municipal Assembly'),
        ('Sefwi Wiawso', 'Sefwi Wiawso'),  # Duplicate preserved
        ('Asokore Mampong', 'Asokore Mampong'),
        ('Ejisu Municipal', 'Ejisu Municipal'),
        ('Suame', 'Suame'),
        ('Ejura-Sekyedumase', 'Ejura-Sekyedumase'),
        ('Accra', 'Accra'),
        ('Prampram', 'Prampram'),
        ('Kumasi Metropolitan', 'Kumasi Metropolitan'),  # Duplicate preserved
        ('Offinso North District', 'Offinso North District'),
        ('Madina', 'Madina'),
        ('Ahafo Ano South', 'Ahafo Ano South'),
        ('Bosomtwe', 'Bosomtwe'),
        ('Sekyere Kumawu', 'Sekyere Kumawu'),
        ('Sefwi Wiawso Municipal Assembly', 'Sefwi Wiawso Municipal Assembly'),
        ('Game North', 'Game North'),
        ('La Dadekotopon', 'La Dadekotopon'),
        ('Dunkwa-On-Offin', 'Dunkwa-On-Offin'),
        ('La-Dadekotopo', 'La-Dadekotopo'),
        ('Sunyani East Municipality', 'Sunyani East Municipality'),
        ('Sunyani', 'Sunyani'),  # Duplicate preserved
        ('Dormaa Central', 'Dormaa Central'),
        ('Madina  Municipal Branch Office', 'Madina  Municipal Branch Office'),
        ('Kintampo South', 'Kintampo South'),
        ('Atebubu Accra Metropolitan Assemblyntin', 'Atebubu Accra Metropolitan Assemblyntin'),  # Typo preserved
        ('Kintampo North', 'Kintampo North')
    ]

    REGION_CHOICES = (
        ('AHAFO', 'AHAFO'),
        ('ASHANTI', 'ASHANTI'),
        ('BONO & BONO EAST', 'BONO & BONO EAST'),
        ('CENTRAL', 'CENTRAL'),
        ('EASTERN', 'EASTERN'),
        ('GREATER ACCRA', 'GREATER ACCRA'),
        ('HEAD OFFICE', 'HEAD OFFICE'),
        ('NORTHERN', 'NORTHERN'),
        ('UPPER EAST', 'UPPER EAST'),
        ('WESTERN', 'WESTERN'),
        ('Greater Accra', 'Greater Accra'),
        ('WESTERN NORTH', 'WESTERN NORTH'),
    )
    POSITION_CHOICES = [
        ('Accountant', 'Accountant'),
        ('Administrator Of Stool Lands', 'Administrator Of Stool Lands'),
        ('Assistant Accountant', 'Assistant Accountant'),
        ('Assistant Chief Executive Officer', 'Assistant Chief Executive Officer'),
        ('Assistant Chief Stool Lands Inspector', 'Assistant Chief Stool Lands Inspector'),
        ('Assistant Director IIA', 'Assistant Director IIA'),
        ('Assistant Director IIB', 'Assistant Director IIB'),
        ('Assistant Information Officer', 'Assistant Information Officer'),
        ('Assistant Internal Auditor', 'Assistant Internal Auditor'),
        ('Assistant Procurement & Supply Chain Manager', 'Assistant Procurement & Supply Chain Manager'),
        ('Assistant Stool Lands Officer', 'Assistant Stool Lands Officer'),
        ('Chief Accountant', 'Chief Accountant'),
        ('Chief Executive Officer', 'Chief Executive Officer'),
        ('Chief Headman', 'Chief Headman'),
        ('Chief Headman Labourer', 'Chief Headman Labourer'),
        ('Chief Revenue Superintendent', 'Chief Revenue Superintendent'),
        ('Chief Stool Lands Inspector', 'Chief Stool Lands Inspector'),
        ('Chief Stool Lands Officer', 'Chief Stool Lands Officer'),
        ('Deputy Chief Stool Lands Inspector', 'Deputy Chief Stool Lands Inspector'),
        ('Deputy Chief Stool Lands Officer', 'Deputy Chief Stool Lands Officer'),
        ('Deputy Director', 'Deputy Director'),
        ('Deputy Stool Lands Inspector', 'Deputy Stool Lands Inspector'),
        ('Deputy Stool Lands Officer', 'Deputy Stool Lands Officer'),
        ('Driver Grade I', 'Driver Grade I'),
        ('Driver Grade II', 'Driver Grade II'),
        ('Driver Grade III', 'Driver Grade III'),
        ('Executive Officer', 'Executive Officer'),
        ('Headman', 'Headman'),
        ('Heavy Duty', 'Heavy Duty'),
        ('Higher Executive Officer', 'Higher Executive Officer'),
        ('Higher Revenue Inspector', 'Higher Revenue Inspector'),
        ('Internal Auditor', 'Internal Auditor'),
        ('IT/IM Officer', 'IT/IM Officer'),
        ('Principal Account Technician', 'Principal Account Technician'),
        ('Principal Accountant', 'Principal Accountant'),
        ('Principal Executive Officer', 'Principal Executive Officer'),
        ('Principal Procurement & Supply Chain Manager', 'Principal Procurement & Supply Chain Manager'),
        ('Principal Revenue Superintendent', 'Principal Revenue Superintendent'),
        ('Principal Stool Lands Inspector', 'Principal Stool Lands Inspector'),
        ('Principal Stool Lands Officer', 'Principal Stool Lands Officer'),
        ('Private Secretary', 'Private Secretary'),
        ('Procurement & Supply Chain Officer', 'Procurement & Supply Chain Officer'),
        ('Programme Officer', 'Programme Officer'),
        ('Records Officer', 'Records Officer'),
        ('Revenue', 'Revenue'),
        ('Revenue Collector', 'Revenue Collector'),
        ('Revenue Inspector', 'Revenue Inspector'),
        ('Revenue Superintendent', 'Revenue Superintendent'),
        ('Sanitary Labourer', 'Sanitary Labourer'),
        ('Senior Accountant', 'Senior Accountant'),
        ('Senior Executive Officer', 'Senior Executive Officer'),
        ('Senior Private Secretary', 'Senior Private Secretary'),
        ('Senior Records Officer', 'Senior Records Officer'),
        ('Senior Revenue Superintendent', 'Senior Revenue Superintendent'),
        ('Senior Stool Lands Officer', 'Senior Stool Lands Officer'),
        ('Ss11', 'Ss11'),
        ('Stenographer Grade I', 'Stenographer Grade I'),
        ('Stenographer Grade II', 'Stenographer Grade II'),
        ('Stenographer Secretary', 'Stenographer Secretary'),
        ('Stool Lands Inspector', 'Stool Lands Inspector'),
        ('Stool Lands Officer', 'Stool Lands Officer'),
        ('Watchman Night', 'Watchman Night'),
        ('Yard Foreman', 'Yard Foreman'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
    ]
    CHANGE_OF_GRADE_CHOICES = [
        ('First Appointment', 'First Appointment'),
        ('High Academic Qualification', 'High Academic Qualification'),
        ('Letter Of Appointment', 'Letter Of Appointment'),
        ('None', 'None'),
        ('Promotion', 'Promotion'),
        ('Regrading (Conversion/Upgrading)', 'Regrading (Conversion/Upgrading)'),
    ]
    CONTRACT_FULLTIME = [
        ('FULLTIME', 'FULLTIME'),
        ('CONTRACT', 'CONTRACT'),
    ]
    MANAGEMENT_UNIT_CHOICES = [
        ('0101 ASL: Office Of The Admin Of Stool Lands', '0101 ASL: Office Of The Admin Of Stool Lands'),
        ('0101 MOC: Info. Services Dept. Head O COST CENTER', '0101 MOC: Info. Services Dept. Head O COST CENTER'),
        ('0613 ASL: ADMIN. OF STOOL LANDS, KUMASI', '0613 ASL: ADMIN. OF STOOL LANDS, KUMASI'),
        ('0408 ASL: Admin Of Stool Lands-Sekondi', '0408 ASL: Admin Of Stool Lands-Sekondi'),
        ('0712 ASL Admin Of Stool Lands Sunyani', '0712 ASL Admin Of Stool Lands Sunyani'),
        ('0313 ASL: Admin of stool lands Cape C Coast CENTRE', '0313 ASL: Admin of stool lands Cape C Coast CENTRE'),
        ('0600 REGIONAL ADMINI: ASHANTI REGIONAL', '0600 REGIONAL ADMINI: ASHANTI REGIONAL'),
        ('0208 ASL:ADMIN OF STOOL LANDS,KOFORIDUA COST CENTRE', '0208 ASL:ADMIN OF STOOL LANDS,KOFORIDUA COST CENTRE'),
        ('0101 OHCS: PROCUREMENT AND SUPPLY CHAIN COST CENTRE', '0101 OHCS: PROCUREMENT AND SUPPLY CHAIN COST CENTRE'),
        ('0408 LGS SEKONDI TAKORADI METRO. ASSEMBLY', '0408 LGS SEKONDI TAKORADI METRO. ASSEMBLY'),
        ('0101 CAGD/MT Stool Lands', '0101 CAGD/MT Stool Lands'),
        ('0101 ASL: Admin Of Stool Lands, Accra', '0101 ASL: Admin Of Stool Lands, Accra'),
        ('310 MOF/CAGD CENTRAL REGIONAL DIRECT', '310 MOF/CAGD CENTRAL REGIONAL DIRECT'),
        ('0712 ASL:ADMIN OF STOOL LANDS SUNYANI', '0712 ASL:ADMIN OF STOOL LANDS SUNYANI'),
        ('0313: Administrator of Stool Lands - Cape Coast', '0313: Administrator of Stool Lands - Cape Coast'),
        ('0200MOF/CAGD-Eastern Regional Directorate', '0200MOF/CAGD-Eastern Regional Directorate'),
        ('0600 MOF/CAGD: ASHANTIREGIONAL DIRECT.', '0600 MOF/CAGD: ASHANTIREGIONAL DIRECT.'),
        ('0813 ASL: Admin Of Stool Lands, TAccra Metropolitan Assemblyle',
         '0813 ASL: Admin Of Stool Lands, TAccra Metropolitan Assemblyle'),
        ('0400 MOF/CAGD WESTERN REGIONAL DIRECT', '0400 MOF/CAGD WESTERN REGIONAL DIRECT'),
        ('0313', '0313'),
        ('0800/LGS: NORTHERN REGIONAL COORDINATING COST CENTRE',
         '0800/LGS: NORTHERN REGIONAL COORDINATING COST CENTRE'),
        ('Administrator of Stool Lands -Western North Region', 'Administrator of Stool Lands -Western North Region'),
        ('0400 LGS WESTERN REGIONAL COORDINATING COUNCIL', '0400 LGS WESTERN REGIONAL COORDINATING COUNCIL'),
        ('0400MOF/CAGD:WESTERN REGIONAL DIRECT COST CENTRE', '0400MOF/CAGD:WESTERN REGIONAL DIRECT COST CENTRE'),
        ('MOF/CAGD: WESTERN REGIONAL DIRECTORATE', 'MOF/CAGD: WESTERN REGIONAL DIRECTORATE'),
        ('Office of of the Administrator of Stool Lands - Western North Region',
         'Office of of the Administrator of Stool Lands - Western North Region'),
        ('0313 Administrator of Stool Lands', '0313 Administrator of Stool Lands'),
        ('Office of the Administrator of Stool Lands -Western North Region',
         'Office of the Administrator of Stool Lands -Western North Region'),
        ('0313 Administrator of Stool Lands', '0313 Administrator of Stool Lands'),
        ('OASL WESTERN NORTH', 'OASL WESTERN NORTH'),
        ('OASL.WESTERN NORTH REGION', 'OASL.WESTERN NORTH REGION'),
        ('0600 REGIONAL ADMINI: ASHANTI REGIONAL', '0600 REGIONAL ADMINI: ASHANTI REGIONAL'),
        ('0313 ASL: Admin of Stool Lands, Cape C COST CENTRE', '0313 ASL: Admin of Stool Lands, Cape C COST CENTRE'),
        ('Adm. of Stool Lands, Kumasi Cost Centre', 'Adm. of Stool Lands, Kumasi Cost Centre'),
        ('310 MOF/CAGD UPPER DENKYIRA EAST MUNCIPAL', '310 MOF/CAGD UPPER DENKYIRA EAST MUNCIPAL'),
        ('1300 CAGD Ahafo regional Directorate COST CENTRE', '1300 CAGD Ahafo regional Directorate COST CENTRE'),
        ('0313 ASL: Admin of Stool Lands, Cape C COST CENTRE', '0313 ASL: Admin of Stool Lands, Cape C COST CENTRE'),
        ('OASL District Officers Conference - Ejisu', 'OASL District Officers Conference - Ejisu'),
        ('0101 MLF (OASL)', '0101 MLF (OASL)'),
        ('0313 ASL: Admin of stool lands, Cape coast center', '0313 ASL: Admin of stool lands, Cape coast center'),
        ('0101 PG: Parks And Gardens HQ', '0101 PG: Parks And Gardens HQ')
    ]
    ACCOMMODATION_STATUS_CHOICES = [
        ('PERSONAL', 'PERSONAL'),
        ('RENTED', 'RENTED'),
        ('OFFICIAL RESIDENCE - OASL', 'OFFICIAL RESIDENCE - OASL'),
        ('OFFICIAL RESIDENCE - OASL', 'OFFICIAL RESIDENCE - OASL'),
        ('OFFICIAL RESIDENCE - GoG', 'OFFICIAL RESIDENCE - GoG'),
        ('OFFICIAL RESIDENCE - GoG', 'OFFICIAL RESIDENCE - GoG'),
    ]

    username = None  # Remove username
    directorate = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Directorate',related_name = 'directorates'    )
    category = models.ForeignKey( Classes, on_delete=models.SET_NULL, verbose_name="class", null=True, blank=True, related_name = 'categories')
    district = models.ForeignKey( Districts,  on_delete=models.SET_NULL, verbose_name="District", null=True, blank=True, related_name = 'districts')
    region = models.ForeignKey( Region, on_delete=models.SET_NULL, verbose_name='Region',  null=True, blank=True, related_name = 'regions')
    current_grade = models.ForeignKey( CurrentGrade,on_delete=models.SET_NULL, null=True, verbose_name='current grade', blank=True, related_name = 'current_gradee')
    next_grade = models.ForeignKey( CurrentGrade, on_delete=models.SET_NULL, null=True, verbose_name='next grade', blank=True, related_name = 'next_gradee')
    change_of_grade = models.ForeignKey( ChangeOfGrade, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'change_of_gradee')
    management_unit_cost_centre = models.ForeignKey( ManagementUnit, on_delete=models.SET_NULL, blank=True, null=True,  related_name = 'management_unitt')


    user_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    title = models.CharField(max_length=20, choices=TITLE_CHOICES, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    maiden_name = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, db_index=True)
    
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    professional = models.CharField(max_length=50, choices=PROFESSIONAL_CHOICES, null=True, blank=True)
    current_salary_level = models.CharField(max_length=20, null=True, blank=True)
    current_salary_point = models.CharField(max_length=20, null=True, blank=True)
    next_salary_level = models.CharField(max_length=20, null=True, blank=True)
    date_of_first_appointment = models.DateField(null=True, blank=True)
    date_of_assumption_of_duty = models.DateField(null=True, blank=True)
    date_of_last_promotion = models.DateField(null=True, blank=True)
    substantive_date = models.DateField(null=True, blank=True)
    national_effective_date = models.DateField(null=True, blank=True)
    years_on_current_grade = models.IntegerField(null=True, blank=True)
    number_of_years_in_service = models.IntegerField(null=True, blank=True)
    fulltime_contract_staff = models.CharField(max_length=100, choices=CONTRACT_FULLTIME, null=True, blank=True)
    academic_qualification = models.CharField(max_length=100, null=True, blank=True)
    professional_qualification = models.CharField(max_length=100, null=True, blank=True)
    staff_category = models.CharField(max_length=20, choices=STAFF_CHOICES, null=True, blank=True)

    single_spine_monthly_salary = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    monthly_gross_pay = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    annual_salary = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    number_of_focus_areas = models.IntegerField(null=True, blank=True)
    number_of_targets = models.IntegerField(null=True, blank=True)
    number_of_targets_met = models.IntegerField(null=True, blank=True)
    number_of_targets_not_met = models.IntegerField(null=True, blank=True)
    overall_assessment_score = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    self_assessment_description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    ghana_card_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    social_security_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    national_health_insurance_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_account_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    bank_account_branch = models.CharField(max_length=100, null=True, blank=True)
    payroll_status = models.CharField(max_length=50, choices=(('ACTIVE (PAID)', 'ACTIVE (PAID)'), ('Inactive', 'Inactive'),
                                                              ('Suspended', 'Suspended')), null=True, blank=True)
    at_post_on_leave = models.CharField(max_length=20, choices=(('AT POST', 'AT POST'), ('ON LEAVE', 'ON LEAVE')),null=True, blank=True)
    on_leave_type = models.CharField(max_length=50, blank=True, null=True, choices=ON_LEAVE_TYPE_CHOICES)
    accommodation_status = models.CharField(max_length=50, choices=ACCOMMODATION_STATUS_CHOICES, null=True, blank=True)
    supervisor_name = models.CharField(max_length=100, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/",  # Folder inside MEDIA_ROOT
        blank=True,
        null=True
    )
    standard_retirement_age = 60
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []  # No required fields
    objects = CustomUserManager()

    @property
    def date_of_retirement(self):
        """Retirement date is 60 years after date_of_birth"""
        if self.date_of_birth:
            return self.date_of_birth + relativedelta(years=self.standard_retirement_age)
        return None
    

    @property
    def age(self):
        """Calculate current age from date_of_birth"""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    @property
    def full_name(self):
        names = []
        if self.first_name:
            names.append(self.first_name)
        if self.middle_name and self.middle_name.lower() != "none":
            names.append(self.middle_name)
        if self.last_name:
            names.append(self.last_name)
        return " ".join(names).strip()


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user_id}"


