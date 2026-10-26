from django.db import models


class SiteSettings(models.Model):
    """Контакты и тексты главной. Запись одна, её правит владелец в админке."""

    company_name = models.CharField("Название компании", max_length=100, default="Чисто")
    hero_title = models.CharField("Заголовок на главной", max_length=200)
    hero_subtitle = models.TextField("Подзаголовок на главной")
    phone = models.CharField("Телефон", max_length=30)
    email = models.EmailField("Email", blank=True)
    address = models.CharField("Адрес", max_length=200, blank=True)
    work_hours = models.CharField("Часы работы", max_length=100, blank=True)
    telegram = models.URLField("Ссылка на Telegram", blank=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def save(self, *args, **kwargs):
        # Всегда одна запись с id=1, вторую создать нельзя
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        return cls.objects.filter(pk=1).first()


class Service(models.Model):
    ICONS = [
        ("home", "Дом"),
        ("sparkles", "Блеск"),
        ("window", "Окно"),
        ("sofa", "Диван"),
        ("building", "Офис"),
        ("hammer", "Ремонт"),
    ]

    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    price_from = models.PositiveIntegerField("Цена от, ₽")
    unit = models.CharField("За что цена", max_length=30, blank=True, help_text="Например: за м², за окно")
    icon = models.CharField("Иконка", max_length=20, choices=ICONS, default="sparkles")
    order = models.PositiveIntegerField("Порядок", default=0, db_index=True)
    is_active = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.CharField("Имя", max_length=60)
    text = models.TextField("Текст отзыва")
    rating = models.PositiveSmallIntegerField("Оценка", choices=[(i, str(i)) for i in range(1, 6)], default=5)
    is_published = models.BooleanField("Опубликован", default=True)
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author}: {self.text[:40]}"


class Faq(models.Model):
    question = models.CharField("Вопрос", max_length=200)
    answer = models.TextField("Ответ")
    order = models.PositiveIntegerField("Порядок", default=0, db_index=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Частые вопросы"
        ordering = ["order", "id"]

    def __str__(self):
        return self.question


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_WORK = "in_work", "В работе"
        DONE = "done", "Выполнена"
        REJECTED = "rejected", "Отказ"

    name = models.CharField("Имя", max_length=60)
    phone = models.CharField("Телефон", max_length=30)
    service = models.ForeignKey(
        Service, verbose_name="Услуга", on_delete=models.SET_NULL, null=True, blank=True, related_name="leads"
    )
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.NEW, db_index=True)
    manager_note = models.TextField("Заметка менеджера", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}, {self.phone}"
