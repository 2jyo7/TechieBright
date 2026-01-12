import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  private readonly USER_KEY = 'techiebright_user';
  private readonly API = 'http://localhost:8000/api';

  private userSubject = new BehaviorSubject<any>(this.getUserFromStorage());
  user$ = this.userSubject.asObservable();

  constructor(private http: HttpClient) {
    this.verifySession();
  }

  /* ===============================
     SIGNUP
  =============================== */
  signup(data: {
    username: string;
    password: string;
    role: 'employee' | 'employer';
  }): Observable<any> {
    return this.http.post<any>(`${this.API}/auth/signup/`, data, {
      withCredentials: true,
    }).pipe(
      tap(user => this.setUser(user))
    );
  }

  /* ===============================
     LOGIN
  =============================== */
  login(data: {
    username: string;
    password: string;
  }): Observable<any> {
    return this.http.post<any>(`${this.API}/auth/login/`, data, {
      withCredentials: true,
    }).pipe(
      tap(user => this.setUser(user))
    );
  }

  /* ===============================
     LOGOUT
  =============================== */
  logout(): void {
    this.http.post(`${this.API}/auth/logout/`, {}, {
      withCredentials: true,
    }).subscribe({
      next: () => this.clearUser(),
      error: () => this.clearUser(),
    });
  }

  /* ===============================
     SESSION VALIDATION
  =============================== */
  private verifySession(): void {
    this.http.get<any>(`${this.API}/auth/me/`, {
      withCredentials: true,
    }).pipe(
      tap(user => this.setUser(user)),
      catchError(() => {
        this.clearUser();
        return of(null);
      })
    ).subscribe();
  }

  /* ===============================
     HELPERS
  =============================== */
  private setUser(user: any): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    this.userSubject.next(user);
  }

  private clearUser(): void {
    localStorage.removeItem(this.USER_KEY);
    this.userSubject.next(null);
  }

  private getUserFromStorage(): any | null {
    const user = localStorage.getItem(this.USER_KEY);
    return user ? JSON.parse(user) : null;
  }

  /* ===============================
     UTILITIES
  =============================== */
  get currentUser(): any {
    return this.userSubject.value;
  }

  isLoggedIn(): boolean {
    return !!this.userSubject.value;
  }
}
