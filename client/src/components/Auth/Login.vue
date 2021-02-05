<template>
    <div class="row justify-content-center">
        <div class="col-md-6">
          {{ error.login }}
            <div v-if="error.length > 0" class="alert alert-danger" role="alert">
                {{ error.login }}
            </div>
            <span class="anchor" id="formLogin"></span>
            <div class="card card-outline-secondary">
                <div class="card-header">
                    <h3 class="mb-0">Login</h3>
                </div>
                <div class="card-body">
                    <form @submit.prevent >
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input v-bind:class="{ 'is-invalid': error.login }" v-model.trim="username" id="username" name="username" type="text" placeholder="" class="form-control input-md" required>
                        </div>
                            <div class="form-group">
                            <label for="password">Passowrd</label>
                            <input v-bind:class="{ 'is-invalid': error.login }" v-model.trim="password" id="password" name="password" type="password" placeholder="" class="form-control input-md" required>
                        </div>
                        <button @click="submit" class="btn btn-success btn-lg float-right" type="submit">Login</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
<script type="text/javascript">
import { mapActions, mapGetters } from 'vuex'
export default {
  data () {
    return {
      username: null,
      password: null
    }
  },
  computed: {
    ...mapGetters([
      'error'
    ])
  },
  methods: {
    ...mapActions([
      'login',
      'me'
    ]),
    submit () {
      let data = {
        username: this.username,
        password: this.password
      }
      this.login(data)
    }
  }
}
</script>
