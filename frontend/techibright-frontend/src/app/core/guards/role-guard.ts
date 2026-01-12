import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { map, take } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  canActivate(route: ActivatedRouteSnapshot) {
    const allowedRoles = route.data['roles'] as string[];

    return this.auth.user$.pipe(
      take(1),
      map(user => {

        //  Not logged in
        if (!user) {
          this.router.navigate(['/login']);
          return false;
        }

        //  Role not allowed
        if (allowedRoles && !allowedRoles.includes(user.role)) {
          this.router.navigate(['/']);
          return false;
        }

        // ✅ Allowed
        return true;
      })
    );
  }
}
