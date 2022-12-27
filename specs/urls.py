from django.urls import path
from specs.views import (
    BaseSpecView,
    CreateNewFeature,
    CreateNewCategory,
    CreateFeatureView,
    CreateNewFeatureValidator,
    FeatureChoiceView,
    CreateNewProductFeatureAjaxView,
    NewProductFeatureView,
    SearchProductAjaxView,
    AttachNewFeatureProduct,
    ProductFeatureChoicesAjaxView,
    UpdateProductFeatureView

)

urlpatterns = [
    path('', BaseSpecView.as_view(), name='product-list-for-features'),
    path('new-feature/', CreateNewFeature.as_view(), name='new-feature'),
    path('new-category/', CreateNewCategory.as_view(), name='new-category'),
    path('new-validator/', CreateNewFeatureValidator.as_view(), name='new-validator'),
    path('feature-choice/', FeatureChoiceView.as_view(), name='feature-choice-validator'),
    path('new-product-feature/', NewProductFeatureView.as_view(), name='new-product-feature'),
    path('feature-create/', CreateFeatureView.as_view(), name='create-feature'),
    path('search-product/', SearchProductAjaxView.as_view(), name='search-product'),
    path('attach-feature/', AttachNewFeatureProduct.as_view(), name='attach-feature'),
    path('product-feature/', ProductFeatureChoicesAjaxView.as_view(), name='product-feature'),
    path('attach-new-product-feature/', CreateNewProductFeatureAjaxView.as_view(), name='attach-new-product-feature'),
    path('update-product-features/', UpdateProductFeatureView.as_view(), name='update-product-features'),
]