import os
import django
from django.core.management.base import BaseCommand
from account.models import User, Department, Classes, CurrentGrade, ChangeOfGrade, Region, Districts, ManagementUnit
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Import HR data from Excel spreadsheet safely'

    def handle(self, *args, **options):
        # Safe string conversion
        def safe_str(value):
            if pd.isna(value):
                return ''
            return str(value).strip()

        # Convert date safely
        def convert_date(value):
            if pd.isna(value) or str(value).strip().upper() in ['', 'NONE', 'NIL', 'NOTIONAL EFFECTIVE DATE']:
                return None
            value = str(value).strip()
            for fmt in ('%d-%b-%y', '%d-%b-%Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y', '%m-%d-%Y'):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
            try:
                if value.replace('.', '', 1).isdigit():
                    return pd.to_datetime(float(value), unit='D', origin='1899-12-30').date()
            except:
                return None
            return None

        # Convert to int
        def convert_int(value):
            if pd.isna(value) or str(value).strip().upper() in ['', 'NONE', 'NIL']:
                return 0
            try:
                return int(float(value))
            except:
                return 0

        # Convert currency to float
        def convert_currency(value):
            if pd.isna(value) or str(value).strip().upper() in ['', 'NONE', 'NIL']:
                return 0.0
            value = str(value).strip()
            if '%' in value:
                try:
                    return float(value.replace('%', '')) / 100
                except:
                    return 0.0
            try:
                return float(value.replace(',', ''))
            except:
                return 0.0

        # Resolve foreign key safely
        def get_fk_instance(model, value, row_num, field_name, lookup_field):
            if not value:
                return None
            try:
                return model.objects.get(**{lookup_field: value})
            except model.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Row {row_num + 1}: No matching {model.__name__} for "{value}" in field "{field_name}"'))
                return None
            except model.MultipleObjectsReturned:
                self.stdout.write(self.style.WARNING(f'Row {row_num + 1}: Multiple {model.__name__} found for "{value}" in field "{field_name}", using first'))
                return model.objects.filter(**{lookup_field: value}).first()

        # Find Excel file
        excel_paths = [
            "HR_DataBase_Dev.xlsx",
            os.path.join("account", "management", "commands", "HR_DataBase_Dev.xlsx")
        ]
        for path in excel_paths:
            if os.path.exists(path):
                excel_path = path
                break
        else:
            raise FileNotFoundError("Could not find HR_DataBase_Dev.xlsx")

        df = pd.read_excel(excel_path, sheet_name='Sheet1')
        self.stdout.write(f"Columns found: {', '.join(df.columns)}")

        created_count = 0
        skipped_count = 0
        error_count = 0
        skipped_users = []

        for index, row in df.iterrows():
            try:
                staff_id = safe_str(row.get('STAFF ID'))
                if not staff_id:
                    skipped_count += 1
                    skipped_users.append((index + 1, "No STAFF ID"))
                    continue
                if User.objects.filter(user_id=staff_id).exists():
                    skipped_count += 1
                    skipped_users.append((index + 1, f"Duplicate STAFF ID: {staff_id}"))
                    continue

                # Resolve foreign keys
                directorate = get_fk_instance(Department, safe_str(row.get('DIRECTORATE/DEPARTMENT/UNIT')), index, 'directorate', 'department_name')
                category = get_fk_instance(Classes, safe_str(row.get('CLASS')), index, 'category', 'classes_name')
                current_grade = get_fk_instance(CurrentGrade, safe_str(row.get('CURRENT GRADE')), index, 'current_grade', 'current_grade')
                next_grade = get_fk_instance(CurrentGrade, safe_str(row.get('NEXT GRADE')), index, 'next_grade', 'current_grade')
                change_of_grade = get_fk_instance(ChangeOfGrade, safe_str(row.get('CHANGE OF GRADE')), index, 'change_of_grade', 'grade')
                region = get_fk_instance(Region, safe_str(row.get('REGION')), index, 'region', 'region')
                district = get_fk_instance(Districts, safe_str(row.get('DISTRICT')), index, 'district', 'district')
                management_unit = get_fk_instance(ManagementUnit, safe_str(row.get('MANAGEMENT UNIT/COST CENTRE')), index, 'management_unit', 'management_unit_name')

                date_of_first_appointment = convert_date(row.get('DATE OF FIRST APPOINTMENT')) or datetime.now().date()
                national_effective_date = convert_date(row.get('NOTIONAL EFFECTIVE DATE')) or date_of_first_appointment

                nhis_number = safe_str(row.get('NATIONAL HEALTH INSURANCE NO.')) or None

                user = User(
                    user_id=staff_id,
                    title=safe_str(row.get('TITLE')),
                    first_name=safe_str(row.get('FIRST_NAME')),
                    last_name=safe_str(row.get('LAST_NAME')),
                    middle_name=safe_str(row.get('MIDDLE_NAME')),
                    maiden_name=safe_str(row.get('MAIDEN_NAME')),
                    gender=safe_str(row.get('GENDER')),
                    role='Staff',
                    date_of_birth=convert_date(row.get('DATE OF BIRTH (MM/DD/YYYY)')),
                    age=convert_int(row.get('AGE')),
                    marital_status=safe_str(row.get('MARITAL STATUS')) or 'Single',
                    category=category,
                    directorate=directorate,
                    current_grade=current_grade,
                    next_grade=next_grade,
                    change_of_grade=change_of_grade,
                    region=region,
                    district=district,
                    management_unit_cost_centre=management_unit,
                    current_salary_level=safe_str(row.get('CURRENT SALARY LEVEL')),
                    current_salary_point=safe_str(row.get('CURRENT SALARY POINT')),
                    next_salary_level=safe_str(row.get('NEXT SALARY LEVEL')),
                    date_of_first_appointment=date_of_first_appointment,
                    date_of_assumption_of_duty=convert_date(row.get('DATE OF ASSUMPTION OF DUTY')),
                    date_of_last_promotion=convert_date(row.get('DATE OF LAST PROMOTION')),
                    substantive_date=convert_date(row.get('SUBSTANTIVE DATE')),
                    national_effective_date=national_effective_date,
                    years_on_current_grade=convert_int(row.get('YEARS ON CURRENT GRADE')),
                    number_of_years_in_service=convert_int(row.get('NUMBER OF YEARS IN THE SERVICE')),
                    fulltime_contract_staff=safe_str(row.get('FULLTIME/CONTRACT STAFF')) or 'FULLTIME',
                    academic_qualification=safe_str(row.get('ACADEMIC QUALIFICATION')),
                    professional_qualification=safe_str(row.get('PROFESSIONAL QUALIFICATION')),
                    staff_category=safe_str(row.get('STAFF CATEGORY')),
                    single_spine_monthly_salary=convert_currency(row.get('SINGLE SPINE MONTHLY SALARY')),
                    monthly_gross_pay=convert_currency(row.get('MONTHLY GROSS PAY')),
                    annual_salary=convert_currency(row.get('ANNUAL SALARY')),
                    phone_number=safe_str(row.get('PHONE NO.')),
                    ghana_card_number=safe_str(row.get('GHANA CARD NUMBER')),
                    social_security_number=safe_str(row.get('SOCIAL SECURITY NO.')),
                    national_health_insurance_number=nhis_number,
                    bank_name=safe_str(row.get('BANK NAME')),
                    bank_account_number=safe_str(row.get('BANK ACCOUNT NO.')),
                    bank_account_branch=safe_str(row.get('BANK ACCOUNT BRANCH')),
                    payroll_status=safe_str(row.get('PAYROLL STATUS')) or 'Active',
                    at_post_on_leave=safe_str(row.get('AT POST / ON LEAVE')) or 'At Post',
                    on_leave_type=safe_str(row.get('ON LEAVE TYPE')),
                    accommodation_status=safe_str(row.get('ACCOMODATION STATUS')),
                    supervisor_name=safe_str(row.get("SUPERVISOR'S NAME")),
                    is_active=True,
                )

                user.set_password('Securepassword123!')
                user.save()
                created_count += 1

            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'Error importing row {index + 1}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'\nImport completed: {created_count} created, {skipped_count} skipped, {error_count} errors'))
        if skipped_users:
            self.stdout.write(self.style.WARNING("Skipped Records Details:"))
            for row_num, reason in skipped_users:
                self.stdout.write(f" - Row {row_num}: {reason}")
