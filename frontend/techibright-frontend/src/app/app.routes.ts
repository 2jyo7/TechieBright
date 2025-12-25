import { Routes } from '@angular/router';
import { EmployeesComponent } from './features/employees/employees.component';
import { SkillsComponent } from './features/skills/skills.component';
import { RecommendComponent } from './features/recommend/recommend.component';
import { HistoryComponent } from './features/history/history.component';
import { GlobalDashboardComponent } from './features/global-dashboard/global-dashboard/global-dashboard.component';
import { EmployeeSkillEditorComponent } from './features/employee-skill-editor/employee-skill-editor.component';
import { EmployeeDashboardComponent } from './features/employee-dashboard/employee-dashboard.component';

export const routes: Routes = [
  { path: '', redirectTo: 'employees', pathMatch: 'full' },
  { path: 'employees', component: EmployeesComponent },
{ path: 'employee/skills/:userId', component: EmployeeSkillEditorComponent },
{ path: 'dashboard/:userId', component: EmployeeDashboardComponent },
  { path: 'skills', component: SkillsComponent },
  { path: 'recommend', component: RecommendComponent },
  { path: 'recommend/history', component: HistoryComponent },
  { path: 'global-dashboard', component: GlobalDashboardComponent },

];
