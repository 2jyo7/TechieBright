from django.db import models
# from django.utils import timezone
from django.contrib.auth.models import User






# =========================
# EMPLOYEE DATA MODEL
# =========================


class EmployeeData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    country = models.CharField(max_length=50)
    job_title = models.CharField(max_length=100)
    age = models.IntegerField()
    race = models.CharField(max_length=50)
    experience_years = models.FloatField()
    salary = models.FloatField()
    industry = models.CharField(max_length=100)

    WORK_TYPE_CHOICES = [
        ("remote", "Remote"),
        ("onsite", "Onsite"),
        ("hybrid", "Hybrid")
    ]
    work_type = models.CharField(max_length=20, choices=WORK_TYPE_CHOICES)

    skills = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Unassigned'} - {self.job_title}"

# =========================
# SKILL MODEL
# =========================
class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # e.g., programming, soft-skill, cloud

    def __str__(self):
        return self.name


# =========================================
# JOB → SKILL MAPPING (Requirement System)
# =========================================
class JobSkillRequirement(models.Model):
    job_title = models.CharField(max_length=100)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    importance_level = models.IntegerField(default=1)  # 1–5 scale

    def __str__(self):
        return f"{self.job_title} requires {self.skill.name}"


# =========================
# AI RECOMMENDATION MODEL
# =========================
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_query = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # perfect as is

    def __str__(self):
        return f"Recommendation for {self.user.username} on {self.created_at.date()}"


# =========================
# Profile MODEL
# =========================

class Profile(models.Model):
    ROLE_CHOICES = (
        ("employee", "Employee"),
        ("employer", "Employer"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
