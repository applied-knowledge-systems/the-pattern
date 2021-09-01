import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EdgePopupComponent } from './edge-popup.component';

describe('EdgePopupComponent', () => {
  let component: EdgePopupComponent;
  let fixture: ComponentFixture<EdgePopupComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EdgePopupComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EdgePopupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
