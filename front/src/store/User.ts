import axios from "axios";
import { makeAutoObservable } from "mobx";
import getCookie, { $api } from "../utils/api/api";



interface IUser {
    id: number;
    email: string;
}

export default class User {
    user = {} as IUser
    isAuth: boolean = false
    isLoading: boolean = false  
    emailError: string = ''
    passwordError: string = ''
    detail: string = ''

    constructor() {
        makeAutoObservable(this)
    }

    setAuth(bool: boolean): void {
        this.isAuth = bool
    }

    setLoading(bool: boolean) {
        this.isLoading = bool
    }

    setUser(user: IUser) {
        this.user = user
    }

    setDetail(detail: string) {
        this.detail = detail
    }

    setPassError(error: string ){
        this.passwordError = error
    }


    setEmailError(error: string ) {
        this.emailError = error
    }


    async login(email: string, password: string) {
        try {
            const response = await axios.post(`${process.env.REACT_APP_BASE_URL}auth/users/`, {email, password})
            this.setUser(response.data)

            await this._getJWT(email, password)

        }catch(error: any){
            if (error.response?.data?.email) {
                
                if ("user with this email already exists." === error.response?.data?.email[0]) {
                    await this._getJWT(email, password)
                }else {
                    this.setEmailError(error.response?.data?.email[0])
                }
            }

            if (error.response?.data?.password) {
                this.setPassError(error.response?.data?.password[0])
            }
        }

    }
    
    async _getJWT(email: string, password: string) {
        try{
            const response = await axios.post(`${process.env.REACT_APP_BASE_URL}auth/jwt/create/`,  {email, password}, {withCredentials: true})
            localStorage.setItem('token', response.data.access)
            
            let date = new Date()
            document.cookie = `token=${response.data.refresh}; path=/;expires=${date.setTime(date.getTime() + 60 * 60 * 24 )}`
            this.setAuth(true)                
        }catch(error: any){ 
            this.setDetail(error.response.data?.detail)
        }   
    }

    async logout() {    
        localStorage.removeItem('token')
        document.cookie = `token=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/;`
        this.setAuth(false)
        this.setUser({} as IUser)
    }

    async checkAuth() {
        this.setLoading(true)
        try {
            const response = await $api.post(`auth/jwt/verify`, {"token": localStorage.getItem('token')})
        }catch (error) {
            if (getCookie("token")) {
                console.log("refresh")
            }
            console.log(error)
        }

        this.setLoading(false)
    }


}



