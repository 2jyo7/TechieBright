import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmployeeSkillEditor } from './employee-skill-editor.component';

describe('EmployeeSkillEditor', () => {
  let component: EmployeeSkillEditor;
  let fixture: ComponentFixture<EmployeeSkillEditor>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmployeeSkillEditor]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmployeeSkillEditor);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
