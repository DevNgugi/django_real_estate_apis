
<template>
<div>
  <h1>Home Page</h1>
  <p>Welcome Back <span id="name"> {{ auth_user_name }} </span></p>
  <p>You are {{ usertype }} a Realtor</p>
  <button @click="logout">Logout</button>
  <button @click="
router.push({ name: 'signup'});

  ">signup</button>

</div>
</template>

<script setup lang="ts">
import { ref ,onMounted} from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { userStore } from '@/stores/user';
const user=userStore()

const usertype=ref('')
const router=useRouter()
const auth_user_name=ref()
const auth_user_is_realtor=ref()

onMounted(() => {


  auth_user_name.value = localStorage.getItem('name')
  auth_user_is_realtor.value = localStorage.getItem('is_realtor') == 'true' ? true:false
  usertype.value = auth_user_is_realtor.value?'':'not'


})

const logout=()=>{
  localStorage.clear () 

router.push({ name: 'login'});

}

</script>

<style scoped>
#name{
  @apply text-2xl font-bold
}
</style>