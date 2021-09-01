import { Component, Injectable, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Store } from '@ngrx/store';
import { Observable, Subject } from 'rxjs';
import { Set } from 'src/app/redux/actions';
import { State } from 'src/app/redux/state';
import * as AppSelectors from '../../redux/selectors';
import Speech from 'speak-tts'

@Component({
  selector: 'app-audio',
  templateUrl: './audio.component.html',
  styleUrls: ['./audio.component.scss']
})
export class AudioComponent implements OnInit {
  @Input() mode = 'toggle';
  @Input() text;

  audioEnabled = false;
  constructor(store: Store<State>, private audioService: AudioService) {
    store.select(AppSelectors.selectAudioEnabled).subscribe(status => {
      this.audioEnabled = status;
    })
  }

  ngOnInit(): void {}

  toggleAudio() {
    if(this.audioEnabled == false){
      this.audioService.initAudio();
    }else{
      this.audioService.destroyAudio();
    }    
  }

  playAudio() {
    this.audioService.addToQueue(this.text);
  }
}

@Injectable({
  providedIn: 'root'
})
export class AudioService {
  audioEnabled = false;
  audioPlaying= false;
  private speechCtrl: any;
  private messageQueue= [];

  constructor(private store: Store<State>){
    store.select(AppSelectors.selectAudioEnabled).subscribe(status => {
      this.audioEnabled = status;

      if(status){
        this.initAudio();
      }else{
        this.destroyAudio();
      }
    });
  }

  initAudio() {
    try{
      this.speechCtrl = new Speech();
      if(this.speechCtrl.hasBrowserSupport()) { // returns a boolean
        console.log("speech synthesis supported")
        this.speechCtrl.init({
          'volume': 1,
          'lang': 'en-GB',
          'rate': 1,
          'pitch': 1,
          'splitSentences': true
        }).then((data) => {
            // The "data" object contains the list of available voices and the voice synthesis params
            console.log("Speech is ready, voices are available")
            this.changeAudioEnabledStatus(true)
        }).catch(e => {
            console.error("An error occured while initializing : ", e)
            this.changeAudioEnabledStatus(false)
        });        
      }else{
        // implement error notification if speech not supported
        this.changeAudioEnabledStatus(false);
      }
    }catch(error){
      this.changeAudioEnabledStatus(false);
      // implement error notification if speech not supported
      console.log("speech synthesis is not supported")
    }    
  }

  destroyAudio(){
    this.speechCtrl = null;
    this.changeAudioEnabledStatus(false);
  }

  changeAudioEnabledStatus(status: boolean){
    this.store.dispatch(new Set({
      state: 'audioEnabled',
      data: status
    }));
  }

  private textToSpeech(text) {
    if(this.audioEnabled){
      this.speechCtrl.speak({
        text: text,
        queue: false, // current speech will be interrupted,
        listeners: {
            onstart: () => {
              // change audio controls using css
              console.log("Start utterance");
              this.audioPlaying = true;
            },
            onend: () => {
              // change audio controls using css
              console.log("End utterance");
              this.audioPlaying = false;
              this.messageQueue.splice(0, 1);
              this.playTextFromQueue();
            },
            onresume: () => {
              // change audio controls using css
              console.log("Resume utterance")
            },
            onboundary: (event) => {
                console.log(event.name + ' boundary reached after ' + event.elapsedTime + ' milliseconds.')
            }
        }
      }).then(() => {
          console.log("Success !")
      }).catch(e => {
          console.error("An error occurred :", e)
      })
    }else{
      console.log('display error message to enable audio')
    }
    
  }

  pauseAudio(){
    this.speechCtrl.pause()
  }

  resumeAudio(){
    this.speechCtrl.resume()
  }

  cancelAudio(){
    this.speechCtrl.cancel()
  }

  addToQueue(text: string) {
    this.messageQueue.push(text);
    this.playTextFromQueue()
  }

  playTextFromQueue(){
    if(this.audioPlaying == false && this.messageQueue.length > 0){
      this.textToSpeech(this.messageQueue[0]);
    }
  }
}