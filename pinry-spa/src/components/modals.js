import PinCreateModal from './pin_create/PinCreateModal.vue';
import LoginForm from './LoginForm.vue';
import SignUpForm from './SignUpForm.vue';
import BoardEdit from './BoardEdit.vue';


function openPinCreate(vm, onCreate) {
  vm.$buefy.modal.open(
    {
      parent: vm,
      component: PinCreateModal,
      hasModalCard: true,
      events: {
        'create.succeed': onCreate,
      },
    },
  );
}

function openBoardCreate(vm) {
  vm.$buefy.modal.open(
    {
      parent: vm,
      component: BoardEdit,
      hasModalCard: true,
    },
  );
}

function openLogin(vm, onSucceed) {
  vm.$buefy.modal.open({
    parent: vm,
    component: LoginForm,
    hasModalCard: true,
    events: {
      'login.succeed': onSucceed,
    },
  });
}

function openSignUp(vm, onSignUpSucceed) {
  vm.$buefy.modal.open({
    parent: vm,
    component: SignUpForm,
    hasModalCard: true,
    events: {
      'signup.succeed': onSignUpSucceed,
    },
  });
}

export default {
  openBoardCreate,
  openPinCreate,
  openLogin,
  openSignUp,
};
