from django.core.exceptions import ValidationError
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    MAX_LEVEL = 5

    name = models.CharField(
        max_length=255,
        verbose_name='Название подразделения'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительское подразделение'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def clean(self):
        super().clean()

        if self.parent:
            parent_level = self.parent.get_level()
            # уровень текущего узла = уровень родителя + 1
            if parent_level + 1 >= self.MAX_LEVEL:
                raise ValidationError({
                    'parent': f'Максимальная глубина вложенности — {self.MAX_LEVEL} уровней.'
                })

    def save(self, *args, **kwargs):
        self.full_clean()  # гарантируем вызов clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class Employee(models.Model):
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО'
    )
    position = models.CharField(
        max_length=255,
        verbose_name='Должность'
    )
    hire_date = models.DateField(
        verbose_name='Дата приема на работу'
    )
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Заработная плата'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name='Подразделение'
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        indexes = [
            models.Index(fields=['department']),
        ]

    def __str__(self):
        return f'{self.full_name} ({self.position})'