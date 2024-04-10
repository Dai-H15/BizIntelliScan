from django.shortcuts import render
from main.views import collect_regnum
import calendar
from django.utils import timezone

from main.models import Interview, RegistSets
# Create your views here.


def get_listInterview(request, year, month):

    return [{"Interview": i, "date": timezone.make_naive(i.date).day} for i in Interview.objects.filter(by_U_ID=request.user.U_ID).filter(date__year=year).filter(date__month=month)]


def calendar_main(request):
    contexts = collect_regnum(request)
    year = timezone.make_naive(timezone.now()).year
    month = timezone.make_naive(timezone.now()).month
    today = timezone.make_naive(timezone.now()).day
    contexts["def_year"] = year
    contexts["def_month"] = month
    contexts["today"] = today
    return render(request, "task_calendar/main.html", contexts)


def get_calendar(request, year, month):
    contexts = {}
    calendar.setfirstweekday(calendar.SUNDAY)
    list_calendar = calendar.monthcalendar(int(year), int(month))
    contexts["list_calendar"] = list_calendar
    contexts["list_interview"] = get_listInterview(request, year, month)
    if year == str(timezone.make_naive(timezone.now()).year) and month == str(timezone.make_naive(timezone.now()).month):
        contexts["today"] = timezone.make_naive(timezone.now()).day
    return render(request, "task_calendar/calendar_base.html", contexts)

