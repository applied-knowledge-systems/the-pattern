import { Inject, Injectable } from '@angular/core';
import {webSocket, WebSocketSubject} from 'rxjs/webSocket';
import { environment } from 'src/environments/environment';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { LOCAL_STORAGE, StorageService } from 'ngx-webstorage-service';

const STORAGE_KEY = 'local_graph';
@Injectable()
export class LocalStorageService {

     constructor(@Inject(LOCAL_STORAGE) private storage: StorageService) { }
     public storeOnLocalStorage(nodeID: string): void {

          // get array of nodes from local storage
          const currentNodeList = this.storage.get(STORAGE_KEY) || [];
          // push new node to array
          currentNodeList.push({
              id: nodeID,
              marked: true
          });
          // insert updated array to local storage
          this.storage.set(STORAGE_KEY, currentNodeList);
          console.log("Local Storage:")
          console.log(this.storage.get(STORAGE_KEY) || 'LocaL storage is empty');
     }
}

interface ISearchResult{
  links: any[];
  nodes: any[];
}

@Injectable({
  providedIn: 'root'
})
export class AppService {

  // searchSocket: WebSocketSubject<any> = webSocket(environment.redisUrl + '/search');
  // graphSocket: WebSocketSubject<any> = webSocket(environment.redisUrl + '/graph');



  graphData$: Observable<any>;
  searchData$: Observable<any>;

  constructor(private http: HttpClient) {
    // this.searchData$ = this.searchSocket.asObservable();
    // this.searchSocket.asObservable().subscribe(dataFromServer => {
    //   console.log('search data')
    //   console.log(dataFromServer)
    // });

    // this.graphData$ = this.graphSocket.asObservable();
    // this.graphData$.subscribe(dataFromServer => {
    //   console.log('graph data')
    //   console.log(dataFromServer)
    // })
  }

  // search(search){
  //   this.searchSocket.next({message: search});
  // }

  // fetchGraph(data){
  //   this.graphSocket.next({ data: data })
  // }

  searchApi(text: string): Observable<ISearchResult>{
    const searchUri = environment.redisUrl+'/search'
    return this.http.post<any>(searchUri, { search: text, withCredentials: true },).pipe(map((data) => {
      console.log(data)
      return data.search_result;
    }));
  }

  QAsearchApi(text: string): Observable<ISearchResult>{
    const searchUri = environment.redisUrl+'/qasearch'
    return this.http.post<any>(searchUri, { search: text }).pipe(map((data) => {
      console.log(data)
      return data.search_result;
    }));
  }

  edgeApi(source: string, target: string): Observable<any>{
    const edgeUri= environment.redisUrl+`/edge/edges:${source}:${target}`
    return this.http.get<any>(edgeUri,{withCredentials: true }).pipe(map((data) => {
      return data.results;
    }));
  }
  excludeNode(nodeID: string): Observable<any>{
    const excludeUri= environment.redisUrl+`/exclude?id=${nodeID}`
    console.log(excludeUri)
    return this.http.get<any>(excludeUri,{withCredentials: true }).pipe(map((data) => {
      console.log(data)
      return data.results;
    }));
  }
}
