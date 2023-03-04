from django.db import models


class CommonFieldsModel(models.Model):
    """Абстрактная модель для повторяющихся полей."""
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date', )
        abstract = True

    def __str__(self):
        return self.text
