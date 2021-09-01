import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { GraphComponent } from './components/graph/graph.component';
import { landingPageComponent } from './components/landing-page/landing-page.component';
import { RolesComponent } from './components/roles/roles.component';


const routes: Routes = [
  { 
    path: '', 
    component: landingPageComponent 
  },
  { 
    path: 'search', 
    component: GraphComponent 
  },
  { 
    path: 'start', 
    component: RolesComponent,
    data: {
      mode: 'role-selector'
    } 
  },
  { 
    path: 'view/:role/:id', 
    component: RolesComponent,
    data: {
      mode: '3d-viewer'
    } 
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
