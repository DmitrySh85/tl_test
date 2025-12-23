from .models import Department


def get_departments_with_children():
    return Department.objects.filter(
        parent=None
    ).prefetch_related(
            "employees",  # все сотрудники подразделения
            "children__employees",  # сотрудники детей первого уровня
            "children__children__employees",  # второго уровня
            "children__children__children__employees",  # третьего уровня
            "children__children__children__children__employees",  # четвертого уровня
            )