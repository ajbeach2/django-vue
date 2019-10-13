<template>
  <transition>
    <div class='alert-container'>
      <div v-for="alert in alerts" 
           class="animated alert alert-dismissible" 
           v-bind:class="alert.type" 
           role="alert">
          <button @click="dismiss(alert)"type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span class="glyphicon glyphicon glyphicon-remove" aria-hidden="true"></span>
          </button>
          <span id="alert-message">
            <strong id="alert-title">{{alert.title}}</strong> {{alert.message}}
          </span>
        </div>
    </div>
  </transition>
</template>

<script type="text/javascript">
import { mapGetters, mapActions } from 'vuex'
export default {
  computed: mapGetters({
    alerts: 'alerts'
  }),

  methods: {
    ...mapActions([
      'hideAlert'
    ]),
    dismiss (e) {
      this.hideAlert(e)
    }
  }
}
</script>

<style>
.alert-container{
  position: fixed;
  z-index: 999;
  right:20px;
}
.alert{
  position:relative;
}
</style>