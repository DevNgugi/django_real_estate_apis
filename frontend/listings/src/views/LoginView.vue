<template>
<section class="bg-gray-50 ">
  <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <!-- <a href="#" class="flex items-center mb-6 text-2xl font-semibold text-gray-900 ">
          <img class="w-8 h-8 mr-2" src="https://www.svgrepo.com/show/455502/sold-house.svg" >
        Twin Brooke Estate 
      </a> -->
      <div class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
          <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 class="text-xl font-bold leading-tight text-center tracking-tight text-gray-900 md:text-2xl ">
                 Login to NList
              </h1>
              <form class="space-y-4 md:space-y-6" action="#" @submit.prevent="submit">
                  <div>
                      <label for="email" class="block mb-2 text-sm font-medium text-gray-900">Your email</label>
                      <input v-model="data.email" type="email" name="email" id="email" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5" placeholder="name@company.com" >
                  </div>
                  <div>
                      <label for="password" class="block mb-2 text-sm font-medium text-gray-900 ">Password</label>
                      <input v-model="data.password" type="password" name="password" id="password" placeholder="••••••••" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5" >
                  </div>
                  <button type="submit" class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">Sign In</button>
                  <p class="text-sm font-light text-gray-500">
                      No Account?
                      <router-link class="font-medium text-primary-600 hover:underline" :to="{ name: 'signup'}">Signup here</router-link>
                       
                  </p>
              </form>
          </div>
      </div>

  </div>
</section>
</template>

<script setup lang="ts">
import { ref ,reactive, onMounted} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { userStore } from '@/stores/user';
const route=useRoute()
import {toast} from 'vue3-toastify';
const user=userStore()
const router = useRouter();

const data=reactive({
    email:route.query.email,
    password:''
})
import axios from 'axios'

onMounted(()=>{

    if (localStorage.getItem('access_token')){
            router.push({ name: 'home'});
        }
})


const submit=async ()=>{
    try{    
       

        const response = await axios.post("http://localhost:8000/api/token/auth/", data);
        if(response.data.access){
            localStorage.setItem("access_token", response.data.access)
            localStorage.setItem("refresh_token", response.data.refresh)

        

        const authUser = await axios.get('http://localhost:8000/auth/user/get/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
            });

            localStorage.setItem("name", authUser.data.user.name)
            localStorage.setItem("is_realtor",authUser.data.user.is_realtor )

            await router.push({ name: 'home'});
        }
        
    }
    catch(error:any){

        console.log(error.response.data);
        
        if (error.response.data.password){
            toast.error(error.response.data.password, {
                autoClose: 3000,
            }); 
        }
        else if (error.response.data.detail)
        {
            toast.error(error.response.data.detail, {
                autoClose: 3000,
            }); 
        }
    }
 
    
}

</script>
