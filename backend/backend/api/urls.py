from rest_framework.routers import SimpleRouter

from backend.api.views import PresentationAPIList, PresentationAPIDetail

router = SimpleRouter()
router.register("presentations", PresentationAPIList.as_view())
router.register("presentations/<int:pk>", PresentationAPIDetail.as_view())
