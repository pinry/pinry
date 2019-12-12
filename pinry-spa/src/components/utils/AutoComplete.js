function getFilteredOptions(options, filterText) {
  return options.filter(
    (option) => {
      const index = option.name
        .toString()
        .toLowerCase()
        .indexOf(filterText.toLowerCase());
      return index >= 0;
    },
  );
}

export default {
  getFilteredOptions,
};
