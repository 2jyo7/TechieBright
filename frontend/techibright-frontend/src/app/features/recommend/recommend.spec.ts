import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RecommendComponent } from './recommend.component';

describe('Recommend', () => {
  let component: RecommendComponent;
  let fixture: ComponentFixture<RecommendComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecommendComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RecommendComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
