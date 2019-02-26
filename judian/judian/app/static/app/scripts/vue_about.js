Vue.component('todo-item-simple', {
    template: '<li>This is a todo</li>',
})

Vue.component('grocery-item', {
    props: ['gc'],
    template: '<li>{{ gc.text }}</li>'
})

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'Hello Vue!',
        people: people,
        todos: [
            { text: 'Learn JavaScript' },
            { text: 'Learn Vue' },
            { text: 'Build something awesome' }
        ],
        groceryList: [
            { id: 0, text: 'Vegetables' },
            { id: 1, text: 'Cheese' },
            { id: 2, text: 'Whatever else humans are supposed to eat' }
        ]
    },
    methods: {
        greet: function (name) {
            console.log('Hello from ' + name + '!')
        },
        reverseMessage: function () {
            this.message = this.message.split('').reverse().join('')
        }
    }
});

app.todos.push({ text: 'Show me the money'})