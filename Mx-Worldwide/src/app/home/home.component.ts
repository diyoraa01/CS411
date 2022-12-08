import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {

    readonly ROOT_URL = 'http://127.0.0.1:3052/';

    constructor(private http: HttpClient) {}

    songName: string='';
    artist: string='';
    trackURL: string='';
    lyrics: string='Lyrics go here';
    imageURL: string='';
    translation: string='Translation goes here';

    search(data:NgForm){
        this.songName = data.value.songName;
        this.artist = data.value.artist;
        console.log(this.songName);
        console.log(this.artist);
    
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
    
        this.http.post(this.ROOT_URL + 'api/lyrics', {'artist': this.artist, 'songName': this.songName}).subscribe((res) => {
            console.log(res)
            Object.values(res).forEach((value) => {
                if (value.includes('Lyrics')) {
                    this.lyrics = value;
                    console.log(this.lyrics);
                }
            });
        });

        this.http.post(this.ROOT_URL + 'api/translate', {'originalLyrics': this.lyrics, 'targetLang': 'ES'}).subscribe((res) => {
            console.log(res)
            Object.values(res).forEach((value) => {
                this.translation = value;
                console.log(this.translation);
            })
        })
    }


    // Needs to be fixed so that two form submissions aren't needed for the player to be updated
    reloadAudio(trackUrl:string){
        var audio = document.getElementById('audioPlayer') as HTMLAudioElement;
        console.log(trackUrl);
        audio.setAttribute('src', trackUrl);
        audio.load();
    }
}
