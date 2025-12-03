from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router=SimpleRouter()
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)
urlpatterns=router.urls







''''
we are using router so we dont need this urls.
urlpatterns=[
    path('products/',views.ProductList.as_view()), #as_view method converts class to function based view
    path('products/<int:pk>/',views.ProductDetail.as_view()),
    path('collections/',views.CollectionList.as_view()),
    path('collections/<int:pk>/',views.CollectionDetail.as_view(),name='collection-detail')
]
'''