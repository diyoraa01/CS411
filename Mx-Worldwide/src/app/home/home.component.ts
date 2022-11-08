import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {

    readonly ROOT_URL = 'http://127.0.0.1:3052/';

    constructor(private http: HttpClient) {}

    songName: string='';

    search(data:NgForm){
        this.songName = data.value.songName;
        console.log(this.songName);
    

        this.http.post(this.ROOT_URL + 'api/search', {'songName': this.songName}).subscribe((res) => {
            console.log(res);
        });
    }
}