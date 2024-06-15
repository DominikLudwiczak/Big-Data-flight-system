import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BookingsServiceService } from 'src/app/services/bookings-service.service';
import { FlightsServiceService } from 'src/app/services/flights-service.service';
import { Flight } from 'src/models/flight';
import {Location} from '@angular/common';

@Component({
  selector: 'app-edit-booking',
  templateUrl: './edit-booking.component.html',
  styleUrls: ['./edit-booking.component.scss']
})
export class EditBookingComponent implements OnInit {
  bookingId: string = "";
  flightId: string = "";
  flights: Flight[] = [];

  constructor(private bookingService: BookingsServiceService,
              private flightService: FlightsServiceService,
              private route: ActivatedRoute,
              private router: Router,
              private _location: Location
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.bookingId = params['booking_id'];
    });
    this.getFlights();
  }

  getFlights() {
    this.flightService.getFlights().subscribe(
      (data) => {
        this.flights = data;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  updateBooking() {
    this.bookingService.updateBooking(this.bookingId, this.flightId).subscribe(
      (data) => {
        this.router.navigate(['/panel/bookings/flight', this.flightId]);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  goBack() {
    this._location.back();
  }
}
