from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import EntryForm, GoalForm
from .models import Entry, Goal
from collections import defaultdict
from datetime import datetime
import csv
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
import uuid

FREQUENCY_LABELS = {
    1: '毎日',
    7: '毎週',
    30.4: '毎月',
    365: '毎年',
    9999: '一回きり',
}

def get_frequency_label(value):
    try:
        return FREQUENCY_LABELS[float(value)]
    except KeyError:
        return f"{value}日ごと"

@login_required
def home(request):
    if not Entry.objects.filter(user=request.user).exists():
        Entry.objects.create(
            user=request.user,
            entry_type='expense',
            amount=10000,
            frequency=30.4,
            note='サンプル支出',
            category='食費'
        )

    entry_form = EntryForm()
    goal_obj, _ = Goal.objects.get_or_create(user=request.user)
    goal_form = GoalForm(request.POST or None, initial={'goal': goal_obj.amount})

    sort = request.GET.get("sort")
    entries = Entry.objects.filter(user=request.user)
    if sort == "oldest":
        entries = entries.order_by("created_at")
    elif sort == "amount_desc":
        entries = entries.order_by("-amount")
    elif sort == "amount_asc":
        entries = entries.order_by("amount")
    else:
        entries = entries.order_by("-created_at")

    if request.method == 'POST' and 'entry_type' in request.POST:
        entry_form = EntryForm(request.POST)
        if entry_form.is_valid():
            Entry.objects.create(
                user=request.user,
                entry_type=entry_form.cleaned_data['entry_type'],
                amount=entry_form.cleaned_data['amount'],
                frequency=float(entry_form.cleaned_data['frequency']),
                note=entry_form.cleaned_data.get('note'),
                category=entry_form.cleaned_data.get('category')
            )
            return redirect('home')

    income_entries, expense_entries = [], []
    daily_net, sum_income_daily, sum_expense_daily = 0, 0, 0
    expense_by_note = defaultdict(float)

    for e in entries:
        daily = e.amount / e.frequency
        freq_label = get_frequency_label(e.frequency)

        data = {
            'id': e.id,
            'date': e.created_at,
            'type': e.get_entry_type_display(),
            'amount': e.amount,
            'frequency': freq_label,
            'daily': abs(daily),
            'note': e.note,
            'category': e.category,
        }

        if e.entry_type == 'expense':
            daily *= -1
            sum_expense_daily += abs(daily)
            expense_by_note[e.note] += e.amount
            expense_entries.append(data)
        else:
            sum_income_daily += daily
            income_entries.append(data)
        daily_net += daily

    # 支出リストを daily の高い順にソート
    expense_entries.sort(key=lambda x: x['daily'], reverse=True)

    daily_str = f"{daily_net:+.0f}円/日"
    chart_labels = list(expense_by_note.keys())
    chart_values = list(expense_by_note.values())

    if goal_form.is_valid():
        goal = goal_form.cleaned_data.get('goal')
        goal_obj.amount = goal
        goal_obj.save()

    goal = goal_obj.amount
    allowance_str = None
    if goal:
        goal_per_day = goal / 365
        usable_per_day = daily_net - goal_per_day
        allowance_str = f"目標を達成するには、1日 {usable_per_day:.0f}円 まで使えます"

    return render(request, 'ledger/home.html', {
        'entry_form': entry_form,
        'goal_form': goal_form,
        'daily_str': daily_str,
        'income_entries': income_entries,
        'expense_entries': expense_entries,
        'sum_income': sum_income_daily,
        'sum_expense': sum_expense_daily,
        'allowance_str': allowance_str,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    })

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    entry.delete()
    return redirect('home')

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry.entry_type = form.cleaned_data['entry_type']
            entry.amount = form.cleaned_data['amount']
            entry.frequency = float(form.cleaned_data['frequency'])
            entry.note = form.cleaned_data.get('note')
            entry.category = form.cleaned_data.get('category')
            entry.save()
            return redirect('home')
    else:
        form = EntryForm(initial={
            'entry_type': entry.entry_type,
            'amount': entry.amount,
            'frequency': entry.frequency,
            'note': entry.note,
            'category': entry.category,
        })

    return render(request, 'ledger/edit.html', {
        'form': form,
        'entry': entry
    })

@login_required
def export_csv(request):
    entries = Entry.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entries.csv"'

    writer = csv.writer(response)
    writer.writerow(['日付', '金額', '頻度', '日額', '名目', 'カテゴリ', 'タイプ'])

    for e in entries:
        daily = e.amount / e.frequency
        writer.writerow([
            e.created_at.strftime('%Y-%m-%d'),
            e.amount,
            e.frequency,
            round(daily),
            e.note,
            e.category,
            e.entry_type
        ])

    return response

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def guest_login(request):
    username = f"guest_{uuid.uuid4().hex[:8]}"
    user = User.objects.create_user(username=username)
    user.set_unusable_password()
    user.save()
    login(request, user)
    return redirect('home')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def about(request):
    return render(request, 'ledger/lp.html')
