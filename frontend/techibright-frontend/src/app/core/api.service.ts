import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Employee } from '../models/employee.model';
import { AIRecommendation } from '../models/ai.model';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://localhost:8000/api/';

  constructor(private http: HttpClient) {}

  // ===============================
  // EMPLOYER (AUTH REQUIRED)
  // ===============================

  getEmployees(): Observable<Employee[]> {
    return this.http.get<Employee[]>(
      `${this.baseUrl}employees/`,
      { withCredentials: true }
    );
  }

  addEmployee(data: Employee): Observable<any> {
    return this.http.post(
      `${this.baseUrl}employees/add/`,
      data,
      { withCredentials: true }
    );
  }

  // ===============================
  // EMPLOYEE PROFILE (SELF)
  // ===============================

  /** Get logged-in employee profile */
  getMyProfile(): Observable<Employee> {
    return this.http.get<Employee>(
      `${this.baseUrl}employee/profile/`,
      { withCredentials: true }
    );
  }

  /** Update logged-in employee profile */
  updateMyProfile(data: {
    job_title: string;
    industry: string;
    experience_years: number;
    work_type: string;
    country: string;
    age: number;
    race: string;
    salary: number;

  }): Observable<any> {
    return this.http.put(
      `${this.baseUrl}employee/profile/update/`,
      data,
      { withCredentials: true }
    );
  }

  /** Delete own profile */
  deleteMyProfile(): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}employee/profile/delete/`,
      { withCredentials: true }
    );
  }

  /** Update logged-in employee skills */
  updateMySkills(skills: string[]): Observable<any> {
    return this.http.put(
      `${this.baseUrl}employee/skills/`,
      { skills },
      { withCredentials: true }
    );
  }

  // ===============================
  // SKILL GAP ANALYSIS
  // ===============================

  analyzeSkillGap(role: string): Observable<any> {
    return this.http.post(
      `${this.baseUrl}skills/gap/`,
      { role },
      { withCredentials: true }
    );
  }

  // ===============================
  // AI RECOMMENDATIONS
  // ===============================

  aiRecommend(query: string): Observable<{ recommendation: AIRecommendation }> {
    return this.http.post<{ recommendation: AIRecommendation }>(
      `${this.baseUrl}ai/recommend/`,
      { query },
      { withCredentials: true }
    );
  }

  getRecommendationHistory(): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.baseUrl}ai/history/`,
      { withCredentials: true }
    );
  }

  deleteRecommendation(id: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}ai/history/${id}/delete/`,
      { withCredentials: true }
    );
  }

  editRecommendation(id: number, query: string): Observable<any> {
    return this.http.put(
      `${this.baseUrl}ai/history/${id}/edit/`,
      { query },
      { withCredentials: true }
    );
  }

  // ===============================
  // GLOBAL DATA (PUBLIC)
  // ===============================

  getGlobalSkills(): Observable<string[]> {
    return this.http.get<string[]>(
      `${this.baseUrl}global/skills/`
    );
  }

  getGlobalRoles(): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.baseUrl}global/roles/`
    );
  }

  getSkillRoleMap(): Observable<Record<string, string[]>> {
    return this.http.get<Record<string, string[]>>(
      `${this.baseUrl}global/skill-role-map/`
    );
  }
}
