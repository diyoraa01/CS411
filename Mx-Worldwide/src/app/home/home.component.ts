import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {

    readonly ROOT_URL = 'http://127.0.0.1:3052/';

    constructor(private http: HttpClient) {}

    // Variable Definition
    songName: string='';
    artist: string='';
    trackURL: string='';
    lyrics: string='Lyrics go here';
    imageURL: string='https://developer.spotify.com/assets/branding-guidelines/icon4@2x.png';
    translation: string='Translation goes here';

    // Send APIs form data
    search(data:NgForm){
        this.songName = data.value.songName;
        this.artist = data.value.artist;
        console.log(this.songName);
        console.log(this.artist);
    
        // Extract API response for image and track
        this.http.post(this.ROOT_URL + 'api/search', {'songName': this.songName, 'artist': this.artist}).subscribe((res) => {
            console.log(res);
            Object.values(res).forEach((value) => {
                if (value.includes('image')) {
                    this.imageURL = value;
                    console.log(this.imageURL);
                }
                else {
                    this.trackURL = value;
                    console.log(this.trackURL);
                }
            });
        });

        this.reloadAudio(this.trackURL);

        // Extract API response for lyrics
        this.http.post(this.ROOT_URL + 'api/lyrics', {'artist': this.artist, 'songName': this.songName}).subscribe((res) => {
            console.log(res)
            Object.values(res).forEach((value) => {
                if (value.includes('Lyrics')) {
                    this.lyrics = value;
                    console.log(this.lyrics);
                }
            });
        });

        // Extract API response for translated lyrics
        this.http.post(this.ROOT_URL + 'api/translate', {'originalLyrics': this.lyrics, 'targetLang': 'ES'}).subscribe((res) => {
            console.log(res)
            Object.values(res).forEach((value) => {
                this.translation = value;
                console.log(this.translation);
            })
        })
    }


    // Load track audio
    reloadAudio(trackUrl:string){
        var audio = document.getElementById('audioPlayer') as HTMLAudioElement;
        console.log(trackUrl);
        audio.setAttribute('src', trackUrl);
        audio.load();
        // Check if another audio.load() here fixes need for double load
    }
}
