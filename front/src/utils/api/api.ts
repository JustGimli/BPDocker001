import axios from "axios";
import User from "../../store/User";

export const $api = axios.create({
    baseURL: process.env.REACT_APP_BASE_URL
})

export const $auth = axios.create({
    baseURL: process.env.REACT_APP_BASE_URL
})

$api.interceptors.request.use(config => {
    config.headers.Authorization = `JWT ${User.data.access}`
    return config

})



$api.interceptors.response.use(config => {
    return config
}, (error => {

    if (error.response.status === 401) {
        $api.post('auth/jwt/refresh/', {refresh: User.data.refresh}).then(resp => {
            if(resp.data.refresh  && resp.data.access){
                User.setAsses(resp.data.access)
                User.setRef(resp.data.refresh)
                return $api.request(error.config)
            }else {
                User.setAuth(false)
            }
        }).catch((error) =>  {
            User.setAuth(false)
        })
    }else if (error.response.status === 400) {
        User.setAuth(false)
    }
    
}))