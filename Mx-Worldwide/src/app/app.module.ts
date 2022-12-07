import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { appRoutingModule } from './app.routing';
import { AppComponent } from './app.component';
import { HomeComponent } from './home';
import { LoginComponent } from './login';


@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule,
    appRoutingModule,
    FormsModule
  ],
  declarations: [
      AppComponent,
      HomeComponent,
      LoginComponent,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { };
