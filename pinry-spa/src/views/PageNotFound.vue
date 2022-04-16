<template>
  <div>
    <PHeader></PHeader>
    <div id="main">
      <div class="fof">
        <p>{{ $t("pageNotFound") }}</p>
        <h1>{{ $t("error404") }}</h1>
      </div>
    </div>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';

export default {
  name: 'PageNotFound',
  components: {
    PHeader,
  },
};
</script>

<style scoped>
*{
    transition: all 0.6s;
}
body{
    font-family: 'Lato', sans-serif;
    color: #888;
    margin: 0;
}
#main{
    display: table;
    width: 100%;
    height: 100vh;
    text-align: center;
}
.fof{
  display: table-cell;
  vertical-align: middle;
}
.fof h1{
  font-size: 50px;
  display: inline-block;
  padding-right: 12px;
  animation: type .5s alternate infinite;
}
@keyframes type{
  from{box-shadow: inset -3px 0px 0px #888;}
  to{box-shadow: inset -3px 0px 0px transparent;}
}
</style>
