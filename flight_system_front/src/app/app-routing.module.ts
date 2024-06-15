import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FlightsComponent } from './page/flights/flights.component';
import { MainComponent } from './page/main/main.component';
import { FlightComponent } from './page/flights/flight/flight.component';
import { BookingsComponent } from './page/bookings/bookings.component';
import { AddBookingComponent } from './page/bookings/add-booking/add-booking.component';
import { EditBookingComponent } from './page/bookings/edit-booking/edit-booking.component';

const routes: Routes = [
  { path: '', redirectTo: 'panel', pathMatch: 'full' },
  {
    path: 'panel',
    component: MainComponent,
    children: [
      { path: '', redirectTo: 'flights', pathMatch: 'full' },
      { path: 'flights', component: FlightsComponent },
      { path: 'flights/:id', component: FlightComponent },

      { path: 'bookings/flight/:flight_id', component: BookingsComponent },
      { path: 'bookings/add/:flight_id', component: AddBookingComponent },
      { path: 'bookings/edit/:booking_id', component: EditBookingComponent },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
