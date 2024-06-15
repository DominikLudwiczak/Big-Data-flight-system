import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Booking } from 'src/models/booking';
import { AddBooking } from 'src/models/addBooking';

const API_URL: string = environment.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class BookingsServiceService {

  constructor(private httpClinet: HttpClient) { }

  getBookings(flightId: string): Observable<Booking[]> {
    return this.httpClinet.get<Booking[]>(`${API_URL}/bookings/${flightId}`);
  }

  addBooking(booking: AddBooking): Observable<AddBooking> {
    return this.httpClinet.post<AddBooking>(`${API_URL}/bookings?flight_id=${booking.flight_id}&num_seats=${booking.num_seats}`, booking.passenger_names);
  }

  updateBooking(bookingId: string, newFlightId: string): Observable<Booking> {
    return this.httpClinet.put<Booking>(`${API_URL}/bookings/${bookingId}?bookId=${bookingId}&flightId=${newFlightId}`, null);
  }

  deleteBooking(bookingId: string): Observable<Booking> {
    return this.httpClinet.delete<Booking>(`${API_URL}/bookings/${bookingId}`);
  }
}
