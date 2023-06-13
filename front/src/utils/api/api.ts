import axios from "axios";


export const $api = axios.create({
    baseURL: process.env.REACT_APP_BASE_URL,
    withCredentials: true,
})


$api.interceptors.request.use(config => {
    config.headers.Authorization = `JWT ${localStorage.getItem('token')}`
    return config

})



$api.interceptors.response.use(config => {
    return config
}, (async(error) => {
    const originalRequest = error.config

    if (originalRequest && !originalRequest._isRetry && error.response.status === 401)
    {
        originalRequest._isRetry = true
        try {
            const response = await axios.post(`${process.env.REACT_APP_BASE_URL}auth/jwt/refresh/`, {refresh: getCookie('token')})
            localStorage.setItem('token', response.data.access)
            return $api.request(originalRequest)
        }catch(error) {
            console.log(error)
        }
        window.location.href = '/';
    }
    
    throw error
    
}))


export default function getCookie(name: string) {
  let matches = document.cookie.match(new RegExp(
    // eslint-disable-next-line no-useless-escape
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}