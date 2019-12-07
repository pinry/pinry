
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
  function markFieldsAsDanger(errorRespObject) {
    Object.entries(errorRespObject).forEach(
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
  function asData() {
    const data = {};
    Object.entries(form).forEach(
      (formField) => {
        const [name, value] = formField;
        data[name] = value.value;
      },
    );
    return data;
  }

  function asDataByFields(requiredFields) {
    const data = {};
    requiredFields.forEach(
      (fieldName) => {
        data[fieldName] = self[fieldName].value;
      },
    );
    return data;
  }

  function assignToForm(data) {
    Object.entries(data).forEach(
      (dataField) => {
        const [key, value] = dataField;
        if (key in self) {
          self[key].value = value;
        }
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
    form: self,
    fields,
    markFieldsAsDanger,
    markFieldAsDanger,
    resetField,
    asData,
    asDataByFields,
    assignToForm,
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
