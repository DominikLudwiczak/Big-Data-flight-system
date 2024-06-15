import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormArray, FormControl, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { BookingsServiceService } from 'src/app/services/bookings-service.service';
import { FlightsServiceService } from 'src/app/services/flights-service.service';
import { AddBooking } from 'src/models/addBooking';
import {Location} from '@angular/common';

export function passengerNamesMatchSeats(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    if (!(control instanceof FormGroup)) {
      throw new Error('passengerNamesMatchSeats validator must be used on a FormGroup');
    }

    const formGroup = control as FormGroup;
    const numSeats = formGroup.get('num_seats')?.value;
    const passengerNames = formGroup.get('passenger_names')?.value;

    if (!numSeats || !passengerNames) {
      return null;
    }

    const valid = passengerNames.length === numSeats;
    return !valid ? { passengerNamesMatchSeats: true } : null;
  };
}

@Component({
  selector: 'app-add-booking',
  templateUrl: './add-booking.component.html',
  styleUrls: ['./add-booking.component.scss']
})

export class AddBookingComponent implements OnInit {
  bookingForm: FormGroup = new FormGroup({
    flight_id: new FormControl('', Validators.required),
    num_seats: new FormControl('', [Validators.required, Validators.min(1)]),
    passenger_names: new FormArray([], Validators.required),
  }, { validators: passengerNamesMatchSeats });

  constructor(private bookingService: BookingsServiceService,
              private flightService: FlightsServiceService,
              private route: ActivatedRoute,
              private router: Router,
              private _location: Location
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.bookingForm.get('flight_id')?.setValue(params['flight_id']);
    });
  }

  get passengerNames() {
    return this.bookingForm.get('passenger_names') as FormArray;
  }

  addPassengers() {
    const numSeats = this.bookingForm.get('num_seats')?.value;
    if (numSeats) {
      const numPassengers = this.passengerNames.value.length;
      
      if (numPassengers < numSeats) {
        for (let i = 0; i < numSeats - numPassengers; i++) {
          this.passengerNames.push(new FormControl('', Validators.required));
        }
      } else {
        while (this.passengerNames.value.length > numSeats) {
          this.passengerNames.removeAt(this.passengerNames.value.length - 1);
        }
      }
    }
  }

  addBooking() {
    if (this.bookingForm.valid) {
      this.bookingService.addBooking(this.bookingForm.value as AddBooking).subscribe(
        (data) => {
          this.router.navigate(['/panel/bookings/flight', this.bookingForm.get('flight_id')?.value]);
        },
        (error) => {
          console.log(error);
        }
      );
    }
  }

  goBack() {
    this._location.back();
  }
}
