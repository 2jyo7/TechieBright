import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Employee } from '../models/employee.model';
import { Skill } from '../models/skill.model';
import { AIRecommendation } from '../models/ai.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://localhost:8000/api/';

  constructor(private http: HttpClient) {}

  getEmployees(): Observable<Employee[]> {
    return this.http.get<Employee[]>(`${this.baseUrl}employees/`);
  }

  addEmployee(data: Employee): Observable<any> {
    return this.http.post(`${this.baseUrl}employees/add/`, data);
  }

 updateEmployeeSkillsByUser(userId: number, skills: string[]) {
  return this.http.put(`${this.baseUrl}employees/by-user/${userId}/update-skills/`, { skills });
}



  getSkills(): Observable<Skill[]> {
    return this.http.get<Skill[]>(`${this.baseUrl}skills/`);
  }

  aiRecommend(payload: { user_id: number; query: string }): Observable<{ recommendation: AIRecommendation }> {
    return this.http.post<{ recommendation: AIRecommendation }>(
      `${this.baseUrl}recommend/`,
      payload
    );
  }

  getRecommendationHistory(user_id: number) {
  return this.http.get<any[]>(`${this.baseUrl}recommend/history/${user_id}/`);
}


deleteRecommendation(id: number) {
  return this.http.delete(`${this.baseUrl}recommend/delete/${id}/`);
}

editRecommendation(id: number, query: string) {
  return this.http.put(`${this.baseUrl}recommend/edit/${id}/`, { query });
}

getGlobalSkills() {
  return this.http.get<string[]>(`${this.baseUrl}global/skills/`);
}

getGlobalRoles() {
  return this.http.get<any[]>(`${this.baseUrl}global/roles/`);
}

getSkillRoleMap() {
  return this.http.get<any>(`${this.baseUrl}global/skill-role-map/`);
}


getEmployeeById(userId: number) {
  return this.http.get<any>(`${this.baseUrl}employees/${userId}/`);
}



}
