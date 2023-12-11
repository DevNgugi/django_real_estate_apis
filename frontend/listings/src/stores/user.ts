import { defineStore } from 'pinia';

export const userStore = defineStore('user', {
  state: () => ({
        name:'',
        is_realtor:'',
       
  }),
  
  getters: {
    getUser: (state) => () => {
    },
  },
  

  actions: {
    setUser(name:string,is_realtor:boolean) {
 
    },
   
   
  },
});
