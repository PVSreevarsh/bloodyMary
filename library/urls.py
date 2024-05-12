from django.urls import path

from .views import SectorListView,InvestmentCreateView,RegisterMSME,SMEListView,DisplaySpecificMSME,showMSMEDetails,BankInvestmentView

urlpatterns = [
    path("bankLanding/", SectorListView.as_view(), name="view-sector-details"),
    path("createInvestment/", InvestmentCreateView.as_view(), name="create-investment"),
     path("registerMSME/", RegisterMSME.as_view(), name="register-msme"),
     path("MSMELanding/", SMEListView.as_view(), name="view-msme-details"),
     path("displayname/<int:id>", DisplaySpecificMSME.as_view(), name="view-msme-details1"),
     path("showMSME/", showMSMEDetails.as_view(), name="view-msme-specific"),
    path("Bankdetails/", BankInvestmentView.as_view(), name="bank-dashboard"),
]

