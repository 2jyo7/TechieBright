import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GlobalDashboardComponent } from './global-dashboard.component';

describe('GlobalDashboard', () => {
  let component: GlobalDashboardComponent;
  let fixture: ComponentFixture<GlobalDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GlobalDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GlobalDashboardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
