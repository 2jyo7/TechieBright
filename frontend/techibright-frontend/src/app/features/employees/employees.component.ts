import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { Employee } from '../../models/employee.model';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-employees',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.scss']
})
export class EmployeesComponent implements OnInit {

  employees: Employee[] = [];

  newEmployee: Employee = {
    country: '',
    job_title: '',
    age: 0,
    race: '',
    experience_years: 0,
    salary: 0,
    industry: '',
    work_type: ''
  };

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadEmployees();
  }

  loadEmployees() {
    this.api.getEmployees().subscribe({
      next: (res) => {
        this.employees = res;
        // console.log('Employees loaded:', res);
        this.cdr.detectChanges(); // 🔥 force UI update
      },
      error: (err) => console.error(err)
    });
  }

  addEmployee() {
    this.api.addEmployee(this.newEmployee).subscribe({
      next: () => {
        alert('Employee added!');

        this.newEmployee = {
          country: '',
          job_title: '',
          age: 0,
          race: '',
          experience_years: 0,
          salary: 0,
          industry: '',
          work_type: ''
        };

        this.loadEmployees();
        this.cdr.detectChanges();
      },
      error: (err) => console.error(err)
    });
  }
}
