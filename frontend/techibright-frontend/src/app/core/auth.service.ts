import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { tap, catchError, switchMap, shareReplay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  private readonly USER_KEY = 'techiebright_user';
  private readonly API = '/api';


  private userSubject = new BehaviorSubject<any>(this.getUserFromStorage());
  user$ = this.userSubject.asObservable();

  // 🔑 CSRF readiness stream
  private csrfReady$: Observable<boolean>;

  constructor(private http: HttpClient) {
    this.csrfReady$ = this.initCsrf().pipe(shareReplay(1));
  }

  /* ===============================
     CSRF INITIALIZATION
  =============================== */
  private initCsrf(): Observable<boolean> {
    return this.http.get<any>(`${this.API}/auth/me/`, {
      withCredentials: true,
    }).pipe(
      tap(res => {
        if (res?.authenticated) {
          this.setUser(res);
        } else {
          this.clearUser();
        }
      }),
      switchMap(() => of(true)),
      catchError(() => {
        this.clearUser();
        return of(true); // still allow CSRF to be considered "ready"
      })
    );
  }

  /* ===============================
     SIGNUP (CSRF SAFE)
  =============================== */
  signup(data: {
    username: string;
    password: string;
    role: 'employee' | 'employer';
  }): Observable<any> {
    return this.csrfReady$.pipe(
      switchMap(() =>
        this.http.post<any>(`${this.API}/auth/signup/`, data, {
          withCredentials: true,
        })
      ),
      tap(user => this.setUser(user))
    );
  }

  /* ===============================
     LOGIN (CSRF SAFE)
  =============================== */
  login(data: {
    username: string;
    password: string;
  }): Observable<any> {
    return this.csrfReady$.pipe(
      switchMap(() =>
        this.http.post<any>(`${this.API}/auth/login/`, data, {
          withCredentials: true,
        })
      ),
      tap(user => this.setUser(user))
    );
  }

  /* ===============================
     LOGOUT (CSRF SAFE)
  =============================== */
  logout(): Observable<any> {
    return this.csrfReady$.pipe(
      switchMap(() =>
        this.http.post(`${this.API}/auth/logout/`, {}, {
          withCredentials: true,
        })
      ),
      tap(() => this.clearUser()),
      catchError(() => {
        this.clearUser();
        return of(null);
      })
    );
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
    return !!this.userSubject.value?.authenticated;
  }
}
