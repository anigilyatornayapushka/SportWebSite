from django.shortcuts import render
from django import views
from django.http import (
    HttpRequest,
    HttpResponse,
)


class HomePageView(views.View):
    """
    Base page with information about site.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='informations/homepage.html')


class PrivacyPolicyView(views.View):
    """
    Base page with information about privacy policy.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='informations/privacy-policy.html')


class TermsOfUseView(views.View):
    """
    Base page with information about terms of use.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='informations/terms-of-use.html')


class FAQView(views.View):
    """
    Base page with answers to the most frequently asked questions.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='informations/faq.html')
