import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { StorageServiceModule } from 'ngx-webstorage-service';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent, NgbdModalContent } from './app.component';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { LocalStorageService } from './app.service';
import { landingPageComponent } from './components/landing-page/landing-page.component';
import { GraphComponent } from './components/graph/graph.component';
import { DataService } from './services/data.service';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { AppEffects } from './redux/effects';
import * as AppReducers from './redux/reducers';
// import { offlineMetaReducer } from './redux/offline.metareducer';
import { SimpleNotificationsModule } from 'angular2-notifications';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { environment } from 'src/environments/environment';
import { SliderComponent } from './components/slider/slider.component';
import { NgxSliderModule } from '@angular-slider/ngx-slider'

import { CarouselModule } from 'ngx-owl-carousel-o';
import { SearchFormComponent } from './components/search-form/search-form.component';
import { AudioComponent, AudioService } from './components/audio/audio.component';
import { NodePopupComponent } from './components/node-popup/node-popup.component';
import { EdgePopupComponent } from './components/edge-popup/edge-popup.component';
import { RolesComponent } from './components/roles/roles.component';
import { GraphService } from './services/graph.service';
import { ThreeService } from './services/three.service';

@NgModule({
  declarations: [
    AppComponent,
    NgbdModalContent,
    landingPageComponent,
    GraphComponent,
    SliderComponent,
    SearchFormComponent,
    AudioComponent,
    NodePopupComponent,
    EdgePopupComponent,
    RolesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    ReactiveFormsModule,
    HttpClientModule,
    StorageServiceModule,
    StoreModule.forRoot(
      AppReducers.reducers,
      // {
      //   metaReducers: [offlineMetaReducer]
      // }
    ),
    StoreDevtoolsModule.instrument({
      maxAge: 25, // Retains last 25 states
      logOnly: environment.production, // Restrict extension to log-only mode
    }),
    EffectsModule.forRoot([AppEffects]),
    SimpleNotificationsModule.forRoot(),
    BrowserAnimationsModule,
    NgxSliderModule,
    CarouselModule
  ],
  providers: [
    // AppService,
    DataService,
    AudioService,
    LocalStorageService,
    GraphService,
    ThreeService
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
