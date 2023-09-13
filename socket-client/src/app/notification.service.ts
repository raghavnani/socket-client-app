import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SwPush } from '@angular/service-worker';
import { News } from './models/models';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  // readonly VAPID_PUBLIC_KEY = '<VAPID-PUBLIC-KEY-HERE>';
  private baseUrl = 'http://104.131.126.10:5200';

  constructor(private http: HttpClient) { }

  //   subscribeToNotification() {
  //     this.swPush.requestSubscription({
  //         serverPublicKey: this.VAPID_PUBLIC_KEY
  //     })
  //     .then(sub => this.sendToServer(sub))
  //     .catch(err => console.error('Could not subscribe to notifications', err));
  //   }


  getNews(params):Observable<any>{

    console.log(params)

    let event_count  = this.http.post<any>(this.baseUrl+'/api/search', params);
    return event_count


  }
}
