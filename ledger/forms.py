
from django import forms

class EntryForm(forms.Form):
    TYPE_CHOICES = [
        ('income', '収入'),
        ('expense', '支出'),
    ]
    FREQUENCY_CHOICES = [
        (1, '毎日'),
        (7, '毎週'),
        (30.4, '毎月'),
        (365, '毎年'),
        (9999, '一回きり'),
    ]
    CATEGORY_CHOICES = [
        ('給与', '給与'),
        ('食費', '食費'),
        ('交通費', '交通費'),
        ('光熱費', '光熱費'),
        ('趣味', '趣味'),
        ('医療', '医療'),
        ('交際費', '交際費'),
        ('その他', 'その他'),
    ]

    entry_type = forms.ChoiceField(
        label='収入 or 支出',
        choices=TYPE_CHOICES,
        initial='expense'
    )
    amount = forms.IntegerField(
        label='金額',
        widget=forms.NumberInput(attrs={
            'placeholder': '例: 10000 円',
            'inputmode': 'numeric'
        })
    )
    frequency = forms.ChoiceField(
        label='頻度',
        choices=FREQUENCY_CHOICES,
        initial=30.4
    )
    category = forms.ChoiceField(
        label='カテゴリ',
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.RadioSelect
    )
    note = forms.CharField(
        label='メモ',
        required=False
    )

class GoalForm(forms.Form):
    goal = forms.IntegerField(
        label='目標年間貯金額（円）',
        required=False
    )
