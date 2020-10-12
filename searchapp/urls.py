from django.urls import path
from .views import main_search,add_review,search_data,tag,acquisition,condition,store,duration,delivery,location,configprice,price,popular_shop,get_reviews
# ,get_suggestion


urlpatterns = [
# path("rents/",rents_list.as_view(), name="rents_list"),
path("mainsearch/", main_search.as_view(),name="main_search"),
# path("filtersearch/", filter_search.as_view(),name="filter_search"),
path("search_data/", search_data.as_view(),name="search_data"),
path("tag/", tag.as_view(),name="tag_data"),
path("acquisition/", acquisition.as_view(),name="acquisition_data"),
path("condition/", condition.as_view(),name="condition_data"),
path("store/", store.as_view(),name="store_data"),
path("delivery/", delivery.as_view(),name="delivery_data"),
path("duration/", duration.as_view(),name="duration_data"),
path("location/", location.as_view(),name="location_data"),
path("configprice/", configprice.as_view(),name="configprice_data"),
path("price/", price.as_view(),name="price_data"),
path("popular-shop/", popular_shop.as_view(),name="price_data"),
# path("getsuggestion/", get_suggestion.as_view(),name="get_suggestion"),
path("addreview/<str:id>/<str:username>/",add_review.as_view(), name="addreview"),
path("get_reviews/<str:id>/",get_reviews.as_view(), name="getreview"),


]
