<template>
  <div id="app">
    <Header>asdfasdfs</Header>
    <div class="container">
      <alert></alert>
      <router-view/>
    </div>
  </div>
</template>

<script type="text/javascript">
import Header from '@/components/Header'
import Alert from '@/components/Alert'
export default {
  name: 'app',
  data () {
    return {}
  },
  components: {
    Alert,
    Header
  }
}
</script>
