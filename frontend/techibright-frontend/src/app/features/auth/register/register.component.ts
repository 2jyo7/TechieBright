import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent {

  loading = false;
  error = '';

  formData = {
    username: '',
    password: '',
    confirmPassword: '',
    role: 'employee' as 'employee' | 'employer',
  };

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  submit() {
    this.error = '';

    if (this.formData.password !== this.formData.confirmPassword) {
      this.error = 'Passwords do not match';
      return;
    }

    this.loading = true;

    this.auth.signup({
      username: this.formData.username,
      password: this.formData.password,
      role: this.formData.role,
    }).subscribe({
      next: (user) => {
        this.loading = false;

        if (user.role === 'employee') {
          this.router.navigate(['/employee/profile']);
        } else {
          this.router.navigate(['/employees']);
        }
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.error || 'Registration failed';
      }
    });
  }
}
