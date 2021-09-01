import { Injectable } from '@angular/core';
import {VRButton} from 'three/examples/jsm/webxr/VRButton';
import ThreeMeshUI from 'three-mesh-ui';

@Injectable({
  providedIn: 'root'
})
export class ThreeService {

  scene: any;
  renderer: any;
  controls: any;
  camera: any;

  constructor() { }

  enableXRRenderer(){
    this.renderer.xr.enabled = true;
    document.body.appendChild(VRButton.createButton(this.renderer));
    this.renderer.setAnimationLoop(() => {
      this.renderer.render(this.scene, this.camera)
    });    
  }

  addPopupContainer(){
    console.log('edge')
    const container = new ThreeMeshUI.Block({
      width: 1.2,
      height: 0.7,
      padding: 0.2,
      fontFamily: '../../../assets/Roboto-msdf.json',
      fontTexture: '.../../../assets/Roboto-msdf.png',
     });

    const text = new ThreeMeshUI.Text({
      content: "Some text to be displayed"
    });

    container.position.set( 0, 1, -1.8 );
    container.rotation.x = 0;
     
    container.add( text );
    this.scene.add( container );
  }

  getDetails(){
    console.log(this.camera)
    console.log(this.controls)
    console.log(this.scene)
    console.log(this.renderer)
  }
}
