from django.urls import path

# ===============================
# AUTH
# ===============================
from core.views.auth import (
    login_view,
    logout_view,
    me,
    signup_view,
)

# ===============================
# EMPLOYEE PROFILE
# ===============================
from core.views.profile import (
    get_employee_profile,
    update_employee_profile,
    delete_employee_profile,
    update_employee_skills
)

# ===============================
# EMPLOYEE FEATURES
# ===============================
from core.views.skill_gap import skill_gap_analysis
from core.views.ai import (
    ai_recommendation,
    get_recommendations,
    delete_recommendation,
    edit_recommendation,
)

# ===============================
# EMPLOYER
# ===============================
from core.views.employer import (
    get_employees,
    add_employee,
)

# ===============================
# GLOBAL DATA
# ===============================
from core.views.global_data import (
    get_global_skills,
    get_global_roles,
    get_skill_role_map,
)


urlpatterns = [

    # ===============================
    # AUTHENTICATION
    # ===============================
    path("auth/signup/", signup_view),
    path("auth/login/", login_view),
    path("auth/logout/", logout_view),
    path("auth/me/", me),

    # ===============================
    # EMPLOYEE PROFILE (SELF)
    # ===============================
    path("employee/profile/", get_employee_profile),
    path("employee/profile/update/", update_employee_profile),
    path("employee/profile/delete/", delete_employee_profile),
    path("employee/skills/", update_employee_skills),

    # ===============================
    # App FEATURES
    # ===============================
    path("skills/gap/", skill_gap_analysis),

    # ===============================
    # AI RECOMMENDATIONS
    # ===============================
    path("ai/recommend/", ai_recommendation),
    path("ai/history/", get_recommendations),
    path("ai/history/<int:rec_id>/edit/", edit_recommendation),
    path("ai/history/<int:rec_id>/delete/", delete_recommendation),

    # ===============================
    # EMPLOYER FEATURES
    # ===============================
    path("employees/", get_employees),
    path("employees/add/", add_employee),

    # ===============================
    # GLOBAL REFERENCE DATA (PUBLIC)
    # ===============================
    path("global/skills/", get_global_skills),
    path("global/roles/", get_global_roles),
    path("global/skill-role-map/", get_skill_role_map),
]
