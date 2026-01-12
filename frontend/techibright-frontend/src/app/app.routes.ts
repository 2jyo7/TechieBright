import { Routes } from '@angular/router';

import { EmployeesComponent } from './features/employees/employees.component';
import { RecommendComponent } from './features/recommend/recommend.component';
import { HistoryComponent } from './features/history/history.component';
import { GlobalDashboardComponent } from './features/global-dashboard/global-dashboard/global-dashboard.component';
import { EmployeeSkillEditorComponent } from './features/employee-skill-editor/employee-skill-editor.component';
import { EmployeeDashboardComponent } from './features/employee-dashboard/employee-dashboard.component';
import { LoginComponent } from './features/auth/login/login.component';
import { RegisterComponent } from './features/auth/register/register.component';
import { ProfileComponent } from './features/profile/profile.component';
import { RoleGuard } from './core/guards/role-guard';


export const routes: Routes = [

  // =========================
  // PUBLIC
  // =========================
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  // =========================
  // EMPLOYEE ONLY
  // =========================
  {
    path: 'employee/profile',
    component: ProfileComponent,
    canActivate: [RoleGuard],
    data: { roles: ['employee'] }
  },
  {
    path: 'employee/dashboard',
    component: EmployeeDashboardComponent,
    canActivate: [RoleGuard],
    data: { roles: ['employee'] }
  },
  {
    path: 'recommend',
    component: RecommendComponent,
    canActivate: [RoleGuard],
    data: { roles: ['employee'] }
  },
  {
    path: 'recommend/history',
    component: HistoryComponent,
    canActivate: [RoleGuard],
    data: { roles: ['employee'] }
  },

  // =========================
  // EMPLOYER ONLY
  // =========================
  {
    path: 'employees',
    component: EmployeesComponent,
    canActivate: [RoleGuard],
    data: { roles: ['employer'] }
  },

  // =========================
  // SHARED
  // =========================
  {
    path: 'global-dashboard',
    component: GlobalDashboardComponent,
    canActivate: [RoleGuard],
    data: { roles: ['employee', 'employer'] }
  },

  { path: '', redirectTo: 'global-dashboard', pathMatch: 'full' }
];
