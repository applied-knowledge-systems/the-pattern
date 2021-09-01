import * as allActions from './actions';
import * as _ from 'lodash';
import { ActionReducerMap } from '@ngrx/store';
import { initialState, AppState, State } from './state';

export function appReducer(state = initialState, action: allActions.Actions): AppState {

    let stateChange = null;
    switch (action.type) {
        
        case allActions.REFRESH:
            if (action.payload.state !== undefined) {
                stateChange = {};
                stateChange[action.payload.state] = action.payload.data;
                return Object.assign({}, state, stateChange);
            } else {
                return Object.assign({}, state, state);
            }
        
        case allActions.CREATE:
            return Object.assign({}, state, { isLoading: true, isLoadingState: action.payload.state });
        
        case allActions.CREATE_SUCCESS:
            if (action.payload.state !== undefined) {
                stateChange = { isLoading: false, isLoadingState: '' };
                stateChange[action.payload.state] = action.payload.data;
                return Object.assign({}, state, stateChange);
            } else {
                return Object.assign({}, state, state);
            }
        
        case allActions.CREATE_FAILURE:
            return Object.assign({}, state, { isLoading: false, isLoadingState: '', error: action.payload.data });
        
        case allActions.READ:
            return Object.assign({}, state, { isLoading: true, isLoadingState: action.payload.state });
        
        case allActions.READ_SUCCESS:
            if (action.payload.state !== undefined) {
                stateChange = { isLoading: false, isLoadingState: '' };
                stateChange[action.payload.state] = action.payload.data;
                return Object.assign({}, state, stateChange);
            } else {
                return Object.assign({}, state, state);
            }
        
        case allActions.READ_FAILURE:
            return Object.assign({}, state, { isLoading: false, isLoadingState: '', error: action.payload.data });
        
        case allActions.UPDATE:
            return Object.assign({}, state, { isLoading: true, isLoadingState: action.payload.state });
        
        case allActions.UPDATE_SUCCESS:
            if (action.payload.state !== undefined) {
                stateChange = { isLoading: false, isLoadingState: '' };
                stateChange[action.payload.state] = action.payload.data;
                return Object.assign({}, state, stateChange);
            } else {
                return Object.assign({}, state, state);
            }
        
        case allActions.UPDATE_FAILURE:
            return Object.assign({}, state, { isLoading: false, isLoadingState: '', error: action.payload.data });
        
        case allActions.DELETE:
            return Object.assign({}, state, { isLoading: true, isLoadingState: action.payload.state });
        
        case allActions.DELETE_SUCCESS:
            if (action.payload.state !== undefined) {
                stateChange = { isLoading: false, isLoadingState: '' };
                stateChange[action.payload.state] = action.payload.data;
                return Object.assign({}, state, stateChange);
            } else {
                return Object.assign({}, state, state);
            }
        
        case allActions.DELETE_FAILURE:
            return Object.assign({}, state, { isLoading: false, isLoadingState: '', error: action.payload.data });
        
        
        case allActions.SET:
            if (action.payload.state !== undefined) {
                stateChange = {}
                stateChange[action.payload.state] = action.payload.data;
                return Object.assign({}, state, stateChange);
            } else {
                return Object.assign({}, state, state);
            }
        default:
            return Object.assign({}, state, state);
    }
}

export const reducers: ActionReducerMap<State> = {
    app: appReducer
};