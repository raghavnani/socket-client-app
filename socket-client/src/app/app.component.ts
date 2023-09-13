import { Component, OnInit } from '@angular/core';
import { io, Socket } from 'socket.io-client';
import { SwPush } from '@angular/service-worker';

import { NotificationService } from './notification.service';
import { News } from './models/models';
import { MatTableDataSource} from '@angular/material/table';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit  {
  title = 'socket-client';
  private socket: any;
  public data: any;

  displayedColumns = [
    
    'TIMESTAMP_UTC',
    'ENTITY_NAME',
    'TOPIC',
    'GROUP',
    'TYPE',
    'EVENT_RELEVANCE',
    'EVENT_SENTIMENT_SCORE',
    'FACT_LEVEL',
    'CATEGORY',
    'SOURCE_NAME',
    'HEADLINE'

  ]
  dataSource: MatTableDataSource<News[]>;

  SEARCH_STRING: any = null
  ENTITY_NAME:any = null
  TOPIC: any = null
  GROUP: any = null
  TYPE: any = null
  FACT_LEVEL: any = null
  CATEGORY: any = null
  SOURCE_NAME: any = null


  isEnabled = this.swPush.isEnabled;
  isGranted = Notification.permission === 'granted';

  constructor(private swPush: SwPush,
    private appService: NotificationService) {
    // Connect Socket with server URL
    this.dataSource = new MatTableDataSource();

    this.socket = io('http://104.131.126.10:5200');
    
  }
  public ngOnInit(): void {

    this.socket.on('notification', (data) => {
      this.dataSource.data.unshift(data);
      this.dataSource.data = this.dataSource.data.slice();      

      // alert("New News")
    });
  }

  
  onSubmit(){
    let params = {

      'SEARCH_STRING': this.SEARCH_STRING,
      'ENTITY_NAME' : this.ENTITY_NAME,
      'TOPIC': this.TOPIC,
      'GROUP': this.GROUP,
      'TYPE': this.TYPE,
      'CATEGORY': this.CATEGORY,
      'SOURCE_NAME': this.SOURCE_NAME,
      'FACT_LEVEL': this.FACT_LEVEL

        }

    console.log(params) 
    this.appService.getNews(params).subscribe()

    setTimeout(() => { console.log("World!"); }, 6000);
    
    this.dataSource = new MatTableDataSource();


    

  }

  // submitNotification(): void {
  //   this.webNotificationService.subscribeToNotification();
  // }

}



