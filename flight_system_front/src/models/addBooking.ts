export class AddBooking {
    flight_id: string;
    num_seats: number;
    passenger_names: string[];

    constructor(flight_id: string, num_seats: number, passenger_names: string[]) {
        this.flight_id = flight_id;
        this.num_seats = num_seats;
        this.passenger_names = passenger_names;
    }
}