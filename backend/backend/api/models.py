from django.db import models


class Presentation(models.Model):
    creator = models.ForeignKey("authentication.User", verbose_name="Пользователь", on_delete=models.CASCADE)
    description = models.TextField("Описание")
    generate_logo = models.BooleanField("Сгенерировать логотип", default=False)
    generate_name = models.BooleanField("Сгенерировать название", default=False)
    checko_url = models.URLField("Ссылка на Checko", default=None, null=True)

    class Meta:
        verbose_name = "Презентация"
        verbose_name_plural = "Презентации"


class Result(models.Model):
    presentation = models.OneToOneField("Presentation", verbose_name="Презентация", on_delete=models.CASCADE)
    logo = models.ImageField("Логотип", upload_to="logos", default=None, null=True)
    name = models.CharField("Название", max_length=100, default=None, null=True)
    pptx_data = models.JSONField("JSON", default=None, null=True)
    pptx = models.FileField("PPTX", default=None, null=True)
    name_status = models.CharField("Статус названия", max_length=100)
    logo_status = models.CharField("Статус логотипа", max_length=100)
    pptx_status = models.CharField("Статус PPTX", max_length=100)
