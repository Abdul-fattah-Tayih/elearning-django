from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Permission, Group

class Command(BaseCommand):
    help = 'Seeds the user groups and their associated permissions'

    def handle(self, *args: Any, **options: Any) -> str | None:        
        teacher, teacher_created = Group.objects.get_or_create(name='teacher')
        student, student_created = Group.objects.get_or_create(name='student')

        if not teacher_created or not student_created:
            raise CommandError('Error creating groups')

        teacher_permissions = Permission.objects.filter(codename__in=[
            'add_course',
            'change_course',
            'delete_course',
            'view_course',
            'add_lesson',
            'change_lesson',
            'delete_lesson',
            'view_lesson'
        ]).all()

        teacher.permissions.add(*teacher_permissions)

        student_permissions = Permission.objects.filter(codename__in=[
            'view_course',
            'view_lesson'
        ]).all()

        student.permissions.add(*student_permissions)

        self.stdout.write('Seeded successfully!')