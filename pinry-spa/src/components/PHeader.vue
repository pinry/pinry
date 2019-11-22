<template>
  <div class="p-header">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
          <a class="navbar-item" href="/">
            <img src="../assets/logo-dark.png" height="28">
          </a>
          <a role="button" class="navbar-burger burger"
             aria-label="menu" aria-expanded="false"
             data-target="PinryNav">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>
        <div id="PinryNav" class="navbar-menu">
          <div class="navbar-start">
            <a class="navbar-item">
              BookmarkLet
            </a>
            <a class="navbar-item">
              Create Pin
            </a>
            <div class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                Browser Extensions
              </a>
              <div class="navbar-dropdown">
                <a class="navbar-item">
                  Chrome
                </a>
                <a class="navbar-item">
                  Firefox
                </a>
              </div>
            </div>
          </div>
          <div class="navbar-end">
            <div class="navbar-item">
              <div class="buttons">
                <a class="button is-primary">
                  <strong>Sign up</strong>
                </a>
                <a class="button is-light">
                  Log in
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'p-header',
};
</script>

<style scoped>

</style>
