import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

  loading = true;
  saving = false;
  message = '';
  error = '';

  profile = {
    job_title: '',
    industry: '',
    experience_years: 0,
    work_type: 'remote',
    country: '',
    age: 0,
    race: '',
    salary: 0,
    skills: [] as string[],
  };

  newSkill = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadProfile();
  }

  loadProfile() {
    this.api.getMyProfile().subscribe({
      next: (res) => {
        this.profile = { ...this.profile, ...res };
        console.log(this.profile);
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load profile';
        this.loading = false;
      }
    });
  }

  saveProfile() {
    this.saving = true;
    this.message = '';

    const {
      job_title,
      industry,
      experience_years,
      work_type,
       country,
      age,
      race,
      salary,
    } = this.profile;

    this.api.updateMyProfile({
      job_title,
      industry,
      experience_years,
      work_type,
      country,
      age,
      race,
      salary
    }).subscribe({
      next: () => {
        this.message = 'Profile updated successfully';
        this.saving = false;
      },
      error: () => {
        this.error = 'Failed to update profile';
        this.saving = false;
      }
    });
  }

  // -------------------
  // SKILLS
  // -------------------

  addSkill() {
    if (!this.newSkill.trim()) return;

    if (!this.profile.skills.includes(this.newSkill)) {
      this.profile.skills.push(this.newSkill.trim());
      this.updateSkills();
    }

    this.newSkill = '';
  }

  removeSkill(skill: string) {
    this.profile.skills = this.profile.skills.filter(s => s !== skill);
    this.updateSkills();
  }

 updateSkills() {
  this.api.updateMySkills(this.profile.skills).subscribe({
    error: () => {
      this.error = 'Failed to update skills';
    }
  });
}

}
