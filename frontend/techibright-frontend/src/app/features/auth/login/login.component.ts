import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {

  loading = false;
  error = '';

  formData = {
    username: '',
    password: '',
  };

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  submit() {
    this.loading = true;
    this.error = '';

    this.auth.login(this.formData).subscribe({
      next: (user) => {
        this.loading = false;

        if (!user) {
          this.router.navigate(['/login']);
          return;
        }

        if (user.role === 'employee') {
          this.router.navigate(['/employee/profile']);
        } else {
          this.router.navigate(['/employees']);
        }
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.error || 'Invalid credentials';
         // force UI back to logged-out state
        this.auth['clearUser']?.();
      }
    });
  }
}
