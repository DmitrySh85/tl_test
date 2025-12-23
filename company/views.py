from django.views.generic import TemplateView
from .models import Department
from .utils import get_departments_with_children


class DepartmentTreeView(TemplateView):
    template_name = "company/department_tree.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем все корневые подразделения
        root_departments = get_departments_with_children()

        context["departments"] = root_departments
        return context
