import { Component, AfterViewInit, Input, OnInit } from '@angular/core';


import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AppService } from './app.service.js';
import { Store } from '@ngrx/store';

import { AppState } from './redux/state';
import { Create, Read, Set } from './redux/actions.js';

@Component({
  selector: 'ngbd-modal-content',
  template: `
    <div class="modal-header">
      <h4 class="modal-title" *ngIf="type == 'node'">Node Data</h4>
      <h4 class="modal-title" *ngIf="type == 'edge'">{{ (edgeResults$ | async)?.title }}</h4>
      <button type="button" class="close" aria-label="Close" (click)="activeModal.dismiss('Cross click')">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="modal-body">
      <p *ngIf="type == 'node'">Hello, Node data will be viewed here!</p>
      <p *ngIf="type == 'edge'">
        {{ (edgeResults$ | async)?.sentence }}
      </p>
    </div>
    <div class="modal-footer">
      <button type="button" class="btn btn-outline-dark" (click)="activeModal.close('Close click')">Close</button>
    </div>
  `
})
export class NgbdModalContent implements OnInit{
  @Input() type;
  @Input() node;
  @Input() edge;

  edgeResults$: any;

  constructor(
    public activeModal: NgbActiveModal,
    private service: AppService) {}

  ngOnInit(){
    this.edgeResults$ = this.service.edgeApi(this.edge.source.id, this.edge.target.id);
  }
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  
  constructor(
    private store: Store<AppState>){
  }

  ngOnInit(){}

  

  

}
