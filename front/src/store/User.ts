import { makeAutoObservable } from "mobx";
import { makePersistable } from "mobx-persist-store";


interface IUser {
    isAuth: boolean;
    access: string;
    refresh: string;
}

class User {
    data: IUser = {
        isAuth: false,
        access: '',
        refresh: '' 
    }

    constructor() {
        makeAutoObservable(this)
    
        makePersistable(this, {name: 'asT', properties: ['data'], storage: window.localStorage})
    }

    setAsses(token: string){
        this.data.access = token;
    }

    setRef(token: string){
        this.data.refresh = token;
    }

    setAuth(flag: boolean) {
        this.data.isAuth = flag 
    }

}


// eslint-disable-next-line import/no-anonymous-default-export
export default new User()