export class Flight {
    flight_id: string;
    departure_airport: string;
    arrival_airport: string;
    departure_time: Date;
    arrival_time: Date;
    capacity: number;
    booked_seats: Set<string>;

    constructor(flight_id: string, departure_airport: string, arrival_airport: string, departure_time: Date, arrival_time: Date, capacity: number, booked_seats: Set<string>) {
        this.flight_id = flight_id;
        this.departure_airport = departure_airport;
        this.arrival_airport = arrival_airport;
        this.departure_time = departure_time;
        this.arrival_time = arrival_time;
        this.capacity = capacity;
        this.booked_seats = booked_seats;
    }
}