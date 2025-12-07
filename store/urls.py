from django.urls import path
from . import views
from rest_framework_nested import routers
router=routers.DefaultRouter()

router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)

#nested router
products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product_reviews')


urlpatterns=router.urls+products_router.urls


''''
we are using router so we dont need this urls.
urlpatterns=[
    path('products/',views.ProductList.as_view()), #as_view method converts class to function based view
    path('products/<int:pk>/',views.ProductDetail.as_view()),
    path('collections/',views.CollectionList.as_view()),
    path('collections/<int:pk>/',views.CollectionDetail.as_view(),name='collection-detail')
]
'''