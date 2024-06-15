import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BookingsServiceService } from 'src/app/services/bookings-service.service';
import { Booking } from 'src/models/booking';

@Component({
  selector: 'app-bookings',
  templateUrl: './bookings.component.html',
  styleUrls: ['./bookings.component.scss']
})
export class BookingsComponent implements OnInit {
  flightId: string = "";
  bookings: Booking[] = [];

  constructor(private bookingsService: BookingsServiceService,
              private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.flightId = params['flight_id'];
      this.getBookings();
    });
  }

  getBookings() {
    this.bookingsService.getBookings(this.flightId).subscribe(
      (data) => {
        this.bookings = data;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  deleteBooking(bookingId: string) {
    this.bookingsService.deleteBooking(bookingId).subscribe(
      (data) => {
        this.getBookings();
      },
      (error) => {
        console.error(error);
      }
    );
  }
}
