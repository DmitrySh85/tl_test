import random

from django.core.management.base import BaseCommand
from faker import Faker

from company.models import Department, Employee


class Command(BaseCommand):
    help = 'Генерация тестовых подразделений и сотрудников'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50_000,
            help='Количество сотрудников (по умолчанию 50 000)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=2_000,
            help='Размер batch для bulk_create'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительно генерировать, даже если сотрудники уже существуют'
        )

    def handle(self, *args, **options):
        count = options['count']
        batch_size = options['batch_size']
        force = options['force']

        if Employee.objects.exists() and not force:
            self.stdout.write(
                self.style.WARNING(
                    'Сотрудники уже существуют. '
                    'Используйте --force для повторной генерации.'
                )
            )
            return

        fake = Faker('ru-RU')

        departments = self._get_or_create_departments()

        self.stdout.write(
            f'Генерация {count} сотрудников (batch_size={batch_size})...'
        )

        employees = []

        for i in range(1, count + 1):
            employees.append(
                Employee(
                    full_name=fake.name(),
                    position=fake.job(),
                    hire_date=fake.date_between(
                        start_date='-10y',
                        end_date='today'
                    ),
                    salary=random.randint(50_000, 300_000),
                    department=random.choice(departments),
                )
            )

            if len(employees) >= batch_size:
                Employee.objects.bulk_create(employees)
                employees.clear()

            if i % 10_000 == 0:
                self.stdout.write(f'Создано {i} сотрудников...')

        if employees:
            Employee.objects.bulk_create(employees)

        self.stdout.write(
            self.style.SUCCESS(
                f'Готово! Успешно создано {count} сотрудников.'
            )
        )

    def _get_or_create_departments(self):
        """
        Создает дерево подразделений до 5 уровней,
        если подразделения отсутствуют.
        """
        if Department.objects.exists():
            self.stdout.write('Подразделения уже существуют.')
            return list(Department.objects.all())

        self.stdout.write('Создание подразделений...')

        departments_by_level = {0: []}

        root = Department.objects.create(name='Головная компания')
        departments_by_level[0].append(root)

        for level in range(1, 5):
            departments_by_level[level] = []
            for i in range(5):
                parent = random.choice(departments_by_level[level - 1])
                dept = Department.objects.create(
                    name=f'Подразделение {level}.{i + 1}',
                    parent=parent
                )
                departments_by_level[level].append(dept)

        departments = [
            dept
            for level_depts in departments_by_level.values()
            for dept in level_depts
        ]

        self.stdout.write(
            self.style.SUCCESS(
                f'Создано подразделений: {len(departments)}'
            )
        )

        return departments