export class Booking {
    booking_id: string;
    flight_id: string;
    passenger_name: string;
    seat_number: string;

    constructor(booking_id: string, flight_id: string, passenger_name: string, seat_number: string) {
        this.booking_id = booking_id;
        this.flight_id = flight_id;
        this.passenger_name = passenger_name;
        this.seat_number = seat_number;
    }
}