from django.shortcuts import render, HttpResponse
from main.views import collect_regnum
from main.models import RegistSets, Interview
from authUser.models import CustomUser
# Create your views here.


def management(request):
    contexts = collect_regnum(request)
    return render(request, "index.html", contexts)


def all_sheets(request):
    if request.user.is_staff:
        contexts = collect_regnum(request)
        count = RegistSets.objects.all().count()
        contexts["count"] = count
    else:
        return HttpResponse("error: 権限がありません")

    return render(request, "all_sheets.html", contexts)


def management_sheets(request):
    contexts = collect_regnum(request)
    return render(request, "management_sheets.html", contexts)


def all_interviewer(request):
    contexts = collect_regnum(request)
    return render(request, "all_interviewer.html", contexts)


def admin_all_sheet(request, sheet_from, where):
    contexts = collect_regnum(request)
    if request.user.is_staff:
        res = RegistSets.objects.all().order_by("-isActive")
        contexts["posts"] = res
        if sheet_from == "企業名":
            res = res.filter(company__name__contains=where)
        if sheet_from == "所属業界名":
            res = res.filter(company__industry__contains=where)
        if sheet_from == "所在地":
            res = res.filter(d_company__location__contains=where)
        if sheet_from == "担当者名":
            res = res.filter(company__contact__contains=where)
        if sheet_from == "ユーザー名":
            res = res.filter(by_U_ID=CustomUser.objects.get(username=where).U_ID)
        contexts["posts"] = res
        post_interviews = {}
        for post in res:
            i = Interview.objects.filter(RegistID=post).order_by("-date").first()
            post_interviews[post.RegistID] = i.InterviewID if i is not None else None
        contexts["post_interviews"] = post_interviews
    else:
        return HttpResponse("error: 権限がありません。")
    return render(request, "admin_sheetview.html", contexts)