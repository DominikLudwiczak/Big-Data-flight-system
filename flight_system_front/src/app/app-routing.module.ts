import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FlightsComponent } from './page/flights/flights.component';
import { MainComponent } from './page/main/main.component';
import { SearchFlightComponent } from './page/search-flight/search-flight.component';
import { FlightComponent } from './page/flights/flight/flight.component';

const routes: Routes = [
  { path: '', redirectTo: 'panel', pathMatch: 'full' },
  {
    path: 'panel',
    component: MainComponent,
    children: [
      { path: '', redirectTo: 'flights', pathMatch: 'full' },
      { path: 'flights', component: FlightsComponent },
      { path: 'flights/:id', component: FlightComponent },
      { path: 'search', component: SearchFlightComponent },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
