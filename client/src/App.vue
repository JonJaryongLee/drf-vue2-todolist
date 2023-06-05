<template>
  <div class="page">
    <header class="header">
      <h1 class="title">Todo List</h1>
      <b-input-group>
        <b-form-input placeholder="할 일을 입력하세요" v-model="userInput"></b-form-input>
        <b-input-group-append>
          <b-button @click="addTodo">추가</b-button>
        </b-input-group-append>
      </b-input-group>
    </header>
    <main class="main">
      <div class="loading-wrapper" v-if="isLoading">
        <b-spinner label="Spinning"></b-spinner>
      </div>
      <div class="todos-wrapper" v-else-if="todos.length">
        <b-list-group>
          <b-list-group-item class="item-container" v-for="todo in filteredTodos" :key="todo.id">
            <b-form-checkbox v-model="todo.is_completed" @change="changeCompleted(todo)">
              <span :class="{ done: todo.is_completed }">{{ todo.title }}</span>
            </b-form-checkbox>
            <b-button-close class="close-btn" @click="deleteTodo(todo.id)"></b-button-close>
          </b-list-group-item>
        </b-list-group>
        <b-button class="toggle-btn" variant="primary" @click="hideCompleted = !hideCompleted">
          {{ hideCompleted ? "전체" : "완료된 항목 숨기기" }}
        </b-button>
      </div>
      <div>
        할 일이 없습니다.
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";
import { onErrorCaptured } from "vue";
export default {
  data() {
    return {
      URL: "http://localhost:8000/api",
      isLoading: true,
      todos: [],
      hideCompleted: false,
      userInput: "",
    }
  },
  created() {
    this.getTodos();
    this.isLoading = false;
  },
  computed: {
    filteredTodos() {
      if (this.hideCompleted) {
        return this.todos.filter((todo) => !todo.is_completed)
      }
      return this.todos;
    }
  },
  methods: {
    async getTodos() {
      try {
        const response = await axios.get(`${this.URL}/todos/`);
        this.todos = response.data;
      } catch (error) {
        console.error(error);
        if(error.response.status === 404) {
          this.todos = [];
        }
      }
    },
    async addTodo() {
      if (this.userInput === "") {
        return;
      }
      this.isLoading = true;
      try {
        await axios.post(`${this.URL}/todos/`, {
          title: this.userInput,
        });
      } catch (error) {
        console.error(error);
      }
      this.getTodos();
      this.userInput = "";
      this.isLoading = false;
    },
    async changeCompleted(todo) {
      this.isLoading = true;
      try {
        await axios.patch(`${this.URL}/todos/${todo.id}/`, {
          title: todo.title,
          is_completed: todo.is_completed,
        })
      } catch (error) {
        console.error(error);
      }
      this.getTodos();
      this.isLoading = false;
    },
    async deleteTodo(id) {
      this.isLoading = true;
      try {
        await axios.delete(`${this.URL}/todos/${id}/`);
      } catch (error) {
        console.error(error);
      }
      this.getTodos();
      this.isLoading = false;
    }
  },
}
</script>

<style scoped>
.page {
  padding: 1rem;
  height: 100vh;
}

.header {
  height: 15%;
}

.title {
  text-align: center;
}

.main {
  height: 75%;
}

.loading-wrapper,
.todos-wrapper {
  height: 100%;
}

.loading-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.done {
  text-decoration: line-through;
}

.toggle-btn {
  margin-top: 1rem;
}

.item-container {
  display: flex;
  justify-content: space-between;
}
</style>