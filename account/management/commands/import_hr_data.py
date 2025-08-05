import os
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from account.models import User
import pandas as pd
from datetime import datetime


class Command(BaseCommand):
    help = 'Import HR data from Excel spreadsheet'

    def handle(self, *args, **options):
        # Try multiple possible file locations
        excel_paths = [
            "HR_DataBase_Dev.xlsx",
            os.path.join("account", "management", "commands", "HR_DataBase_Dev.xlsx")
        ]

        for path in excel_paths:
            if os.path.exists(path):
                excel_path = path
                break
        else:
            raise FileNotFoundError("Could not find HR_DataBase_Dev.xlsx in any expected location")

        try:
            # Load the Excel file
            df = pd.read_excel(excel_path, sheet_name='Sheet1')

            self.stdout.write(f"Columns found: {', '.join(df.columns)}")

            def convert_date(excel_date):
                """Convert various date formats to Django DateField compatible format"""
                if pd.isna(excel_date) or str(excel_date).strip().upper() in ['', 'NONE', 'NIL',
                                                                              'NOTIONAL EFFECTIVE DATE']:
                    return None

                excel_date = str(excel_date).strip()

                # Try multiple date formats
                date_formats = [
                    '%d-%b-%y', '%d-%b-%Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y',
                    '%Y-%m-%d %H:%M:%S', '%d-%m-%Y', '%m-%d-%Y'
                ]

                for fmt in date_formats:
                    try:
                        return datetime.strptime(excel_date, fmt).date()
                    except ValueError:
                        continue

                # Handle Excel numeric dates
                try:
                    if excel_date.replace('.', '', 1).isdigit():
                        return pd.to_datetime(float(excel_date), unit='D', origin='1899-12-30').date()
                except:
                    return None

            def convert_currency(value):
                """Convert currency values to float"""
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

            def convert_int(value):
                """Convert values to integer with error handling"""
                if pd.isna(value) or str(value).strip().upper() in ['', 'NONE', 'NIL']:
                    return 0
                try:
                    return int(float(str(value).strip()))
                except:
                    return 0

            # Counters
            created_count = 0
            skipped_count = 0
            error_count = 0
            skipped_users = []

            # Process each row
            for index, row in df.iterrows():
                try:
                    staff_id = str(row['STAFF ID']).strip() if pd.notna(row['STAFF ID']) else None

                    # Skip if STAFF ID missing
                    if not staff_id:
                        skipped_count += 1
                        skipped_users.append((index + 1, "No STAFF ID"))
                        continue

                    # Skip if user already exists
                    if User.objects.filter(user_id=staff_id).exists():
                        skipped_count += 1
                        skipped_users.append((index + 1, f"Duplicate STAFF ID: {staff_id}"))
                        continue

                    # Convert required dates
                    date_of_first_appointment = convert_date(row['DATE OF FIRST APPOINTMENT'])
                    if date_of_first_appointment is None:
                        self.stdout.write(
                            self.style.WARNING(f'Row {index + 1}: Missing date_of_first_appointment, using today'))
                        date_of_first_appointment = datetime.now().date()

                    national_effective_date = convert_date(row[' NOTIONAL EFFECTIVE DATE'])
                    if national_effective_date is None:
                        national_effective_date = date_of_first_appointment

                    nhis_number = None
                    if pd.notna(row['NATIONAL HEALTH INSURANCE NO.']) and str(
                            row['NATIONAL HEALTH INSURANCE NO.']).strip() not in ['', 'NONE', 'NIL']:
                        nhis_number = str(row['NATIONAL HEALTH INSURANCE NO.']).strip()

                    # Create user
                    user = User(
                        user_id=staff_id,
                        title=row['TITLE'].strip() if pd.notna(row['TITLE']) else '',
                        first_name=row['FIRST_NAME'].strip() if pd.notna(row['FIRST_NAME']) else '',
                        last_name=row['LAST_NAME'].strip() if pd.notna(row['LAST_NAME']) else '',
                        middle_name=row['MIDDLE_NAME'].strip() if pd.notna(row['MIDDLE_NAME']) else '',
                        role='Staff',
                        maiden_name=row['MAIDEN_NAME'].strip() if pd.notna(row['MAIDEN_NAME']) else '',
                        gender=row['GENDER'].strip() if pd.notna(row['GENDER']) else '',
                        date_of_birth=convert_date(row['DATE OF BIRTH (MM/DD/YYYY)']),
                        age=convert_int(row['AGE']),
                        marital_status=row['MARITAL STATUS'].strip() if pd.notna(row['MARITAL STATUS']) else 'Single',
                        category=row['CLASS'].strip() if pd.notna(row['CLASS']) else '',
                        directorate=row['DIRECTORATE/DEPARTMENT/UNIT'].strip() if pd.notna(
                            row['DIRECTORATE/DEPARTMENT/UNIT']) else '',
                        current_grade=row['CURRENT GRADE'].strip() if pd.notna(row['CURRENT GRADE']) else '',
                        next_grade=row['NEXT GRADE'].strip() if pd.notna(row['NEXT GRADE']) else '',
                        current_salary_level=row['CURRENT SALARY LEVEL'].strip() if pd.notna(
                            row['CURRENT SALARY LEVEL']) else '',
                        current_salary_point=row['CURRENT SALARY POINT'].strip() if pd.notna(
                            row['CURRENT SALARY POINT']) else '',
                        next_salary_level=row['NEXT SALARY LEVEL'].strip() if pd.notna(row['NEXT SALARY LEVEL']) else '',
                        date_of_first_appointment=date_of_first_appointment,
                        date_of_assumption_of_duty=convert_date(row['DATE OF ASSUMPTION OF DUTY']),
                        date_of_last_promotion=convert_date(row['DATE OF LAST PROMOTION']),
                        change_of_grade=row['CHANGE OF GRADE'].strip() if pd.notna(row['CHANGE OF GRADE']) else 'None',
                        substantive_date=convert_date(row['SUBSTANTIVE DATE']),
                        national_effective_date=national_effective_date,
                        years_on_current_grade=convert_int(row['YEARS ON CURRENT GRADE']),
                        number_of_years_in_service=convert_int(row['NUMBER OF YEARS IN THE SERVICE']),
                        fulltime_contract_staff=row['FULLTIME/CONTRACT STAFF'].strip() if pd.notna(
                            row['FULLTIME/CONTRACT STAFF']) else 'FULLTIME',
                        academic_qualification=row['ACADEMIC QUALIFICATION'].strip() if pd.notna(
                            row['ACADEMIC QUALIFICATION']) else '',
                        professional_qualification=row['PROFESSIONAL QUALIFICATION'].strip() if pd.notna(
                            row['PROFESSIONAL QUALIFICATION']) else '',
                        staff_category=row['STAFF CATEGORY'].strip() if pd.notna(row['STAFF CATEGORY']) else '',
                        region=row['REGION'].strip() if pd.notna(row['REGION']) else '',
                        district=row['DISTRICT'].strip() if pd.notna(row['DISTRICT']) else '',
                        single_spine_monthly_salary=convert_currency(row['SINGLE SPINE MONTHLY SALARY ']),
                        monthly_gross_pay=convert_currency(row['MONTHLY GROSS PAY']),
                        annual_salary=convert_currency(row['ANNUAL SALARY']),
                        date_of_retirement=convert_date(row['DATE OF RETIREMENT']) or None,
                        number_of_focus_areas=convert_int(row['NUMBER OF FOCUS AREAS']),
                        number_of_targets=convert_int(row['NUMBER OF TARGETS']),
                        number_of_targets_met=convert_int(row['NUMBER OF TARGETS MET']),
                        number_of_targets_not_met=convert_int(row['NUMBER OF TARGETS NOT MET']),
                        overall_assessment_score=convert_currency(row['OVERALL ASSESSMENT SCORE FOR THE YEAR']),
                        self_assessment_description=row['SELF-ASSESSMENT DESCRIPTION OF RATING'].strip() if pd.notna(
                            row['SELF-ASSESSMENT DESCRIPTION OF RATING']) else '',
                        phone_number=str(row['PHONE NO.']).strip() if pd.notna(row['PHONE NO.']) else '',
                        ghana_card_number=row['GHANA CARD NUMBER'].strip() if pd.notna(row['GHANA CARD NUMBER']) else '',
                        social_security_number=row['SOCIAL SECURITY NO.'].strip() if pd.notna(
                            row['SOCIAL SECURITY NO.']) else '',
                        national_health_insurance_number=nhis_number,
                        bank_name=row['BANK NAME'].strip() if pd.notna(row['BANK NAME']) else '',
                        bank_account_number=str(row['BANK ACCOUNT NO.']).strip() if pd.notna(
                            row['BANK ACCOUNT NO.']) else '',
                        bank_account_branch=row['BANK ACCOUNT BRANCH'].strip() if pd.notna(row['BANK ACCOUNT BRANCH']) else '',
                        management_unit_cost_centre=row['MANAGEMENT UNIT/COST CENTRE'].strip() if pd.notna(
                            row['MANAGEMENT UNIT/COST CENTRE']) else '',
                        payroll_status=row['PAYROLL STATUS'].strip() if pd.notna(row['PAYROLL STATUS']) else 'Active',
                        at_post_on_leave=row['AT POST / ON LEAVE'].strip() if pd.notna(row['AT POST / ON LEAVE']) else 'At Post',
                        on_leave_type=row['ON LEAVE TYPE'].strip() if pd.notna(row['ON LEAVE TYPE']) else None,
                        accommodation_status=row['ACCOMODATION STATUS'].strip() if pd.notna(row['ACCOMODATION STATUS']) else '',
                        supervisor_name=row["SUPERVISOR'S NAME"].strip() if pd.notna(row["SUPERVISOR'S NAME"]) else '',
                        is_active=True,
                    )

                    user.set_password('Securepassword123!')
                    user.save()
                    created_count += 1

                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'Error importing row {index + 1}: {str(e)}'))
                    continue

            # Print results
            self.stdout.write(self.style.SUCCESS(
                f'\nImport completed: {created_count} created, {skipped_count} skipped, {error_count} errors'
            ))

            if skipped_users:
                self.stdout.write(self.style.WARNING("\nSkipped Records Details:"))
                for row_num, reason in skipped_users:
                    self.stdout.write(f" - Row {row_num}: {reason}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading Excel file: {str(e)}'))
