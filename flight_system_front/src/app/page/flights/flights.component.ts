import { Component, OnInit } from '@angular/core';
import { FlightsServiceService } from 'src/app/services/flights-service.service';

@Component({
  selector: 'app-flights',
  templateUrl: './flights.component.html',
  styleUrls: ['./flights.component.scss']
})
export class FlightsComponent implements OnInit {
  constructor(private flightsService: FlightsServiceService) {}

  ngOnInit(): void {
    this.getFlights();
  }

  getFlights() {
    this.flightsService.getFlights().subscribe(
      (response) => {
        console.log(response);
      },
      (error) => {
        console.log(error);
      }
    );
  }
}

