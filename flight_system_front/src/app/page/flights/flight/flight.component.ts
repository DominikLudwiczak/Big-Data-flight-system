import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FlightsServiceService } from 'src/app/services/flights-service.service';
import { Flight } from 'src/models/flight';

@Component({
  selector: 'app-flight',
  templateUrl: './flight.component.html',
  styleUrls: ['./flight.component.scss']
})
export class FlightComponent implements OnInit {
  flight: Flight = {} as Flight;

  constructor(private flightService: FlightsServiceService,
              private route: ActivatedRoute
            ) {}

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.getFlight(params['id']);
    });
  }

  getFlight(flightId: string) {
    this.flightService.getFlight(flightId).subscribe((flight: Flight) => {
      this.flight = flight;
    });
  }
}
