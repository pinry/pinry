<template>
  <div class="signup-modal">
    <div>
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Sign Up</p>
        </header>
        <section class="modal-card-body">
          <b-field label="Username"
                   :type="form.username.type"
                   :message="form.username.error">
            <b-input
              type="string"
              v-model="form.username.value"
              placeholder="Your Username"
              maxlength="30"
              required>
            </b-input>
          </b-field>

          <b-field label="Email"
                   :type="form.email.type"
                   :message="form.email.error">
            <b-input
              type="email"
              v-model="form.email.value"
              password-reveal
              placeholder="Your email"
              required>
            </b-input>
          </b-field>
          <b-field label="Password"
                   :type="form.password.type"
                   :message="form.password.error">
            <b-input
              type="password"
              v-model="form.password.value"
              password-reveal
              placeholder="Your password"
              required>
            </b-input>
          </b-field>
          <b-field label="Password repeat"
                   :type="form.password_repeat.type"
                   :message="form.password_repeat.error">
            <b-input
              type="password"
              v-model="form.password_repeat.value"
              password-reveal
              placeholder="Your password again"
              required>
            </b-input>
          </b-field>
        </section>
        <footer class="modal-card-foot">
          <button class="button" type="button" @click="$parent.close()">Close</button>
          <button
            @click="doRegister"
            class="button is-primary">Register</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import api from './api';
import ModelForm from './utils/ModelForm';

const fields = [
  'username',
  'email',
  'password',
  'password_repeat',
];

export default {
  name: 'SignUpForm',
  data() {
    const model = ModelForm.fromFields(fields);
    return {
      form: model.form,
      helper: model,
    };
  },
  methods: {
    doRegister() {
      this.helper.resetAllFields();
      const self = this;
      const promise = api.User.signUp(
        self.form.username.value,
        self.form.email.value,
        self.form.password.value,
        self.form.password_repeat.value,
      );
      promise.then(
        (user) => {
          self.$emit('signup.succeed', user);
          self.$parent.close();
        },
        (resp) => {
          self.helper.markFieldsAsDanger(resp.data);
        },
      );
    },
  },
};
</script>
