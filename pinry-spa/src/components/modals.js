import PinCreateModal from './pin_edit/PinCreateModal.vue';
import LoginForm from './LoginForm.vue';
import SignUpForm from './SignUpForm.vue';
import BoardEdit from './BoardEdit.vue';
import Add2Board from './pin_edit/Add2Board.vue';


function openPinEdit(vm, props = null, onCreated = null) {
  vm.$buefy.modal.open(
    {
      component: PinCreateModal,
      props,
      hasModalCard: true,
      events: {
        pinCreated() {
          if (onCreated !== null) {
            onCreated();
          }
        },
      },
    },
  );
}

function openAdd2Board(vm, pin, username) {
  vm.$buefy.modal.open(
    {
      component: Add2Board,
      props: { pin, username },
      hasModalCard: true,
    },
  );
}

function openBoardCreate(vm) {
  vm.$buefy.modal.open(
    {
      component: BoardEdit,
      hasModalCard: true,
    },
  );
}

function openBoardEdit(vm, board, onSaved) {
  vm.$buefy.modal.open(
    {
      component: BoardEdit,
      props: {
        board,
        isEdit: true,
      },
      events: {
        boardSaved: onSaved,
      },
      hasModalCard: true,
    },
  );
}

function openLogin(vm, onSucceed) {
  vm.$buefy.modal.open({
    component: LoginForm,
    hasModalCard: true,
    events: {
      loginSucceed: onSucceed,
    },
  });
}

function openSignUp(vm, onSignUpSucceed) {
  vm.$buefy.modal.open({
    component: SignUpForm,
    hasModalCard: true,
    events: {
      signupSucceed: onSignUpSucceed,
    },
  });
}

export default {
  openBoardCreate,
  openBoardEdit,
  openAdd2Board,
  openPinEdit,
  openLogin,
  openSignUp,
};
