import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {

  user_id = 1;
  history: any[] = [];
  loading = true;
  error = '';

  constructor(private api: ApiService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.api.getRecommendationHistory().subscribe({
      next: (res) => {
        this.history = structuredClone(res);  // ⬅ ensures new object reference
        this.loading = false;

        this.cdr.detectChanges(); // ⬅ FORCE Angular to update UI
      },
      error: (err) => {
        this.error = err?.error?.error || "Failed to load history.";
        this.loading = false;

        this.cdr.detectChanges(); // ⬅ also needed in error case
      }
    });
  }

  deleteItem(id: number) {
  if (!confirm("Are you sure you want to delete this item?")) return;

  this.api.deleteRecommendation(id).subscribe({
    next: () => {
      this.history = this.history.filter(item => item.id !== id);
      this.cdr.detectChanges();
    }
  });
}

editItem(item: any) {
  const newQuery = prompt("Edit your query:", item.query);
  if (!newQuery || newQuery.trim() === "") return;

  this.api.editRecommendation(item.id, newQuery).subscribe({
    next: () => {
      item.query = newQuery;
      this.cdr.detectChanges();
    }
  });
}

}
