from django.urls import path

from .views import (
    HomePageView,
    PrivacyPolicyView,
    TermsOfUseView,
    FAQView,
    ProfileView,
)


urlpatterns = (
    path('', HomePageView.as_view(), name='homepage'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-of-use/', TermsOfUseView.as_view(), name='terms-of-use'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('profile/', ProfileView.as_view(), name='profile'),
)
