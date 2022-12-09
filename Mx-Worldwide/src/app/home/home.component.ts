import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface USERS {
    musicName: string;
    artistName: string;
    lan: string;
}

@Component({ 
    templateUrl: 'home.component.html',
    styleUrls: ['home.component.css']
})
export class HomeComponent {

    readonly ROOT_URL = 'http://127.0.0.1:3052/';
    readonly ROOT_URL2 = 'http://127.0.0.1:5000/';

    constructor(private http: HttpClient) {}

    // Variable Definition
    songName: string='';
    artist: string='';
    trackURL: string='';
    lyrics: string='Lyrics go here';
    imageURL: string='https://developer.spotify.com/assets/branding-guidelines/icon4@2x.png';
    translation: string='Welcome to the Mx-Worldwide Lyrics Translator! Enter a song name, artist, preferred language, and enjoy!';
    language: string='EN';
    history!: USERS[];
    

    // Send APIs form data
    search(data:NgForm){
        this.songName = data.value.songName;
        this.artist = data.value.artist;
        console.log(this.songName);
        console.log(this.artist);
        this.language = (<HTMLSelectElement>document.getElementById('language')).value;
        console.log(this.language);
    
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
                if (value.includes('artist')) {
                    this.artist = value;
                    console.log(this.artist);
                }
                if (value.includes('songName')) {
                    this.songName = value;
                    console.log(this.songName);
                }
            });
        });

        // Extract API response for translated lyrics
        if (this.language != "EN") {
        this.http.post(this.ROOT_URL + 'api/translate', {'originalLyrics': this.lyrics, 'targetLang': this.language}).subscribe((res) => {
            console.log(res)
            Object.values(res).forEach((value) => {
                this.translation = value;
                console.log(this.translation);
            })
        })
        }

        // Extract user history
        this.http.get<USERS>(this.ROOT_URL + 'get_user_mh').subscribe((res) => {
            console.log(res)
            Object.values(res).forEach((value) => {
                this.history = value;
            })
        })

        

        this.http.post(this.ROOT_URL2 + 'create_music', {'musicname': this.songName, 'artist': this.artist, 
                                                        'language': this.language, 'lyrics': this.translation}).subscribe((res) => {
            console.log(res)
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
