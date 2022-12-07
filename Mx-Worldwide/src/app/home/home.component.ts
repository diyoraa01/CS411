import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {

    readonly ROOT_URL = 'http://127.0.0.1:3052/';

    constructor(private http: HttpClient) {}

    songName: string='';
    artist: string='';
    trackURL: string='';
    lyrics: string='';

    search(data:NgForm){
        this.songName = data.value.songName;
        this.artist = data.value.artistName;
        console.log(this.songName);
        console.log(this.artist);
    
        this.http.post(this.ROOT_URL + 'api/search', {'songName': this.songName}).subscribe((res) => {
            console.log(res);

            Object.values(res).forEach((value) => {
                this.trackURL = value;
                console.log(this.trackURL);
            });
        });

        this.reloadAudio(this.trackURL);
    
        this.http.post(this.ROOT_URL + 'api/lyrics', {'artist': this.artist, 'songName': this.songName}).subscribe((res) => {
            console.log(res)
            Object.values(res).forEach((value) => {
                this.lyrics = value;
                console.log(this.lyrics);
            });
        });
    }





    // Needs to be fixed so that two form submissions aren't needed for the player to be updated
    reloadAudio(trackUrl:string){
        var audio = document.getElementById('audioPlayer') as HTMLAudioElement;
        console.log(trackUrl);
        audio.setAttribute('src', trackUrl);
        audio.load();
    }
}