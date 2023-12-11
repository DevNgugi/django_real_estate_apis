import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'
let refresh=false;
const data = localStorage.getItem('refresh_token')
axios.interceptors.response.use(resp => resp, async error => {
    console.log(error.response.status)
    if (error.response.status == 401 && !refresh) {
        refresh = true
        const response = await axios.post('/api/token/refresh/', {
            refresh: data
        })
         
        if (response.status === 200) {
            const token = localStorage.setItem('access_token', response.data.access)
           
            axios.defaults.headers.common.Authorization = `Bearer ${token}`;
            
        }
    }
    return error;
})