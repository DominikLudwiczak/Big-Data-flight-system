import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Flight } from 'src/models/flight';

const API_URL: string = environment.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class FlightsServiceService {

  constructor(private httpClinet: HttpClient) { }

  getFlights(): Observable<Flight[]> {
    return this.httpClinet.get<Flight[]>(`${API_URL}/flights`);
  }

  getFlight(flightId: string): Observable<Flight> {
    return this.httpClinet.get<Flight>(`${API_URL}/flights/${flightId}`);
  }

  addFlight(flight: Flight): Observable<Flight> {
    return this.httpClinet.post<Flight>(`${API_URL}/flights`, flight);
  }

  deleteFlight(flightId: string): Observable<Flight> {
    return this.httpClinet.delete<Flight>(`${API_URL}/flights/${flightId}`);
  }
}
