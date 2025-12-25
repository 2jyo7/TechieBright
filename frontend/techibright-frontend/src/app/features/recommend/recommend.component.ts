import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { AIRecommendation } from '../../models/ai.model';

@Component({
  selector: 'app-recommend',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './recommend.component.html',
  styleUrls: ['./recommend.component.scss']
})
export class RecommendComponent {

  query = '';
  user_id = 1;  // later dynamic (login)
  loading = false;
  errorMsg = '';
  recommendation: AIRecommendation | null = null;

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  getRecommendation() {
    if (!this.query.trim()) {
      this.errorMsg = 'Please enter a query.';
      return;
    }

    this.loading = true;
    this.errorMsg = '';
    this.recommendation = null; // reset UI immediately

    this.api.aiRecommend({ user_id: this.user_id, query: this.query })
      .subscribe({
        next: (res) => {
          // Force Angular change detection (fixes the double-click issue)
          this.recommendation = structuredClone(res.recommendation);

          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (err) => {
          this.loading = false;
          this.errorMsg = err?.error?.error || 'Something went wrong.';
          this.cdr.detectChanges();
        }
      });
  }
}
