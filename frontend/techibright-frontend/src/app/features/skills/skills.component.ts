import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';
import { Skill } from '../../models/skill.model';

@Component({
  selector: 'app-skills',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './skills.component.html',
})
export class SkillsComponent implements OnInit {

  skills: Skill[] = [];

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getSkills().subscribe({
      next: (res) => this.skills = res,
      error: (err) => console.error(err)
    });
  }
}
