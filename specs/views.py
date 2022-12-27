from django.shortcuts import render
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse
from specs.models import CategoryFeature, FeatureValidator, ProductFeature
from specs.forms import NewCategoryForm, NewCategoryFeatureKeyForm
from mainapp.models import Category, Product


class BaseSpecView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'product_features.html', {})


class CreateNewFeature(View):
    def get(self, request, *args, **kwargs):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_feature.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        if form.is_valid():
            new_category_feature_key = form.save(commit=False)
            new_category_feature_key.category = form.cleaned_data['category']
            new_category_feature_key.feature_name = form.cleaned_data['feature_name']
            new_category_feature_key.save()
        return HttpResponseRedirect('/product-specs/')


class CreateNewCategory(View):
    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.name = form.cleaned_data['name']
            new_category.save()
        return HttpResponseRedirect('product-specs')


class CreateNewFeatureValidator(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'new_validator.html', context)


class FeatureChoiceView(View):
    def get(self, request, *args, **kwargs):
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
            <select class="form_select" name="feature-validators" id="feature-validators-id" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
        """
        feature_key_qs = CategoryFeature.objects.filter(
            category_id=int(request.GET.get('category_id'))
        )
        res_string = ""
        for item in feature_key_qs:
            res_string += option.format(value=item.feature_name, option_name=item.feature_name)
        html_select = html_select.format(result=res_string)
        return JsonResponse({'result': html_select, 'value': int(request.GET.get('category_id'))})


class CreateFeatureView(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        feature_name = request.GET.get('feature_name')
        value = request.GET.get('feature_value').strip(" ")
        print(value)
        category = Category.objects.get(id=int(category_id))
        feature = CategoryFeature.objects.get(category=category, feature_name='')
        existed_objects, created = FeatureValidator.objects.get_or_create(
            category=category,
            feature_key=feature,
            valid_feature_value=value
        )
        if not created:
            return JsonResponse({
                "error": f"значение '{value}' уже существует"
            })
        messages.add_message(
            request, messages.SUCCES,
            f"значение '{value} для характеристики'"
            f"'{feature.feature_name}'в категории {category.name} успешно создано"
        )
        return JsonResponse({'result': 'ok'})


class NewProductFeatureView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'new_product_feature.html', context)


class SearchProductAjaxView(View):
    def get(self, request, *args, **kwargs):
        query = request.POST.get('query')
        category_id = request.GET.get('category_id')
        category = Category.objects.get(id=int(category_id))
        products = list(Product.objects.filter(
            category=category,
            title__icontains=query
        ).values())
        return JsonResponse({'result': products})


class AttachNewFeatureProduct(View):
    def get(self, request, *args, **kwargs):
        res_string = ''
        product = Product.objects.get(int(request.GET.get('product_id')))
        existing_features = list(set(item.feature.feature_name for item in product.features.all()))
        category_features = CategoryFeature.objects.filter(
            category=product.category
        ).exclude(feature_name__in=existing_features)
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
                    <select class="form_select" name="product-category-features" id="product-category-features-id" aria-label="Default select example">
                        <option selected>---</option>
                        {result}
                    </select>
                """
        for item in category_features:
            res_string += option.format(value=item.category.id, option_name=item.feature_name)
        html_select = html_select.format(result=res_string)
        return JsonResponse({'features': html_select})


class ProductFeatureChoicesAjaxView(View):
    def get(self, request, *args, **kwargs):
        res_string = ""
        category = Category.objects.get(id=int(request.GET.get('category_id')))
        feature_key = CategoryFeature.objects.get(
            category=category,
            feature_name=request.GET.get('product_feature_name')
        )
        validators_qs = FeatureValidator.objects.filter(
            category=category,
            feature_key=feature_key
        )
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
                    <select class="form_select" name="product-category-features-choices" id="product-category-features-choices-id" aria-label="Default select example">
                        <option selected>---</option>
                        {result}
                    </select>
                        """
        for item in validators_qs:
            res_string += option.format(value=item.id, option_name=item.valid_feature_value)
        html_select = html_select.format(result=res_string)
        return JsonResponse({'features': html_select})


class CreateNewProductFeatureAjaxView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(title=request.GET.get('product'))
        category_feature = CategoryFeature.objects.get(
            category=product.category,
            feature_name=request.GET.get('category_feature')
        )
        value = request.GET.get('value')
        feature = ProductFeature.objects.create(
            feature=CategoryFeature,
            product=product,
            value=value
        )
        product.features.add(feature)
        return JsonResponse({"OK": "OK"})


class UpdateProductFeatureView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'update_product_features.html', context)
