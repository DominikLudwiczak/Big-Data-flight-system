import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from "@angular/common/http";
import { Observable } from "rxjs";

export class AuthInterceptor implements HttpInterceptor {

  constructor() { }

  intercept(req: HttpRequest<any>,
    next: HttpHandler): Observable<HttpEvent<any>> {

    req = req.clone({
      headers: req.headers.set('Content-Type', 'application/json').set('Access-Control-Allow-Origin', '*')
    });
    
    return next.handle(req);
  }
}
