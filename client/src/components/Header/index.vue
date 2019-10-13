<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <router-link class="navbar-brand" to="/">Client</router-link> 
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                     <router-link class="nav-link" to="/">Home</router-link> 
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/about">About</router-link> 
                </li>
                <li  v-if="!authenticated" class="nav-item">
                    <router-link class="nav-link" to="/register">Regsiter</router-link>
                </li>
            </ul>
            <form v-if="!authenticated" class="form-inline my-2 my-lg-0">
                <router-link class="btn btn-success my-2 my-sm-0" to="/login">Login</router-link> 
            </form>
            <form v-if="authenticated" class="form-inline my-2 my-lg-0">
                <button class="btn btn-info" @click="logout">
                    <span class="fas fa-sign-out-alt" aria-hidden="true"> LogOut </span>
                </button>
            </form>
        </div>
    </nav>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  data () {
    return {
    }
  },

  computed: {
    ...mapGetters([
      'user',
      'authenticated'
    ])
  },

  methods: {
    ...mapActions([
      'logout'
    ])
  }
}
</script>