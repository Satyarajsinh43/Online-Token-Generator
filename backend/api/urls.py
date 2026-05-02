from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    OfficeViewSet, TokenViewSet, EmployeeViewSet, 
    RegisterView, DistrictViewSet, TalukaViewSet, VillageViewSet,
    MyTokenObtainPairView, ServiceViewSet,
    BookTokenView, TokenReceiptView, VerifyTokenView, verify_token,
    SendOTPView, VerifyOTPView, CreateEmployeeAPIView, clerk_sync_user,
    AvailableSlotsView
)

router = DefaultRouter()
router.register(r'districts', DistrictViewSet)
router.register(r'talukas', TalukaViewSet)
router.register(r'villages', VillageViewSet)
router.register(r'offices', OfficeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'tokens', TokenViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('book-token/', BookTokenView.as_view(), name='book_token'),
    path('token/receipt/<int:pk>/', TokenReceiptView.as_view(), name='token_receipt'),
    path('verify-token/<str:token_hash>/', VerifyTokenView.as_view(), name='verify_token'),
    path('verify-token/', verify_token, name='staff_verify_token'),
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('create-staff/', CreateEmployeeAPIView.as_view(), name='create_staff'),
    path('clerk-sync-user/', clerk_sync_user, name='clerk_sync_user'),
    path('available-slots/', AvailableSlotsView.as_view(), name='available_slots'),
]
