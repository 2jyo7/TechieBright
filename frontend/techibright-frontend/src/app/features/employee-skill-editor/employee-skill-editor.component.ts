import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-employee-skill-editor',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './employee-skill-editor.component.html',
  styleUrls: ['./employee-skill-editor.component.scss']
})
export class EmployeeSkillEditorComponent implements OnInit {

  userId!: number;         // get from route
  allSkills: string[] = [];
  filteredSkills: string[] = [];

  selectedSkills: string[] = [];
  searchTerm = "";

  loading = true;
  message = "";

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.userId = Number(this.route.snapshot.paramMap.get("userId"));

    // Load global skills
    this.api.getGlobalSkills().subscribe((skills) => {
      this.allSkills = skills;
      this.filteredSkills = skills;
      this.loading = false;
      this.cdr.detectChanges();
    });
  }

  search() {
    const term = this.searchTerm.toLowerCase();
    this.filteredSkills = this.allSkills.filter(skill =>
      skill.toLowerCase().includes(term)
    );
  }

  selectSkill(skill: string) {
    if (!this.selectedSkills.includes(skill)) {
      this.selectedSkills.push(skill);
    }
    this.searchTerm = "";
    this.filteredSkills = this.allSkills;
  }

  removeSkill(skill: string) {
    this.selectedSkills = this.selectedSkills.filter(s => s !== skill);
  }

  saveSkills() {
    this.api.updateEmployeeSkillsByUser(this.userId, this.selectedSkills).subscribe({
      next: () => {
        this.message = "Skills updated successfully!";
        this.cdr.detectChanges();
      }
    });
  }
}
