from django.urls import path
from .views import rents_list,accounts_detail, accounts_signup,login,upload_property,get_profile,get_property,add_like,add_view,update_profile,get_top_company,get_view_property,you_may_like,get_category,add_rate,update_item,get_cart,add_to_cart,remove_from_cart,cart_recommend,get_cart_len,remove_Item,get_all_items
urlpatterns = [
path("rents/",rents_list.as_view(), name="rents_list"),
path("accounts/<int:pk>/",accounts_detail.as_view(), name="accounts_detail"),
path("signup/",accounts_signup.as_view(), name="accounts_create"),
path("login/", login.as_view(),name="login"),
path("store/upload/",upload_property.as_view(), name="upload_property"),
path("dashboard/profile/<str:username>/",get_profile.as_view(), name="get_profile"),
path("dashboard/myproperty/<str:username>/",get_property.as_view(), name="get_property"),
path("toview/<str:id>/",get_view_property.as_view(), name="get_view_property"),
path("getallitem/",get_all_items.as_view(), name="get_all_item"),
path("addview/<str:id>/",add_view.as_view(), name="addview"),
path("addlike/<str:id>/",add_like.as_view(), name="addlike"),
path("addrate/<str:id>/<str:value>/<str:username>/",add_rate.as_view(), name="addrate"),
path("youmaylike/<str:store>/<str:id>/",you_may_like.as_view(), name="youmaylike"),
path("dashboard/updateprofile/",update_profile.as_view(), name="updateprofile"),
path("dashboard/updateitem/",update_item.as_view(), name="updateitem"),
path("getTopCompany/", get_top_company.as_view(),name="get_top_company"),
path("getcategory/", get_category.as_view(),name="get_category"),
path("getcart/<str:username>/",get_cart.as_view(), name="getcart"),
path("getcartlen/<str:username>/",get_cart_len.as_view(), name="getcartlen"),
path("addtocart/<str:id>/<str:username>/",add_to_cart.as_view(), name="addtocart"),
path("removefromcart/<str:cart_user>/<str:item_id>/",remove_from_cart.as_view(), name="removefromcart"),
path("dashboard/remove-item/<str:item_id>/",remove_Item.as_view(), name="removeItem"),

path("cartrecommend/",cart_recommend.as_view(), name="cartrecommend"),


]

