from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db.utils import OperationalError
from ecwsp.sis.sample_data import *
from ecwsp.sis.sample_gui_data import *
from ecwsp.sis.models import Student
from ecwsp.sis.management.commands.populate_sample_application import ApplicationTemplateGenerator
from optparse import make_option

class Command(BaseCommand):
    help = 'Populate blank database'
    gui = False

    option_list = BaseCommand.option_list + (
        make_option('--gui',
            action='store_true',
            dest='gui',
            default=False,
            help='Populate sample data for people to use while demoing or working on front end'),
    )

    def handle(self, *args, **options):
        try:
            if Student.objects.first():
                raise CommandError('You cannot run this on a already populated database')
        except OperationalError: # New database
            import django
            if django.get_version()[:3] != '1.7':
                call_command('syncdb', all=True, interactive=False)
            else:
                call_command('migrate', interactive=False)

        if options['gui']:
            SisGUIData().create_all()
        else :
            SisData().create_all()
            ApplicationTemplateGenerator().create_default_admission_application()
        
        self.stdout.write('Success. Good Job!')