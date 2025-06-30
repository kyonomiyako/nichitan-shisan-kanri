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

    entry_type = forms.ChoiceField(
        label='収入 or 支出',
        choices=TYPE_CHOICES,
        initial='expense'
    )
    amount = forms.IntegerField(label='金額')
    frequency = forms.ChoiceField(
        label='頻度',
        choices=FREQUENCY_CHOICES,
        initial=30.4
    )
    note = forms.CharField(
        label='項目',
        required=True,
        error_messages={'required': '項目を入力してください'}
    )

class GoalForm(forms.Form):
    goal = forms.IntegerField(label='目標年間貯金額', required=False)
