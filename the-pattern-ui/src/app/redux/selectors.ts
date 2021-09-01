import { createSelector } from '@ngrx/store';

import { AppState, State } from './state';
// selectors
export const selectAppState = (state: State) => state.app;

export const selectSearchResults = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.searchResults;
    });

export const selectEdgeResults = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.edgeResults;
    });

export const selectQAResults = createSelector(
  selectAppState,
  (state: AppState) => {
      return state.answerResults;
  });

export const selectIsLoading = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.isLoading;
    });

export const selectIsLoadingState = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.isLoadingState;
    });

export const selectError = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.error;
    });

export const selectNodeResults = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.nodeResults;
    });

export const selectedEvent = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.selected;
    });

export const selectedNode = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.selectedNode;
    });

export const selectUX = createSelector(
    selectAppState,
    (state: AppState) => {
        return {
            toolBarStyle: state.toolBarStyle,
            mobile: state.mobile,
        };
    });

export const selectSearchTerm = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.searchTerm
    });

export const selectSearchYears = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.searchYears
    });

export const selectAudioEnabled = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.audioEnabled
    });

export const selectAnswerResults = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.answerResults
    });
    
export const selectActiveRole = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.activeRole
    });
    

    

