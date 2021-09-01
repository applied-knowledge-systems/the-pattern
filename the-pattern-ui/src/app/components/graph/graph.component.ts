import { Component, OnInit, ViewChild, ElementRef, HostListener, Input } from '@angular/core';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { Store } from '@ngrx/store';
import { State } from '../../redux/state';
import * as AppSelectors from '../../redux/selectors';
import { filter, distinctUntilChanged } from 'rxjs/operators';
import * as THREE from 'three';
import { GraphService } from 'src/app/services/graph.service';


@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit {
  emptySearch = true;
  canvasHeight: number;
  canvasWidth: number;

  @ViewChild('graph', { static: true }) graph: ElementRef;
  @Input() renderer: string
  @Input() controller: string

  loading$;
  loadingState$;
  
  constructor(
    private store: Store<State>, 
    private graphService: GraphService
  ) { }

  ngOnInit() {
    this.canvasHeight = window.innerHeight - 128;
    this.canvasWidth = window.innerWidth;
    this.store.select<any>(AppSelectors.selectSearchResults)
      .pipe(
        filter(x => x!=null),
        distinctUntilChanged()
      ).subscribe((results) => {
        this.emptySearch = false;
        this.graphService.gData = results;
        this.graphService.populateGraph(this.graph.nativeElement, this.canvasHeight, this.canvasWidth, this.renderer);
      }
    );

    this.loading$ = this.store.select(AppSelectors.selectIsLoading)
    this.loadingState$ = this.store.select(AppSelectors.selectIsLoadingState)
  }

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.canvasHeight = window.innerHeight - 128;
    this.canvasWidth = window.innerWidth;
    this.graphService.populateGraph(this.graph.nativeElement, this.canvasHeight, this.canvasHeight, this.renderer)
  }

  postProcessing(){
    const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      1.5,
      0.4,
      0.85
    );
    bloomPass.threshold = 0;
    bloomPass.strength = 5;
    bloomPass.radius = 0;
    // const strength = 0.7;
    // const radius = 0.2;
    // const threshold = 0;
    // const bloomPass = new UnrealBloomPass(new Vector2(128, 128), strength, radius, threshold);
    // this.Graph.postProcessingComposer().addPass(bloomPass);
  }

  addRoomToScence(){
    // const room = new THREE.LineSegments(
    //   new BoxLineGeometry( 6, 6, 6, 10, 10, 10 ).translate( 0, 3, 0 ),
    //   new THREE.LineBasicMaterial( { color: 0x808080 } )
    // );
  
    // this.threeScene.add( room );
  }

}
