<template>
  <div class="add2board-modal">
    <div>
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Add Pin to Board</p>
        </header>
        <section class="modal-card-body">
          <div class="columns">
            <div class="column">
              <FileUpload
                :previewImageURL="pin.url"
              ></FileUpload>
            </div>
            <div class="column">
              <FilterSelect
                :allOptions="boardOptions"
                v-on:selected="onSelectBoard"
              ></FilterSelect>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button" type="button" @click="$parent.close()">Close</button>
          <button
            @click="doAdd2Board"
            class="button is-primary">Add Pin to Board
          </button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import API from '../api';
import FileUpload from './FileUpload.vue';
import FilterSelect from './FilterSelect.vue';


export default {
  name: 'Add2Board',
  props: ['pin', 'username'],
  components: {
    FileUpload,
    FilterSelect,
  },
  data() {
    return {
      boardOptions: [],
      boardIds: [],
    };
  },
  created() {
    this.fetchBoardList();
  },
  methods: {
    doAdd2Board() {
      if (this.boardIds.length > 0) {
        const promises = [];
        this.boardIds.forEach(
          (boardId) => {
            promises.push(
              API.Board.addToBoard(boardId, [this.pin.id]),
            );
          },
        );
        Promise.all(promises).then(
          () => {
            this.$buefy.toast.open('Succeed to add pin to boards');
            this.$parent.close();
          },
          () => {
            this.$buefy.toast.open(
              {
                message: 'Failed to add pin to boards',
                type: 'is-danger',
              },
            );
          },
        );
      }
    },
    onSelectBoard(boardIds) {
      this.boardIds = boardIds;
    },
    fetchBoardList() {
      API.Board.fetchFullList(this.username).then(
        (resp) => {
          const boardOptions = [];
          resp.data.forEach(
            (board) => {
              const boardOption = { name: board.name, value: board.id };
              boardOptions.push(boardOption);
            },
          );
          this.boardOptions = boardOptions;
        },
        () => {
          console.log('Error occurs while fetch board full list');
        },
      );
    },
  },
};
</script>
