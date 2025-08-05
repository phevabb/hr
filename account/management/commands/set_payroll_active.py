from django.core.management.base import BaseCommand
from account.models import User

class Command(BaseCommand):
    help = "Set all users' PAYROLL STATUS field to 'ACTIVE (PAID)'"

    def handle(self, *args, **options):
        try:
            updated_count = User.objects.update(payroll_status="ACTIVE (PAID)")
            self.stdout.write(self.style.SUCCESS(f"✅ Successfully updated {updated_count} users' payroll status to 'ACTIVE (PAID)'"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error updating payroll status: {str(e)}"))
