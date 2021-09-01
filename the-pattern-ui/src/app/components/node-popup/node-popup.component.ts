import { Component, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { Store } from '@ngrx/store';
import {State} from '../../redux/state';
import * as AppSelectors from '../../redux/selectors';
import { distinctUntilChanged, filter } from 'rxjs/operators';
import { Read } from 'src/app/redux/actions';
@Component({
  selector: 'app-node-popup',
  templateUrl: './node-popup.component.html',
  styleUrls: ['./node-popup.component.scss']
})
export class NodePopupComponent implements OnInit {
  node: any;
  nodeResults$: any;
  term:any;
  constructor(
    public activeModal: NgbActiveModal,
    private store: Store<State>
  ) {
    this.store.select(AppSelectors.selectedNode)
      .pipe(distinctUntilChanged())
      .pipe(filter(x => x!=null))
      .subscribe(node => {
        this.node = node;
      }
    );
  }

  ngOnInit(): void {
    this.store.select(AppSelectors.selectSearchTerm).subscribe(term => {
      this.term=term;
    });
  }

  notImportant(){
    // request for node results
     this.store.dispatch(new Read({
          route: 'exclude?id='+this.node.id,
          state: `excludeNode`,
          postProcess:'notImportant'
     }));
    this.activeModal.close()
  }

}
