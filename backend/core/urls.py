from django.urls import path
from .views.employees import get_employees, add_employee,  update_skills_by_user, get_employee_by_id
from .views.skills import get_skills
from .views.ai import ai_recommendation,  get_recommendations, delete_recommendation, edit_recommendation

from .views.global_data import get_global_skills, get_global_roles, get_skill_role_map


urlpatterns = [
    path('employees/', get_employees, name='get_employees'),
    path('employees/add/', add_employee, name='add_employee'),
    path("employees/<int:user_id>/", get_employee_by_id, name="get_employee_by_id"),
    path('skills/', get_skills, name='get_skills'),
    path('recommend/', ai_recommendation, name='ai_recommendation'),
    path('recommend/history/<int:user_id>/', get_recommendations, name='get_recommendations'),
    path('recommend/edit/<int:rec_id>/', edit_recommendation, name='edit_recommendation'),
    path('recommend/delete/<int:rec_id>/', delete_recommendation, name='delete_recommendation'),
    path('employees/by-user/<int:user_id>/update-skills/', update_skills_by_user),


    path('global/skills/', get_global_skills),
    path('global/roles/', get_global_roles),
    path('global/skill-role-map/', get_skill_role_map),

]
