from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account", views.account, name="account"),
    path("add", views.add, name="add"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("update/<int:task_id>", views.update, name="update"),
    path("<str:day>tag=<str:tag>", views.view_tasks, name="view_tasks"),
    path("bother_us", views.bother_us, name="bother_us"),
    path("date_picker", views.date_picker, name="date_picker"),
    path("logbook", views.logbook, name="logbook"),
    path("<int:task_id>", views.open_page, name="open_page"),
    path("confirm", views.confirm, name="confirm"),
    path("decline", views.decline, name="decline"),
    path("check_off/<int:id>", views.check_off, name="check_off"),
    path("quick_add", views.quick_add, name="quick_add"),
    path("edit_tag", views.edit_tag, name="edit_tag"),
    path("delete_tag", views.delete_tag, name="delete_tag"),
    path("delete_friend", views.delete_friend, name="delete_friend"),
    path("add_friend", views.add_friend, name="add_friend"),
    path("add_tag", views.add_tag, name="add_tag"),
    path("delete_account", views.delete_account, name="delete_account"),
    path("change_password", views.change_password, name="change_password"),
    path("not_today/<int:task_id>", views.not_today, name="not_today"),
    path("change_theme", views.change_theme, name="change_theme"),
    path("default_theme", views.default_theme, name="default_theme"),
    path("privacy_policy", views.privacy_policy, name="privacy_policy")
]