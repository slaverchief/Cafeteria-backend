from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Модель блюда
class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True) # название блюда
    price = models.PositiveIntegerField() # цена блюда

    def __str__(self):
        return f"{self.name} - {self.price}₽"

    class Meta:
        verbose_name_plural = "Dishes"

STATUS_CHOICES =(
    (1, "Оплачено"),
    (2, "Готово"),
    (3, "В ожидании"),
)

# Модель заказа
class Order(models.Model):
    table_number = models.IntegerField() # номер стола
    items = models.ManyToManyField(Dish, related_name='orders') # список блюд
    status = models.IntegerField(choices=STATUS_CHOICES, blank=False, default=3) # статус заказа
    paid_date = models.DateField(null=True, blank=True) # дата оплаты заказа

    def validate_constraints(self, exclude=None):
        res = super().validate_constraints(exclude)
        print(res)
        return res

    def get_paid_date(self):
        return self.paid_date.strftime("%d.%m.%Y")

    # метод возвращает строковое представление статуса через его численный идентификатор в списке STATUS_CHOICES
    def get_status(self):
        return STATUS_CHOICES[self.status-1][1]

    # метод возвращает общую сумму заказа, подсчитывая стоимость всех блюд в заказе
    def total_price(self, as_int=False):
        s = sum([item.price for item in self.items.all()])
        if as_int:
            return s
        return str(s)+'₽'

    # метод генерирует список блюд с их ценами в виде списка строк для представления в шаблоне
    def get_items_list(self):
        string = ""
        items_list = self.items.all()
        for i, item in enumerate(items_list):
            string += f"{item.name}({item.price}₽)"
            if i != len(items_list) - 1:
                string += ', '
        return string

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    status__gte=1, status__lte=3
                ),
                name="Allowable status values",
                violation_error_message="Кодовый номер статуса не может быть меньше 1 или больше 3",
            ),

            models.UniqueConstraint(fields=['table_number'], name='unique_table_number',
                                    violation_error_message="Номер стола уже занят"),

        ]