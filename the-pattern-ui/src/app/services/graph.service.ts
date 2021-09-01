import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { MeshBasicMaterial, SphereGeometry, Mesh } from 'three';
import SpriteText from 'three-spritetext';
import { State } from '../redux/state';
import { Read, Set as SetStoreValue } from 'src/app/redux/actions.js';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { NodePopupComponent } from '../components/node-popup/node-popup.component';
import { EdgePopupComponent } from '../components/edge-popup/edge-popup.component';
import { ThreeService } from './three.service';

declare var ForceGraph3D;

@Injectable({
  providedIn: 'root'
})
export class GraphService {
  Graph: any;
  gData: any;

  constructor(
    private store: Store<State>, 
    private modalService: NgbModal,
    private threeService: ThreeService) { }

  populateGraph(htmlElement, height, width, renderType: string) {
    let highlightNodes = new Set();
    let highlightLinks = new Set();
    this.Graph = ForceGraph3D();
    this.Graph(htmlElement)
      .linkWidth(link => highlightLinks.has(link) ? 4 : 1)
      .linkDirectionalParticles(link => highlightLinks.has(link) ? 4 : 0)
      .linkDirectionalParticleWidth(4)
      .nodeAutoColorBy('rank')
      .nodeThreeObject(node => {
        // use a sphere as a drag handle
        const obj = new Mesh(
          new SphereGeometry(10),
          new MeshBasicMaterial({ depthWrite: false, transparent: true, opacity: 0 })
        );

        // add text sprite as child
        const sprite = new SpriteText(node.name);
        sprite.color = node.color;
        sprite.textHeight = 8;
        obj.add(sprite);

        return obj;
      })
      .linkHoverPrecision(5)
      .onLinkHover(link => {
        highlightNodes.clear();
        highlightLinks.clear();

        if (link) {
          highlightLinks.add(link);
          highlightNodes.add(link.source);
          highlightNodes.add(link.target);
        }

        this.updateHighlight();
      })
      .backgroundColor('#37474f')
      .height(height) // this.canvasHeight
      .width(width) // this.canvasWidth
      .graphData(this.gData)

    this.Graph.onNodeClick(this.onNodeClick.bind(this));
    this.Graph.onLinkClick(this.onLinkClick.bind(this));

    this.threeService.scene = this.Graph.scene();
    this.threeService.renderer = this.Graph.renderer();
    this.threeService.controls = this.Graph.controls();
    this.threeService.camera = this.Graph.camera();

    if(renderType === 'XR'){
      this.threeService.enableXRRenderer()
    }

    this.threeService.getDetails()

    // this.addEdgeDetailsContainer();
    // this.postProcessing();
  }

  onNodeClick(node, event){
    this.onGraphClick({ type: 'node', data: node })
  }

  onLinkClick(node, event){
    this.onGraphClick({ type: 'edge', data: node });
  }

  onLinkHover(node, event){
    this.onGraphClick({ type: 'edge', data: node });
  }

  updateHighlight() {
    // trigger update of highlighted objects in scene
    this.Graph
      .nodeColor(this.Graph.nodeColor())
      .linkWidth(this.Graph.linkWidth())
      .linkDirectionalParticles(this.Graph.linkDirectionalParticles());
  }

  onGraphClick(event){
    switch(event.type){
      case 'node':
        this.store.dispatch(new SetStoreValue({
          data: event.data,
          state: 'selectedNode'
        }));
        this.showNodeDetails()
        break;

      case 'edge':
        this.store.dispatch(new Read({
          state: 'edgeResults',
          route: `edge/edges:${event.data.source.id}:${event.data.target.id}`
        }));

        this.store.dispatch(new SetStoreValue({
          data: event.data,
          state: 'selected'
        }));
        this.showEdgeDetails()
        break;

      default:
        break;
    }
  }

  showNodeDetails() {
    this.modalService.open(NodePopupComponent, { size: 'sm', scrollable: true });
  }

  showEdgeDetails() {
    this.modalService.open(EdgePopupComponent, { size: 'xl', scrollable: true });
  }
}
