import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SharedModule } from './shared/shared.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialsModule } from './materials/materials.module';
import { MainComponent } from './page/main/main.component';
import { FlightsComponent } from './page/flights/flights.component';
import { SearchFlightComponent } from './page/search-flight/search-flight.component';
import { FlightComponent } from './page/flights/flight/flight.component';

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    FlightsComponent,
    SearchFlightComponent,
    FlightComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    SharedModule,
    BrowserAnimationsModule,
    MaterialsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
