export class AddBooking {
    flight_id: string;
    booking_id: string;
    seat_number: string;
    passenger_name: string;

    constructor(flight_id: string, booking_id: string, seat_number: string, passenger_name: string) {
        this.flight_id = flight_id;
        this.booking_id = booking_id;
        this.seat_number = seat_number;
        this.passenger_name = passenger_name;
    }
}