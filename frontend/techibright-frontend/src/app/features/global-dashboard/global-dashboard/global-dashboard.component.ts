import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/api.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-global-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './global-dashboard.component.html',
  styleUrls: ['./global-dashboard.component.scss']
})
export class GlobalDashboardComponent implements OnInit {

  skills: string[] = [];
  roles: any[] = [];
  skillMap: any = {};

  loading = true;

  selectedRole: any = null; // for popup

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    Promise.all([
      this.api.getGlobalSkills().toPromise(),
      this.api.getGlobalRoles().toPromise(),
      this.api.getSkillRoleMap().toPromise()
    ]).then((data) => {
      this.skills = data[0] as string[];
      this.roles = data[1] as any[];
      this.skillMap = data[2] as any;

      this.loading = false;
      this.cdr.detectChanges();
    });
  }

  openRole(role: any) {
    this.selectedRole = role;
  }

  closeRole() {
    this.selectedRole = null;
  }
}
