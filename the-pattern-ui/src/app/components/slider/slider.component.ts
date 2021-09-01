import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Options } from '@angular-slider/ngx-slider';
import { debounceTime, filter } from 'rxjs/operators';
import { Store } from '@ngrx/store';

import { State } from '../../redux/state';
import { Create } from 'src/app/redux/actions';
import * as AppSelectors from '../../redux/selectors';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.scss']
})
export class SliderComponent implements OnInit {
  form: FormGroup;
  years = []
  initYear = 2001;
  searchTerm = '';
  options: Options = {
    floor: this.initYear,
    ceil: this.initYear
  };

  get year() { return this.form.get('year') }

  constructor(fb: FormBuilder, private store: Store<State>) {
    this.form = fb.group({
      year: new FormControl(this.initYear)
    });
  }

  reset() {
    this.form.reset(this.initYear)
  }



  ngOnInit() {

    this.store.select<any>(AppSelectors.selectSearchYears)
      .pipe(filter(x => x!=null))
      .subscribe((results) => {
        this.changeSliderOptions(results)
      }
    );

    this.store.select<any>(AppSelectors.selectSearchTerm)
      .pipe(filter(x => x!=null))
      .subscribe((term) => {
        this.searchTerm = term
      }
    );
  }

  changeSliderOptions(years) {
    const newOptions: Options = Object.assign({}, this.options);
    if(years.list.length > 0){
      newOptions.stepsArray = years.list.map((year: string) => {
        return { value: year }
      });
    }
    
    newOptions.ceil = years.max || this.initYear
    newOptions.floor = years.min || this.initYear
    this.year.setValue(years.median)
    this.options = newOptions;
  }

  fetchFilteredData() {
    // dispatch redux action
    this.store.dispatch(new Create({
      data: { years: [this.year.value], search: this.searchTerm },
      state: 'searchResults',
      route: 'search'
    }));
  }

}
