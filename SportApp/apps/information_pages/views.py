from django.shortcuts import render
from django.views import View
from django.http import (
    HttpRequest,
    HttpResponse,
)


class HomePageView(View):
    """
    Base page with information about site.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='homepage.html')


class SiteMapView(View):
    """
    Base page with information about all routes.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='sitemap.html')


class PrivacyPolicyView(View):
    """
    Base page with information about privacy policy.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='privacy-policy.html')


class TermsOfUseView(View):
    """
    Base page with information about terms of use.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='terms-of-use.html')


class FAQView(View):
    """
    Base page with answers to the most frequently asked questions.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='faq.html')
