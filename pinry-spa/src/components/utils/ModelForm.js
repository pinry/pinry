
function createFormModel(fields) {
  const form = {};
  fields.forEach(
    (fieldName) => {
      form[fieldName] = {
        value: null,
        error: null,
        type: null,
      };
    },
  );
  return form;
}


function FormHelper(form, fields = []) {
  const self = form;
  function resetField(fieldName) {
    self[fieldName].type = 'is-info';
    self[fieldName].error = null;
  }
  function markFieldAsDanger(fieldName, errorMsg) {
    self[fieldName].error = errorMsg;
    self[fieldName].type = 'is-danger';
  }
  function markFieldsAsDanger(errorRespObjecct) {
    Object.entries(errorRespObjecct).forEach(
      (errorTuple) => {
        const [key, error] = errorTuple;
        let msg;
        if (Array.isArray(error)) {
          [msg] = error;
        } else {
          msg = error;
        }
        markFieldAsDanger(key, msg);
      },
    );
  }
  function resetAllFields() {
    fields.forEach(
      (fieldName) => {
        resetField(fieldName);
      },
    );
  }
  return {
    form,
    fields,
    markFieldsAsDanger,
    markFieldAsDanger,
    resetField,
    resetAllFields,
  };
}

function fromFields(fields) {
  const form = createFormModel(fields);
  return FormHelper(form, fields);
}

export default {
  createFormModel,
  FormHelper,
  fromFields,
};
