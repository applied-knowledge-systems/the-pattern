import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {
  ICreate, ICreateSuccess,
  IRead, IReadSuccess,
  IUpdate, IUpdateSuccess,
  IDelete, IDeleteSuccess
} from '../redux/interfaces';
import { Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  baseUrl = environment.redisUrl;

  constructor(private http: HttpClient) { }

  create(payload: ICreate): Observable<ICreateSuccess>{
    const status = this.checkPayloadStatus(payload);
    return this.http.post<any>(this.baseUrl + '/' + payload.route, payload.data,{withCredentials: true }).pipe(map((data) => {
      const response : ICreateSuccess = {
        id: data._id,
        data: data,
        notify: status.notify,
        state: payload.state,
        navigate: status.navigate,
        navigateTo: payload.navigateTo,
        postProcess: payload.postProcess,
        postProcessStatus: status.postProcessStatus,
        message: payload.message
      }
      return response;
    }));
  }

  read(payload: IRead): Observable<IReadSuccess> {
    const status = this.checkPayloadStatus(payload);
    return this.http.get<any>(this.baseUrl + '/' + payload.route, { params: payload.query ,withCredentials: true }).pipe(map((data) => {
      const response: IReadSuccess = {
        data: data,
        state: payload.state,
        navigate: status.navigate,
        navigateTo: payload.navigateTo,
        postProcess: payload.postProcess,
        postProcessStatus: status.postProcessStatus
      }
      return response;
    }));
  }

  update(payload: IUpdate): Observable<IUpdateSuccess> {
    const status = this.checkPayloadStatus(payload);
    return this.http.put<any>(this.baseUrl + '/' + payload.route, payload.data).pipe(map((data)=> {
      const response: IUpdateSuccess = {
        data: data,
        state: payload.state,
        message: payload.message,
        notify: status.notify,
        navigate: status.navigate,
        navigateTo: payload.navigateTo
      }
      return response;
    }));
  }

  delete(payload: IDelete): Observable<IDeleteSuccess> {
    const status = this.checkPayloadStatus(payload);
    return this.http.delete<any>(this.baseUrl + '/' + payload.route)
            .pipe(map((data) => {
              const response: IDeleteSuccess = {
                notify: status.notify,
                message: payload.message,
                navigateTo: payload.navigateTo,
                navigate: status.navigate
              }
              return response;
            }));
  }

  checkPayloadStatus(payload){
    let result = {
      notify: false,
      navigate: false,
      postProcessStatus: false
    }

    if(payload.navigateTo !== undefined){
      result.navigate = true;
    }

    if(payload.message !== undefined){
      result.notify = true;
    }

    if(payload.postProcess !== undefined){
      result.postProcessStatus = true;
    }

    return result;
  }
}


