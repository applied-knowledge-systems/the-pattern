export interface ICreate {
    id?: string;
    data: any;
    collection?: string;
    route?: string;
    state?: string;
    message?: string;
    postProcess?: string;
    navigateTo?: {
        route: string,
        query?: any
    };
}

export interface ICreateSuccess {
    id: string;
    data: any;
    notify?: boolean;
    state?: string;
    navigate?: boolean;
    message?: string;
    navigateTo?: {
        route: string,
        query?: any
    };
    postProcess?: string,
    postProcessStatus?: boolean
}

export interface ICreateFailure {
    data: any;
    message?: string;
}

export interface IRead {
    route?: string;
    query?: any;
    state?: string;
    navigateTo?: {
        route: string,
        query?: any
    };
    postProcess?: string;
}

export interface IReadSuccess {
    route?: string;
    data: any;
    query?: any;
    state?: string;
    navigate?: boolean;
    navigateTo?: {
        route: string,
        query?: any
    };
    postProcess?: string;
    postProcessStatus?: boolean
}

export interface IReadFailure {
    collection?: string;
    route?: string;
    query?: any;
    message?: string;
}

export interface IUpdate {
    route?: string;
    collection?: string;
    data: any;
    navigateTo?: {
        route: string,
        query?: any
    };
    state?: string;
    message?: string;
}

export interface IUpdateSuccess {
    data: any;
    state?: string;
    message?: string;
    notify?: boolean;
    navigate?: boolean;
    navigateTo?: {
        route: string,
        query?: any
    };
}

export interface IUpdateFailure {
    collection?: string;
    route?: string;
    query?: any;
    data?: any;
    message?: string;
}

export interface IDelete {
    route?: string;
    message?: string;
    navigateTo?: {
        route: string,
        query?: any
    };
}

export interface IDeleteSuccess {
    data?: any;
    notify?: boolean;
    navigate?: boolean;
    message?: string;
    navigateTo?: {
        route: string,
        query?: any
    };
}

export interface IDeleteFailure {
    collection?: string;
    route?: string;
    query?: any;
    data?: any;
    message?: string;
}


export interface IAuth {
    email: string;
    password: string;
    rememberMe?: boolean;
    navigateTo?: {
        route: string,
        query?: any
    };
    state?: string;
}

export interface IAuthSuccess {
    data: {
        _id: string;
        token: string;
        email: string;
        profile: any;
        teams: any[];
        verified: boolean;
    },
    navigate?: boolean;
    navigateTo?: {
        route: string,
        query?: any
    };
    state?: string;
}

export interface IAuthFailure {
    message: string;
}

export interface ISignup {
    name?: string;
    email: string;
    password: string;
    package?: any;
    role: string;
    navigateTo?: {
        route: string,
        query?: any
    };
}

export interface ISignupSuccess {
    _id: string;
    token: string;
    navigate: boolean;
    navigateTo?: {
        route: string,
        query?: any
    };
}

export interface ISignupFailure {
    message: string;
}

