import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Mx-Worldwide';

  readonly ROOT_URL = 'http://127.0.0.1:3052/';

  constructor(private http: HttpClient) {}

  hello: any;

  // Flask Hello World Test
  // sayHello() {
  //   this.http.get(this.ROOT_URL + 'api/hello').subscribe(data => {
  //     this.hello = data as JSON;});
  //   console.log(this.hello);
  // }


}
