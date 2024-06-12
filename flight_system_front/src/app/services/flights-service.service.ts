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

  getFlights(): Observable<any> {
    return this.httpClinet.get<any>(`${API_URL}/flights`);
  }
}
