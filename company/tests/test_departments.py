from django.test import TestCase
from ..models import Department, Employee
from datetime import date
from ..utils import get_departments_with_children


class DepartmentEmployeesTestCase(TestCase):
    def setUp(self):
        # Создаем корневое подразделение
        root = Department.objects.create(name="Root")
        # Создаем дочернее
        child = Department.objects.create(name="Child", parent=root)
        # Сотрудников
        Employee.objects.create(full_name="Иванов Иван", position="Dev", hire_date=date.today(), salary=1000, department=root)
        Employee.objects.create(full_name="Петров Петр", position="QA", hire_date=date.today(), salary=1200, department=child)

    def test_get_with_employees(self):
        qs = get_departments_with_children()
        self.assertEqual(qs.count(), 1)  # только корневое
        root = qs.first()
        self.assertEqual(root.employees.count(), 1)
        child = root.children.first()
        self.assertEqual(child.employees.count(), 1)
