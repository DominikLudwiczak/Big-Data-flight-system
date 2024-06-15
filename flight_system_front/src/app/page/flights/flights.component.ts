import { Component, OnInit } from '@angular/core';
import { FlightsServiceService } from 'src/app/services/flights-service.service';
import { Flight } from 'src/models/flight';

@Component({
  selector: 'app-flights',
  templateUrl: './flights.component.html',
  styleUrls: ['./flights.component.scss']
})
export class FlightsComponent implements OnInit {
  flights: Flight[] = [];

  constructor(private flightsService: FlightsServiceService) {}

  ngOnInit(): void {
    this.getFlights();
  }

  getFlights() {
    this.flightsService.getFlights().subscribe(
      (response) => {
        this.flights = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }
}

