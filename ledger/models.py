from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('income', '収入'),
        ('expense', '支出'),
    ]

    CATEGORY_CHOICES = [
        ('食費', '食費'),
        ('交通費', '交通費'),
        ('光熱費', '光熱費'),
        ('趣味', '趣味'),
        ('医療', '医療'),
        ('交際費', '交際費'),
        ('その他', 'その他'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅ 修正
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    amount = models.IntegerField()
    frequency = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時
    note = models.CharField(max_length=100, blank=True, verbose_name="名目")
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True,
        verbose_name="カテゴリ"
    )

    def __str__(self):
        return f"{self.get_entry_type_display()}: {self.amount}円 / {self.frequency}日"

class Goal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
