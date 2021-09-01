import { Action } from '@ngrx/store';
import { ICreate, ICreateSuccess, ICreateFailure, IRead, IReadSuccess, IReadFailure, IUpdate, IUpdateSuccess, IUpdateFailure, IDelete, IDeleteSuccess, IDeleteFailure, IAuth, IAuthSuccess, IAuthFailure, ISignupSuccess, ISignup, ISignupFailure } from './interfaces';

export interface AuthAction<T> extends Action {
    type: string;
    payload: T;
}

export const REFRESH = '[APP] REFRESH';
export const SET = '[APP] SET';

export const CREATE = '[APP] CREATE';
export const CREATE_SUCCESS = '[APP] CREATE_SUCCESS';
export const CREATE_FAILURE = '[APP] CREATE_FAILURE';

export const UPDATE = '[APP] UPDATE';
export const UPDATE_SUCCESS = '[APP] UPDATE_SUCCESS';
export const UPDATE_FAILURE = '[APP] UPDATE_FAILURE';

export const READ = '[APP] READ';
export const READ_SUCCESS = '[APP] READ_SUCCESS';
export const READ_FAILURE = '[APP] READ_FAILURE';

export const DELETE = '[APP] DELETE';
export const DELETE_SUCCESS = '[APP] DELETE_SUCCESS';
export const DELETE_FAILURE = '[APP] DELETE_FAILURE';

export class Refresh implements AuthAction<any> {
    type = REFRESH;
    payload: any = null;

    constructor(data: any) {
        this.payload = data;
    }
}

export class Set implements AuthAction<any> {
    type = SET;
    payload: any = null;

    constructor(data: any) {
        this.payload = data;
    }
}

export class Create implements AuthAction<ICreate> {
    type = CREATE;
    payload: ICreate = null;

    constructor(data: ICreate) {
        this.payload = data;
    }
}

export class CreateSuccess implements AuthAction<ICreateSuccess> {
    type = CREATE_SUCCESS;
    payload: ICreateSuccess = null;

    constructor(data: ICreateSuccess) {
        this.payload = data;
    }
}

export class CreateFailure implements AuthAction<ICreateFailure> {
    type = CREATE_FAILURE;
    payload = null;

    constructor(data: ICreateFailure) {
        this.payload = data;
    }
}

export class Read implements AuthAction<IRead> {
    type = READ;
    payload: IRead = null;

    constructor(data: IRead) {
        this.payload = data;
    }
}

export class ReadSuccess implements AuthAction<IReadSuccess> {
    type = READ_SUCCESS;
    payload: IReadSuccess = null;

    constructor(data: IReadSuccess) {
        this.payload = data;
    }
}

export class ReadFailure implements AuthAction<IReadFailure> {
    type = READ_FAILURE;
    payload = null;

    constructor(data: IReadFailure) {
        this.payload = data;
    }
}

export class Update implements AuthAction<IUpdate> {
    type = UPDATE;
    payload: IUpdate = null;

    constructor(data: IUpdate) {
        this.payload = data;
    }
}

export class UpdateSuccess implements AuthAction<IUpdateSuccess> {
    type = UPDATE_SUCCESS;
    payload: IUpdateSuccess = null;

    constructor(data: IUpdateSuccess) {
        this.payload = data;
    }
}

export class UpdateFailure implements AuthAction<IUpdateFailure> {
    type = UPDATE_FAILURE;
    payload = null;

    constructor(data: IUpdateFailure) {
        this.payload = data;
    }
}

export class Delete implements AuthAction<IDelete> {
    type = DELETE;
    payload: IDelete = null;

    constructor(data: IDelete) {
        this.payload = data;
    }
}

export class DeleteSuccess implements AuthAction<IDeleteSuccess> {
    type = DELETE_SUCCESS;
    payload: IDeleteSuccess = null;

    constructor(data: IDeleteSuccess) {
        this.payload = data;
    }
}

export class DeleteFailure implements AuthAction<IDeleteFailure> {
    type = DELETE_FAILURE;
    payload = null;

    constructor(data: IDeleteFailure) {
        this.payload = data;
    }
}

export type Actions =
    Refresh
    | Set
    | Create
    | CreateSuccess
    | CreateFailure
    | Read
    | ReadSuccess
    | ReadFailure
    | Update
    | UpdateSuccess
    | UpdateFailure
    | Delete
    | DeleteSuccess
    | DeleteFailure;

