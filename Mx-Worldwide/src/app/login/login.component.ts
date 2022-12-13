import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({ templateUrl: 'login.component.html' })
export class LoginComponent {
    readonly ROOT_URL = 'http://127.0.0.1:3052/';

    constructor(private http: HttpClient) {
        window.onload = this.check();
    }
    
    data : any;
    btn : any;
    signIn()
    {
        this.http.get(this.ROOT_URL + 'oauth/signin').subscribe(data => {
            this.data = data as JSON;
            if (this.data != undefined)
            {
                window.location.href = this.data['link'];
            }
        });
        console.log(this.data);
    }

    check()
    {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        console.log(urlParams.get('oauth_token'));
        console.log(urlParams.get('oauth_verifier'));
        if(urlParams.get('oauth_verifier') != null)
        {
            this.http.post(this.ROOT_URL + 'oauth/signin2', {'oauth_token': urlParams.get('oauth_token'), 'oauth_verifier': urlParams.get('oauth_verifier')}).subscribe(data => {
                this.data = data as JSON;
                if(this.data['status'] == "Ok")
                {
                    this.btn = document.getElementById('signIn');
                    if (this.btn != null)
                    {
                        this.btn.textContent = 'You are signed in';
                    }
                }
            });
        }
        return null;
    }
}
