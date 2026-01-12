import { Component, OnInit, ChangeDetectorRef, NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-employee-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './employee-dashboard.component.html',
  styleUrls: ['./employee-dashboard.component.scss']
})
export class EmployeeDashboardComponent implements OnInit {


  employee: any;
  loading = true;
  selectedRole = '';
gapResult: any = null;
roles: any[] = [];

  constructor(
   
    private api: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    
     this.loadRoles();
  }

  

  loadRoles() {
  this.api.getGlobalRoles().subscribe(res => {
    this.roles = res;
  });
}

analyzeGap() {
  this.api.analyzeSkillGap(this.selectedRole)
    .subscribe(res => {
      this.gapResult = res;
      console.log('Gap Analysis Result:', this.gapResult);
       this.cdr.detectChanges();
    });
}
}


